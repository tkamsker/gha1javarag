/*
 * Copyright 2009 - 2012 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.core.service.impl;

import java.util.Date;
import java.util.List;

import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.dao.DataAccessException;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

import at.a1ta.bite.audit.core.Auditor;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.cuco.core.audit.ContextAwareAuditHelper;
import at.a1ta.cuco.core.audit.CuCoAuditActivity;
import at.a1ta.cuco.core.audit.CuCoAuditScope;
import at.a1ta.cuco.core.dao.cusco.CusCoResponse;
import at.a1ta.cuco.core.dao.db.CustomerUnlockRequestDao;
import at.a1ta.cuco.core.service.CuscoUnlockService;
import at.a1ta.cuco.core.service.CustomerUnlockService;
import at.a1ta.cuco.core.shared.dto.Customer;
import at.a1ta.cuco.core.shared.dto.access.ContextAwareCustomerUnlockRequest;
import at.a1ta.cuco.core.shared.dto.access.UnlockRequestContext;
import at.a1ta.cuco.core.shared.dto.access.UnlockStateEnum;

@Service
public class CustomerUnlockServiceImpl implements CustomerUnlockService {

  private static final Logger logger = LoggerFactory.getLogger(CustomerUnlockServiceImpl.class);

  private SettingService settings;
  private CustomerUnlockRequestDao unlockDao;
  private CuscoUnlockService cuscoUnlockService;

  @Override
  public boolean checkIfUnlockedForSession(Customer customer, UserInfo user, String sessionId) {
    Assert.notNull(customer);
    Assert.notNull(user);

    List<ContextAwareCustomerUnlockRequest> result = unlockDao.findByCustomerIdAndUsernameAndContextKey(customer.getCustomerNumber(), user.getBiteUser(), sessionId);
    if (result.isEmpty()) {
      return false;
    }

    for (ContextAwareCustomerUnlockRequest unlockRequest : result) {
      if ((unlockRequest != null && UnlockStateEnum.FINISHED_UNLOCKED.equals(unlockRequest.getState()))) {
        return true;
      }
    }
    return false;
  }

  @Override
  public boolean checkIfUnlockded(Customer customer, UserInfo user, String contextKey, String referenceKey) {
    Assert.notNull(customer);
    Assert.notNull(user);
    Assert.notNull(referenceKey);

    ContextAwareCustomerUnlockRequest result = unlockDao.findByCustomerIdAndUsernameAndJobIdAndSessionKey(customer.getCustomerNumber(), user.getBiteUser(), referenceKey, contextKey);

    if (result == null || !UnlockStateEnum.FINISHED_UNLOCKED.equals(result.getState())) {
      return false;
    }
    Auditor.audit(ContextAwareAuditHelper.createFor(CuCoAuditScope.CUSTOMER, CuCoAuditActivity.UNLOCK).withCustomerNumber(customer.getId()));

    return true;
  }

  @Override
  public CusCoResponse sendUnlockRequest(Customer customer, UserInfo user, UnlockRequestContext context, String contextKey) {
    long start = System.currentTimeMillis();
    logger.debug("START:sendUnlockRequest;username:" + user.getUsername() + ";customer:" + customer.getId() + ";;;");
    Assert.notNull(customer);
    Assert.notNull(user);
    Assert.notNull(context);
    Assert.hasText(contextKey);

    ContextAwareCustomerUnlockRequest request = new ContextAwareCustomerUnlockRequest();
    request.setContext(context);
    request.setCustomerId(customer.getId());
    request.setSessionKey(contextKey);
    request.setUser(user.getBiteUser());

    Auditor.audit(ContextAwareAuditHelper.createFor(CuCoAuditScope.CUSTOMER, CuCoAuditActivity.REQUEST_UNLOCK).withCustomerNumber(customer.getId()));

    long start_cusco = System.currentTimeMillis();
    logger.debug("START:sendUnlockRequest:prepareForSign;username:" + user.getUsername() + ";customer:" + customer.getId() + ";;;");
    CusCoResponse response;
    try {
      response = cuscoUnlockService.prepareForSign(customer, user, null, settings.getValue("dupos.cusco.template"));
    } catch (Exception e) {
      logger.error("Error while preparing document for sign", e);
      throw e;
    }
    long end_cusco = System.currentTimeMillis();
    request.setJobId(response.getJobId());
    logger.debug("END:sendUnlockRequest:prepareForSign;username:" + user.getUsername() + ";customer:" + customer.getId() + ";cusco.jobid:" + response.getJobId() + ";duration:"
        + (end_cusco - start_cusco) + "ms;");
    unlockDao.insert(request);

    long end = System.currentTimeMillis();
    logger.debug("END:sendUnlockRequest;username:" + user.getUsername() + ";customer:" + customer.getId() + ";cusco.jobid:" + response.getJobId() + ";duration:" + (end - start) + "ms;");
    return response;
  }

  @Override
  public boolean updateUnlockRequestStateAndCheckIfUnlocked(Customer customer, UserInfo user, String contextKey, String referenceKey) {
    try {
      long start = System.currentTimeMillis();
      logger.debug("START:updateUnlockRequestStateAndCheckIfUnlocked;username:" + user.getUsername() + ";customer:" + customer.getId() + ";cusco.jobid:" + referenceKey + ";;");
      logger.debug("START:updateUnlockRequestStateAndCheckIfUnlocked:checkStatusForSigned;username:" + user.getUsername() + ";customer:" + customer.getId() + ";cusco.jobid:" + referenceKey + ";;");
      CusCoResponse response = cuscoUnlockService.checkStatusForSigned(referenceKey);
      long end_cusco = System.currentTimeMillis();
      logger.debug("END:updateUnlockRequestStateAndCheckIfUnlocked:checkStatusForSigned;username:" + user.getUsername() + ";customer:" + customer.getId() + ";cusco.jobid:" + referenceKey
          + ";duration:" + (end_cusco - start) + "ms;");

      if (StringUtils.equalsIgnoreCase("signed", response.getStatus())) {
        ContextAwareCustomerUnlockRequest request = unlockDao.findByCustomerIdAndUsernameAndJobIdAndSessionKey(customer.getCustomerNumber(), user.getBiteUser(), referenceKey, contextKey);

        if (request != null) {
          request.setState(UnlockStateEnum.FINISHED_UNLOCKED);
          logger.debug("checkStatusForSigned:FINISHED_UNLOCKED;username:" + user.getUsername() + ";customer:" + customer.getId() + ";cusco.jobid:" + referenceKey + ";;");
          request.setFinished(new Date());
        }
        unlockDao.update(request);

        Auditor.audit(ContextAwareAuditHelper.createFor(CuCoAuditScope.CUSTOMER, CuCoAuditActivity.UNLOCK).withCustomerNumber(customer.getId()));
      } else if (!StringUtils.equalsIgnoreCase("Unknown", response.getStatus())) {
        ContextAwareCustomerUnlockRequest request = unlockDao.findByCustomerIdAndUsernameAndJobIdAndSessionKey(customer.getCustomerNumber(), user.getBiteUser(), referenceKey, contextKey);

        if (request != null) {
          request.setState(UnlockStateEnum.FINISHED_LOCKED);
          logger.debug("checkStatusForSigned:FINISHED_LOCKED;username:" + user.getUsername() + ";customer:" + customer.getId() + ";cusco.jobid:" + referenceKey + ";;");
          request.setFinished(new Date());
        }
        unlockDao.update(request);

        Auditor.audit(ContextAwareAuditHelper.createFor(CuCoAuditScope.CUSTOMER, CuCoAuditActivity.LOCK).withCustomerNumber(customer.getId()));
      }
      long end = System.currentTimeMillis();
      logger.debug(
          "END:updateUnlockRequestStateAndCheckIfUnlocked;username:" + user.getUsername() + ";customer:" + customer.getId() + ";cusco.jobid:" + referenceKey + ";duration:" + (end - start) + "ms;");
    } catch (DataAccessException e) {
      logger.info("Error while requesting for " + customer.getId() + " / " + user.getUsername() + "/ " + referenceKey, e);
    }

    return checkIfUnlockded(customer, user, contextKey, referenceKey);
  }

  @Override
  public void lockOverride(Customer customer, UserInfo user, String sessionId, UnlockStateEnum state) {
    List<ContextAwareCustomerUnlockRequest> result = unlockDao.findByCustomerIdAndUsernameAndContextKey(customer.getCustomerNumber(), user.getBiteUser(), sessionId);

    if (result.isEmpty()) {
      Auditor.audit(ContextAwareAuditHelper.createFor(CuCoAuditScope.CUSTOMER, CuCoAuditActivity.LOCK_OVERRIDE).withCustomerNumber(customer.getId()));

      ContextAwareCustomerUnlockRequest request = new ContextAwareCustomerUnlockRequest();
      request.setContext(UnlockRequestContext.SESSION);
      request.setCreated(new Date());
      request.setCustomerId(customer.getId());
      request.setFinished(new Date());
      request.setSessionKey(sessionId);
      request.setState(state);
      request.setUser(user.getBiteUser());
      request.setJobId("manual-override-" + user.getUsername() + "-" + sessionId);
      request.setFinished(request.getCreated());
      unlockDao.insert(request);
      return;
    }

    for (ContextAwareCustomerUnlockRequest request : result) {
      request.setState(state);
      request.setFinished(new Date());
      Auditor.audit(ContextAwareAuditHelper.createFor(CuCoAuditScope.CUSTOMER, CuCoAuditActivity.LOCK_OVERRIDE).withCustomerNumber(customer.getId()));
      unlockDao.update(request);
    }
  }

  @Autowired(required = false)
  public void setUnlockDao(CustomerUnlockRequestDao unlockDao) {
    this.unlockDao = unlockDao;
  }

  @Autowired
  public void setCuscoUnlockService(CuscoUnlockService cuscoUnlockService) {
    this.cuscoUnlockService = cuscoUnlockService;
  }

  @Autowired
  public void setSettings(SettingService settings) {
    this.settings = settings;
  }

}
