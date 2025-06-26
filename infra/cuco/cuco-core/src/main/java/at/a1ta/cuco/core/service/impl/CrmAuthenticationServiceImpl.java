package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.HashMap;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.cuco.core.dao.db.CucoLogsDao;
import at.a1ta.cuco.core.service.CrmAuthenticationService;
import at.a1ta.cuco.core.shared.dto.BillingAccountNumber;
import at.a1ta.cuco.core.shared.dto.CrmAuthenticationInfo;
import at.a1ta.cuco.core.shared.dto.Party;
import at.mobilkom.crm.authentication.GetCustomerPasswordsRequestDocument;
import at.mobilkom.crm.authentication.GetCustomerPasswordsRequestDocument.GetCustomerPasswordsRequest;
import at.mobilkom.crm.authentication.GetCustomerPasswordsResponseDocument;
import at.mobilkom.crm.authentication.GetCustomerPasswordsResponseDocument.GetCustomerPasswordsResponse;
import at.mobilkom.crm.authentication.Password;
import at.mobilkom.crm.authentication.PasswordTypeEnum;

import com.telekomaustriagroup.esb.crmauthenticationsvc.CrmAuthenticationSvcStub;

@Service
public class CrmAuthenticationServiceImpl extends BaseEsbClient<CrmAuthenticationSvcStub> implements CrmAuthenticationService {

  private static final Logger LOGGER = LoggerFactory.getLogger(CrmAuthenticationServiceImpl.class);
  @Autowired
  private SettingService settingService;
  @Autowired
  private CucoLogsDao cucoLogsDao;

  private static final String PASSWORDVIEW_PASSWORDTYPE = "mobile PW";

  @Override
  public HashMap<String, CrmAuthenticationInfo> getCustomerPasswords(ArrayList<BillingAccountNumber> bans, Party party, UserInfo userInfo) {
    HashMap<String, CrmAuthenticationInfo> result = new HashMap<String, CrmAuthenticationInfo>();
    for (BillingAccountNumber curBan : bans) {
      CrmAuthenticationInfo crmAuthenticationInfo = new CrmAuthenticationInfo(CrmAuthenticationInfo.LOADING);

      try {
        GetCustomerPasswordsRequestDocument getCustomerPasswordsRequestDocument = GetCustomerPasswordsRequestDocument.Factory.newInstance();
        GetCustomerPasswordsRequest request = GetCustomerPasswordsRequest.Factory.newInstance();
        request.setBan(curBan.getBan() + "");
        request.setCallingSystem("CUCO");
        getCustomerPasswordsRequestDocument.setGetCustomerPasswordsRequest(request);
        crmAuthenticationInfo.setStatus(CrmAuthenticationInfo.NOT_RECEIVED);
        crmAuthenticationInfo.setBan(curBan.getBan() + "");
        GetCustomerPasswordsResponseDocument responseDoc = stub.getCustomerPasswords(getCustomerPasswordsRequestDocument, null);
        GetCustomerPasswordsResponse response = responseDoc.getGetCustomerPasswordsResponse();
        if (response != null && response.getPasswords() != null && response.getPasswords().getPasswordArray() != null) {
          crmAuthenticationInfo.setStatus(CrmAuthenticationInfo.LOADED);
          for (Password pwd : response.getPasswords().getPasswordArray()) {
            if (pwd.getType() != null && pwd.getValue() != null && pwd.getType() == PasswordTypeEnum.BAN) { // && pwd.getState()==PasswordStateEnum.ACTIVE
              crmAuthenticationInfo.setPassword(pwd.getValue());
            }
          }
          if (crmAuthenticationInfo.getPassword() != null && !crmAuthenticationInfo.getPassword().isEmpty()) {
            cucoLogsDao.insertLogEntryForViewPassword(party.getId(), userInfo.getName(), userInfo.getUsername(),
                settingService.getValueOrDefault("cucoLogsPasswordViewPasswordType", PASSWORDVIEW_PASSWORDTYPE), curBan.getBan() + "");
          }
        } else {
          crmAuthenticationInfo.setStatus(CrmAuthenticationInfo.NOT_RECEIVED);
        }
      } catch (Exception ex) {
        crmAuthenticationInfo.setStatus(CrmAuthenticationInfo.ERROR);
        LOGGER.error("Error while loading CrmAuthentication", ex);
      }
      result.put(curBan.getBan() + "", crmAuthenticationInfo);
    }
    return result;
  }
}
