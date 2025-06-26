package at.a1ta.cuco.core.service.impl;

import java.io.File;

import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.service.PartyCustomerLoyaltyService;
import at.a1ta.cuco.core.shared.dto.PartyCustomerLoyaltyInfo;
import at.a1telekom.cll.customerloyalty.ConnectPlusCustomer;
import at.a1telekom.cll.customerloyalty.IsConnectPlusCustomerRequest;
import at.a1telekom.cll.customerloyalty.IsConnectPlusCustomerRequestDocument;
import at.a1telekom.cll.customerloyalty.IsConnectPlusCustomerResponse;
import at.a1telekom.cll.customerloyalty.IsConnectPlusCustomerResponseDocument;

import com.telekomaustriagroup.esb.customerloyalty.CustomerLoyaltyStub;

@Service
public class PartyCustomerLoyaltyServiceImpl extends BaseEsbClient<CustomerLoyaltyStub> implements PartyCustomerLoyaltyService {

  private static final Logger LOGGER = LoggerFactory.getLogger(PartyCustomerLoyaltyServiceImpl.class);
  @Autowired
  private SettingService settingService;

  @Override
  public PartyCustomerLoyaltyInfo getParty(long partyId) {
    if (!settingService.getBooleanValue("partyDataPortletView.showA1ConnectPlusInfo", true)) {
      return null;
    }

    PartyCustomerLoyaltyInfo partyCustomerLoyaltyInfo = new PartyCustomerLoyaltyInfo(PartyCustomerLoyaltyInfo.LOADING);

    try {
      IsConnectPlusCustomerRequestDocument isConnectPlusCustomerRequestDocument = IsConnectPlusCustomerRequestDocument.Factory.newInstance();
      IsConnectPlusCustomerRequest request = IsConnectPlusCustomerRequest.Factory.newInstance();
      ConnectPlusCustomer addNewCustomer = request.addNewCustomer();
      addNewCustomer.setPartyId(Long.toString(partyId));
      isConnectPlusCustomerRequestDocument.setIsConnectPlusCustomerRequest(request);
      partyCustomerLoyaltyInfo.setStaus(PartyCustomerLoyaltyInfo.NOT_RECEIVED);

      IsConnectPlusCustomerResponse response;
      IsConnectPlusCustomerResponseDocument responseDoc;
      String mockResponseFileName = System.getProperty("catalina.base") + "//mocks//CustomerLoyaltyIsConnectPlusCustomerCMSYS5905.xml";
      if (settingService.getBooleanValue("testModeActive", false) && new File(mockResponseFileName).exists()) {
        response = IsConnectPlusCustomerResponseDocument.Factory.parse(FileUtils.readFileToString(new File(mockResponseFileName))).getIsConnectPlusCustomerResponse();
      } else {
        responseDoc = stub.isConnectPlusCustomer(isConnectPlusCustomerRequestDocument, null);
        response = responseDoc.getIsConnectPlusCustomerResponse();
      }
      if (response != null) {
        partyCustomerLoyaltyInfo.setStaus(PartyCustomerLoyaltyInfo.LOADED);
        partyCustomerLoyaltyInfo.setConnectPlusCustomer(response.getConnectPlusCustomer());
      } else {
        partyCustomerLoyaltyInfo.setStaus(PartyCustomerLoyaltyInfo.NOT_RECEIVED);
      }
    } catch (Exception ex) {
      partyCustomerLoyaltyInfo.setStaus(PartyCustomerLoyaltyInfo.ERROR);
      LOGGER.error("Error while loading CustomerLoyalty", ex);
    }
    return partyCustomerLoyaltyInfo;
  }

}
