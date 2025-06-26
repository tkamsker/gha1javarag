package at.a1ta.cuco.core.service.impl;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import a1.gdpr.webservice.Brand;
import a1.gdpr.webservice.GetCurrentDeclarationOfConsentForPartyRequest;
import a1.gdpr.webservice.GetCurrentDeclarationOfConsentForPartyRequestDocument;
import a1.gdpr.webservice.GetCurrentDeclarationOfConsentForPartyResponseDocument;
import a1.gdpr.webservice.Touchpoint;
import a1.gdpr.webservice.UserType;
import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.cuco.core.service.PartyDeclarationOfConsentService;
import at.a1ta.cuco.core.shared.dto.PartyDeclarationOfConsentInfo;
import at.a1ta.cuco.core.shared.dto.PartyDeclarationOfConsentInfo.StatusNeedForAction;
import at.a1ta.cuco.core.shared.dto.PartyDeclarationOfConsentInfo.StatusOfCompleteness;

import com.telekomaustriagroup.esb.partydeclarationofconsent.PartyDeclarationOfConsentStub;

@Service
public class PartyDeclarationOfConsentServiceImpl extends BaseEsbClient<PartyDeclarationOfConsentStub> implements PartyDeclarationOfConsentService {

  private static final Logger LOGGER = LoggerFactory.getLogger(PartyDeclarationOfConsentServiceImpl.class);

  @Override
  public PartyDeclarationOfConsentInfo getCurrentDeclarationOfConsentForParty(String partyId, String userId, Brand.Enum brand, UserType.Enum userType) {
    PartyDeclarationOfConsentInfo partyDeclarationOfConsentInfo = new PartyDeclarationOfConsentInfo(PartyDeclarationOfConsentInfo.LOADING, StatusOfCompleteness.UNKNOWN);
    try {
      GetCurrentDeclarationOfConsentForPartyRequestDocument getCurrentDeclarationOfConsentForPartyRequestDocument = GetCurrentDeclarationOfConsentForPartyRequestDocument.Factory.newInstance();
      GetCurrentDeclarationOfConsentForPartyRequest request = GetCurrentDeclarationOfConsentForPartyRequest.Factory.newInstance();
      request.setPartyId(partyId);
      request.setTouchpoint(Touchpoint.CUSTOMER_COCKPIT);
      request.setBrand(Brand.A_1_RBM);
      request.setUser(userId);
      request.setUserType(UserType.CUSTOMER);
      if (brand != null) {
        request.setBrand(brand);
      }

      if (userType != null) {
        request.setUserType(userType);
      }
      getCurrentDeclarationOfConsentForPartyRequestDocument.setGetCurrentDeclarationOfConsentForPartyRequest(request);
      partyDeclarationOfConsentInfo.setStaus(PartyDeclarationOfConsentInfo.NOT_RECEIVED);
      GetCurrentDeclarationOfConsentForPartyResponseDocument response = stub.getCurrentDeclarationOfConsentForParty(getCurrentDeclarationOfConsentForPartyRequestDocument, null);
      if (response != null && response.getGetCurrentDeclarationOfConsentForPartyResponse() != null && response.getGetCurrentDeclarationOfConsentForPartyResponse().getParty() != null
          && response.getGetCurrentDeclarationOfConsentForPartyResponse().getParty().getCurrentDeclarationOfConsent() != null) {
        partyDeclarationOfConsentInfo.setStaus(PartyDeclarationOfConsentInfo.LOADED);
        partyDeclarationOfConsentInfo.setStatusOfCompleteness(StatusOfCompleteness.valueOf(response.getGetCurrentDeclarationOfConsentForPartyResponse().getParty().getCurrentDeclarationOfConsent()
            .getStatusOfCompleteness().toString()));
        partyDeclarationOfConsentInfo.setStatusNeedForAction(StatusNeedForAction.valueOf(response.getGetCurrentDeclarationOfConsentForPartyResponse().getParty().getCurrentDeclarationOfConsent()
            .getStatusNeedForAction().toString()));
      } else {
        partyDeclarationOfConsentInfo.setStaus(PartyDeclarationOfConsentInfo.NOT_RECEIVED);
      }
    } catch (Exception ex) {
      partyDeclarationOfConsentInfo.setStaus(PartyDeclarationOfConsentInfo.ERROR);
      LOGGER.error("Error while loading PartyDeclarationOfConsent", ex);
    }

    return partyDeclarationOfConsentInfo;
  }

}
