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
package at.a1ta.cuco.core.dao.db.impl;

import java.util.Date;
import java.util.HashMap;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;
import org.springframework.orm.ibatis.SqlMapClientTemplate;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.shared.dto.access.ContextAwareCustomerUnlockRequest;
import at.a1ta.cuco.core.shared.dto.access.UnlockStateEnum;

@RunWith(MockitoJUnitRunner.class)
public class CustomerUnlockRequestDaoImplTest {

  @Mock
  private SqlMapClientTemplate sqlMapClientTemplateMock;

  private CustomerUnlockRequestDaoImpl dao;

  @Before
  public void setUp() {
    dao = new CustomerUnlockRequestDaoImpl();
    dao.setSqlMapClientTemplate(sqlMapClientTemplateMock);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testInsertWithNull() {
    dao.insert(null);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testInsertWithNegativeCustomerId() {
    ContextAwareCustomerUnlockRequest request = createRequest(-1, 10L, "session");
    request.setJobId("jobId");
    dao.insert(request);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testInsertWithEmptyJobId() {
    ContextAwareCustomerUnlockRequest request = createRequest(1, 10L, "session");
    request.setJobId("");
    dao.insert(request);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testInsertWithEmptyUsername() {
    ContextAwareCustomerUnlockRequest request = createRequest(1, null, "session");
    request.setJobId("job");
    dao.insert(request);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testInsertWithEmptySessionKey() {
    ContextAwareCustomerUnlockRequest request = createRequest(1, 10L, "");
    request.setJobId("job");
    dao.insert(request);
  }

  @Test
  public void testInsert() {
    ContextAwareCustomerUnlockRequest request = createRequest(1, 10L, "session");
    request.setJobId("job");

    ArgumentCaptor<String> statementCaptor = ArgumentCaptor.forClass(String.class);
    ArgumentCaptor<Object> paramsCaptor = ArgumentCaptor.forClass(Object.class);

    dao.insert(request);

    Mockito.verify(sqlMapClientTemplateMock, Mockito.times(1)).insert(statementCaptor.capture(), paramsCaptor.capture());
    Assert.assertEquals("CustomerUnlockRequest.insert", statementCaptor.getValue());
    Assert.assertEquals(request, paramsCaptor.getValue());
  }

  @Test(expected = IllegalArgumentException.class)
  public void testUpdateWithNull() {
    dao.update(null);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testUpdateWithNegativeCustomerId() {
    ContextAwareCustomerUnlockRequest request = createRequest(-1, 10L, "session");
    request.setJobId("jobId");
    dao.update(request);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testUpdateWithEmptyJobId() {
    ContextAwareCustomerUnlockRequest request = createRequest(1, 10L, "session");
    request.setJobId("");
    dao.update(request);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testUpdateWithEmptyUsername() {
    ContextAwareCustomerUnlockRequest request = createRequest(1, null, "session");
    request.setJobId("job");
    dao.update(request);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testUpdateWithEmptySessionKey() {
    ContextAwareCustomerUnlockRequest request = createRequest(1, 10L, "");
    request.setJobId("job");
    dao.update(request);
  }

  @Test
  public void testUpate() {
    ContextAwareCustomerUnlockRequest request = createRequest(1, 10L, "session");
    request.setJobId("job");
    request.setFinished(new Date());
    request.setState(UnlockStateEnum.FINISHED_UNLOCKED);

    ArgumentCaptor<String> statementCaptor = ArgumentCaptor.forClass(String.class);
    ArgumentCaptor<Object> paramsCaptor = ArgumentCaptor.forClass(Object.class);

    dao.update(request);

    Mockito.verify(sqlMapClientTemplateMock, Mockito.times(1)).update(statementCaptor.capture(), paramsCaptor.capture());
    Assert.assertEquals("CustomerUnlockRequest.update", statementCaptor.getValue());
    Assert.assertEquals(request, paramsCaptor.getValue());
  }

  @SuppressWarnings({"rawtypes"})
  @Test
  public void testFindByCustomerIdAndUsernameAndJobIdAndSessionKey() {
    long customerId = 100100100;
    BiteUser user = new BiteUser();
    user.setId(10L);
    String jobId = "jobId";
    String sessionKey = "sessionKey";

    ArgumentCaptor<String> statementCaptor = ArgumentCaptor.forClass(String.class);
    ArgumentCaptor<HashMap> paramsCaptor = ArgumentCaptor.forClass(HashMap.class);

    dao.findByCustomerIdAndUsernameAndJobIdAndSessionKey(customerId, user, jobId, sessionKey);

    Mockito.verify(sqlMapClientTemplateMock, Mockito.times(1)).queryForObject(statementCaptor.capture(), paramsCaptor.capture());
    Assert.assertEquals("CustomerUnlockRequest.findCustomerUnlockRequestByCustomerIdAndUsernameAndJobIdAndSessionKey", statementCaptor.getValue());

    Assert.assertEquals(jobId, paramsCaptor.getValue().get("jobId"));
    Assert.assertEquals(customerId, paramsCaptor.getValue().get("customerId"));
    Assert.assertEquals(10L, paramsCaptor.getValue().get("userId"));
    Assert.assertEquals(sessionKey, paramsCaptor.getValue().get("sessionKey"));

  }

  @SuppressWarnings({"rawtypes"})
  @Test
  public void testFindByCustomerIdAndUsernameAndSessionKey() {
    BiteUser user = new BiteUser();
    user.setId(10L);
    long customerId = 100100100;
    String sessionKey = "sessionKey";

    ArgumentCaptor<String> statementCaptor = ArgumentCaptor.forClass(String.class);
    ArgumentCaptor<HashMap> paramsCaptor = ArgumentCaptor.forClass(HashMap.class);

    dao.findByCustomerIdAndUsernameAndContextKey(customerId, user, sessionKey);

    Mockito.verify(sqlMapClientTemplateMock, Mockito.times(1)).queryForList(statementCaptor.capture(), paramsCaptor.capture());
    Assert.assertEquals("CustomerUnlockRequest.findCustomerUnlockRequestByCustomerIdAndUsernameAndSessionKey", statementCaptor.getValue());

    Assert.assertEquals(customerId, paramsCaptor.getValue().get("customerId"));
    Assert.assertEquals(10L, paramsCaptor.getValue().get("userId"));
    Assert.assertEquals(sessionKey, paramsCaptor.getValue().get("sessionKey"));
  }

  private ContextAwareCustomerUnlockRequest createRequest(int i, Long userId, String sessionKey) {
    ContextAwareCustomerUnlockRequest request = new ContextAwareCustomerUnlockRequest();
    request.setCustomerId(i);
    if (userId != null) {
      BiteUser user = new BiteUser();
      user.setId(userId);
      request.setUser(user);
    }
    request.setSessionKey(sessionKey);
    return request;
  }
}
