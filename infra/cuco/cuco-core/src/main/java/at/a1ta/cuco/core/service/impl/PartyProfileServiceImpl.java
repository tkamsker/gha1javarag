package at.a1ta.cuco.core.service.impl;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.Date;

import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.service.PartyProfileService;
import at.a1ta.cuco.core.shared.dto.PartyAdditionalInfo;
import at.a1ta.cuco.core.shared.dto.PartyProfileInfo;
import at.a1ta.cuco.core.shared.dto.PartyProfileNPSInfo;
import at.a1ta.cuco.core.shared.dto.PartyProfileSolvency;
import at.a1ta.cuco.core.shared.dto.PointOfSaleInfo;
import at.a1ta.cuco.core.shared.dto.StandardAddress;
import at.a1ta.cuco.core.shared.dto.StandardAddress.AddressDataSource;
import at.a1ta.cuco.core.shared.dto.SupportingUnit;
import at.a1telekom.parma.pps.v1_0.GetPartyFields;
import at.a1telekom.parma.pps.v1_0.GetPartyRequest;
import at.a1telekom.parma.pps.v1_0.GetPartyRequestDocument;
import at.a1telekom.parma.pps.v1_0.GetPartyResponse;
import at.a1telekom.parma.pps.v1_0.GetPartyResponseDocument;
import at.a1telekom.parma.pps.v1_0.common.Address;
import at.a1telekom.parma.pps.v1_0.common.AuthorizationInfo;
import at.a1telekom.parma.pps.v1_0.common.ContactInformation;
import at.a1telekom.parma.pps.v1_0.common.NetPromoterScore;

import com.telekomaustriagroup.esb.partyprofile.PartyProfileStub;

@Service
public class PartyProfileServiceImpl extends BaseEsbClient<PartyProfileStub> implements PartyProfileService {

private static final Logger LOGGER = LoggerFactory.getLogger(PartyProfileServiceImpl.class);
  @Autowired
  private SettingService settingService;

  private static final String DEFAULT_SYSTEM = "CUCO";
  private static final String DEFAULT_USER = "UCuCO01";

  /**
   * Key for ...
   */
  private static final String DEALER_EMAIL_KEY = "EMAIL";
  /**
   * Key for ...
   */
  private static final String DEALER_PHONE_KEY = "PHONE";

  
  @Override
  public PartyProfileInfo getParty(long partyId) {
    if (!settingService.getBooleanValue("nps.showNPSInfo", false)) {
      return null;
    }
    PartyProfileInfo partyProfileInfo = new PartyProfileInfo(PartyProfileInfo.LOADING);

    try {
      GetPartyRequestDocument getPartyRequestDocument = GetPartyRequestDocument.Factory.newInstance();
      GetPartyRequest request = GetPartyRequest.Factory.newInstance();
      GetPartyFields getPartyFields = GetPartyFields.Factory.newInstance();
      getPartyFields.setPartyId(Integer.parseInt(partyId + ""));
      request.setGetPartyFields(getPartyFields);
      request.setAuthorizationInfo(AuthorizationInfo.Factory.newInstance());
      request.getAuthorizationInfo().setSystem(settingService.getValueOrDefault("esbPartyProfileSystem", DEFAULT_SYSTEM));
      request.getAuthorizationInfo().setUser(settingService.getValueOrDefault("esbPartyProfileUser", DEFAULT_USER));
      getPartyRequestDocument.setGetPartyRequest(request);
      partyProfileInfo.setStaus(PartyProfileInfo.NOT_RECEIVED);

      GetPartyResponse response;
      GetPartyResponseDocument responseDoc;
      String mockResponseFileName = System.getProperty("catalina.base") + "//mocks//PartyProfileGetPartyCMSYS3413.xml";
      if (settingService.getBooleanValue("testModeActive", false) && new File(mockResponseFileName).exists()) {
        response = GetPartyResponseDocument.Factory.parse(FileUtils.readFileToString(new File(mockResponseFileName))).getGetPartyResponse();
      } else {
        responseDoc = stub.getParty(getPartyRequestDocument, null);
        response = responseDoc.getGetPartyResponse();
      }
      
      if (response != null && response.getParty() != null && response.getParty().getNetPromoterScoreArray() != null) {
        partyProfileInfo.setStaus(PartyProfileInfo.LOADED);
        for (NetPromoterScore score : response.getParty().getNetPromoterScoreArray()) {
          if (score.getScoringType() != null && score.getScoringValue() != null && score.getScoringDate() != null) {
            Date date = score.getScoringDate().getTime();
            SimpleDateFormat sdf = new SimpleDateFormat("d.M.yyyy");
            String getScoringDate = sdf.format(date);
            partyProfileInfo.addToScores(new PartyProfileNPSInfo(score.getScoringType(), score.getScoringValue(), getScoringDate));
          }
        }
        if (response.getParty().getSolvency() == null || response.getParty().getSolvency().getCreditLimit() == null || response.getParty().getSolvency().getCreditLimit().getAmount() == null) {
        	LOGGER.info("did not receive creditlimit in PartyProfile");
        } else {
        	PartyProfileSolvency partyProfileSolvency = new PartyProfileSolvency();
        	partyProfileSolvency.setCreditLimit(response.getParty().getSolvency().getCreditLimit().getAmount().toPlainString());
        	partyProfileInfo.setSolvency(partyProfileSolvency);
        }

        PointOfSaleInfo posInfo = new PointOfSaleInfo();
        SupportingUnit supportingUnit = new SupportingUnit();
        
        
        
        if (response.getParty() == null || response.getParty().getSupportingUnit() == null) {
            posInfo.setStaus(PointOfSaleInfo.ERROR);
            supportingUnit.setStatus(SupportingUnit.ERROR);
            LOGGER.info("did not receive supportingUnit info in PartyProfile");
        } else {
            
            partyProfileInfo.setAccountManagementSegment(response.getParty().getAccountManagementSegment());
            supportingUnit.setSkzText(response.getParty().getSupportingUnit().getSkzText());
            supportingUnit.setShopSupport(response.getParty().getSupportingUnit().getShopSupport());
            supportingUnit.setSupportName(response.getParty().getSupportingUnit().getSupportName());
            
            if (response.getParty().getSupportingUnit().getContactInformation() != null) {
                for (final ContactInformation contactInformation : response.getParty().getSupportingUnit().getContactInformation().getListArray()) {
                    if (DEALER_EMAIL_KEY.equals(contactInformation.getType())) {
                        supportingUnit.setEmailAddress(contactInformation.getEmailAddress());
                    }
                    if (DEALER_PHONE_KEY.equals(contactInformation.getType())) {
                        supportingUnit.setPhoneNumber(contactInformation.getRawPhoneNumber());
                    }
                }
            }
            
            if (response.getParty().getPointOfSale() == null) {
                posInfo.setStaus(PointOfSaleInfo.NOT_RECEIVED);
            } else {
                posInfo.setAddress(extractAddress(response.getParty().getPointOfSale().getAddress()));
                posInfo.setDealerId(response.getParty().getPointOfSale().getDealerId());
                posInfo.setDealerName(response.getParty().getPointOfSale().getDealerName());
                posInfo.setDelearEmailId(response.getParty().getPointOfSale().getEMail());
                posInfo.setDealerPhonenumber(response.getParty().getPointOfSale().getPhoneNumber());
                posInfo.setStaus(PointOfSaleInfo.LOADED);
            }

            partyProfileInfo.setShopSupport(response.getParty().getSupportingUnit().getShopSupport());
            partyProfileInfo.setAccountManagementSegment(response.getParty().getAccountManagementSegment());

            supportingUnit.setStatus(SupportingUnit.LOADED);
            partyProfileInfo.setPosInfo(posInfo);
            partyProfileInfo.setSupportingUnit(supportingUnit);
        }
        
      } else {
        partyProfileInfo.setStaus(PartyProfileInfo.NOT_RECEIVED);
      }
    } catch (Exception ex) {
      partyProfileInfo.setStaus(PartyProfileInfo.ERROR);
      LOGGER.error("Error while loading PartyProfile", ex);
    }
    return partyProfileInfo;
  }

  @Override
  public String getBvkUser(String bvkUserId) {

    try {
      GetPartyRequestDocument getPartyRequestDocument = GetPartyRequestDocument.Factory.newInstance();
      GetPartyRequest request = GetPartyRequest.Factory.newInstance();
      GetPartyFields getPartyFields = GetPartyFields.Factory.newInstance();
      getPartyFields.setBvkId(bvkUserId.toUpperCase());
      request.setGetPartyFields(getPartyFields);
      request.setAuthorizationInfo(AuthorizationInfo.Factory.newInstance());
      request.getAuthorizationInfo().setSystem(settingService.getValueOrDefault("esbPartyProfileSystem", DEFAULT_SYSTEM));
      request.getAuthorizationInfo().setUser(settingService.getValueOrDefault("esbPartyProfileUser", DEFAULT_USER));
      getPartyRequestDocument.setGetPartyRequest(request);

      GetPartyResponse response;
      GetPartyResponseDocument responseDoc;
      String mockResponseFileName = System.getProperty("catalina.base") + "//mocks//PartyProfileGetPartyUsingBvkUserIdCMSYS3220.xml";
      if (settingService.getBooleanValue("testModeActive", false) && new File(mockResponseFileName).exists()) {
        response = GetPartyResponseDocument.Factory.parse(FileUtils.readFileToString(new File(mockResponseFileName))).getGetPartyResponse();
      } else {
        responseDoc = stub.getParty(getPartyRequestDocument, null);
        response = responseDoc.getGetPartyResponse();
      }
      return response.getParty().getPartyId() + "";
    } catch (Exception ex) {
      LOGGER.error("Error while loading PartyProfile Service using BvkUserID", ex);
    }
    return "";
  }

  @Override
  public String getOneTVUser(String oneTVUserId) {

    try {
      GetPartyRequestDocument getPartyRequestDocument = GetPartyRequestDocument.Factory.newInstance();
      GetPartyRequest request = GetPartyRequest.Factory.newInstance();
      GetPartyFields getPartyFields = GetPartyFields.Factory.newInstance();

      getPartyFields.addNewCloudService().setCloudServiceUsername(oneTVUserId);
      getPartyFields.getCloudService().setPlatformName(settingService.getValue("partyProfile.OneTvUser.setPlatformName"));

      request.setGetPartyFields(getPartyFields);
      request.setAuthorizationInfo(AuthorizationInfo.Factory.newInstance());
      request.getAuthorizationInfo().setSystem(settingService.getValueOrDefault("esbPartyProfileSystem", DEFAULT_SYSTEM));
      request.getAuthorizationInfo().setUser(settingService.getValueOrDefault("esbPartyProfileUser", DEFAULT_USER));
      getPartyRequestDocument.setGetPartyRequest(request);

      GetPartyResponse response;
      GetPartyResponseDocument responseDoc;

      responseDoc = stub.getParty(getPartyRequestDocument, null);
      response = responseDoc.getGetPartyResponse();
      return response.getParty().getPartyId() + "";
    } catch (Exception ex) {
      LOGGER.error("Error while loading PartyProfile Service using OneTVUserID", ex);
    }
    return "";
  }
  
  private StandardAddress extractAddress(Address esbAddress) {
      StandardAddress address = new StandardAddress();
      if (esbAddress != null) {
        address.setLkmsId(esbAddress.getLocationId());
        address.setStreet(esbAddress.getStreet().getStreetName());
        address.setHouseNumber(esbAddress.getHouseNumber());
        address.setBlock(esbAddress.getBlock());
        address.setStaircase(esbAddress.getStaircase());
        address.setFloorNumber(esbAddress.getFloorNumber());
        address.setDoorNumber(esbAddress.getDoorNumber());
        address.setAdditional(esbAddress.getAdditional());
        address.setPostcode(esbAddress.getStreet().getStreetPostcode());
        address.setVillage(esbAddress.getStreet().getStreetVillage());
        address.setCity(esbAddress.getStreet().getStreetCity());
        address.setCountry(esbAddress.getCountry3Char());
      }
      address.setDataSource(AddressDataSource.PARTY_SERVICE);
      return address;
    }

}
