package at.a1ta.cuco.core.service.impl;

import java.util.HashMap;
import java.util.Map;

import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.service.MasterSessionControlService;

import com.telekomaustriagroup.esb.mastersessioncontrol.MasterSessionControlStub;
import com.tibco.www.ns.mastersessioncontrol.CreateSessionDocument;
import com.tibco.www.ns.mastersessioncontrol.CreateSessionDocument.CreateSession;
import com.tibco.www.ns.mastersessioncontrol.LoginDataType;
import com.tibco.www.ns.mastersessioncontrol.ResponseDocument;

@Service
public class MasterSessionControlServiceImpl extends BaseEsbClient<MasterSessionControlStub> implements MasterSessionControlService {

  private static final Logger logger = LoggerFactory.getLogger(MasterSessionControlServiceImpl.class);
  private SettingService settingService;

  public MasterSessionControlServiceImpl() {

  }

  @Override
  public String getURLForDOCHome(String partyID, String username, String name, String ipAddress) {
    String url = null;
    try {
      CreateSessionDocument createSessionDocument = CreateSessionDocument.Factory.newInstance();
      String[] configuredRequestParamSettings = settingService.getValuesIgnoreMissing("gdprJune2017.masterSessionControlServiceLoginData");
      Map<String, String> configuredRequestParamMap = new HashMap<String, String>();
      for (String param : configuredRequestParamSettings) {
        if (StringUtils.isEmpty(param) || !param.contains("=") || param.split("=").length < 2) {
          continue;
        }
        configuredRequestParamMap.put(param.split("=")[0], param.split("=")[1]);
      }
      CreateSession createSession = CreateSession.Factory.newInstance();
      LoginDataType loginData = createSession.addNewLoginData();
      loginData.setAonAccountId(configuredRequestParamMap.containsKey("AonAccountId") ? configuredRequestParamMap.get("AonAccountId") : "0");
      loginData.setPhoneNumber(configuredRequestParamMap.containsKey("PhoneNumber") ? configuredRequestParamMap.get("PhoneNumber") : "");
      loginData.setMobileNumber(configuredRequestParamMap.containsKey("MobileNumber") ? configuredRequestParamMap.get("MobileNumber") : "");
      loginData.setMobileTariffType(configuredRequestParamMap.containsKey("MobileTariffType") ? configuredRequestParamMap.get("MobileTariffType") : "NONE");
      loginData.setBillingAccountId(configuredRequestParamMap.containsKey("BillingAccountId") ? configuredRequestParamMap.get("BillingAccountId") : "0");
      loginData.setBillingAccountNumber(configuredRequestParamMap.containsKey("BillingAccountNumber") ? configuredRequestParamMap.get("BillingAccountNumber") : "");
      loginData.setKumsPartnerId(partyID);
      loginData.setDisplayName(name);
      loginData.setLoginName(username);
      loginData.setRemoteIp(ipAddress);
      loginData.setLoginType(configuredRequestParamMap.containsKey("LoginType") ? configuredRequestParamMap.get("LoginType") : "AGENT");
      loginData.setCustomerType(configuredRequestParamMap.containsKey("CustomerType") ? configuredRequestParamMap.get("CustomerType") : "A1TA");
      loginData.setAuthenticationSystem(configuredRequestParamMap.containsKey("AuthenticationSystem") ? configuredRequestParamMap.get("AuthenticationSystem") : "CUSTOMER_COCKPIT");
      loginData.setRole(configuredRequestParamMap.containsKey("Role") ? configuredRequestParamMap.get("Role") : "MANAGE_CUSTOMER");
      loginData.setServiceId(configuredRequestParamMap.containsKey("ServiceId") ? configuredRequestParamMap.get("ServiceId") : "DOC_HOME");
      createSessionDocument.setCreateSession(createSession);
      ResponseDocument response = stub.createSession(createSessionDocument, null);
      if (response != null && response.getResponse() != null && response.getResponse().getEntryArray() != null && response.getResponse().getEntryArray(0).getRedirect() != null) {
        url = response.getResponse().getEntryArray(0).getRedirect();
      } else {
        if (response == null || response.getResponse() == null) {
          logger.error("null response from MasterSessionControl for DOC_HOME");
        } else {
          logger.error("Invalid response from MasterSessionControl for DOC_HOME", response);
        }
      }
    } catch (Exception ex) {
      logger.error("Error while getting Master session for DOC_HOME", ex);
    }

    return url;
  }

  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }

}
