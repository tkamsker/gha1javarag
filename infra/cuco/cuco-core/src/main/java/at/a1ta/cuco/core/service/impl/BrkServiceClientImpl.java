package at.a1ta.cuco.core.service.impl;

import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.TextService;
import at.a1ta.cuco.core.service.BrkServiceClient;
import at.a1ta.cuco.core.shared.dto.product.BRKAccountInfo;
import at.mobilkom.eai.brk2.GetBRKAccountInfosRequestDocument;
import at.mobilkom.eai.brk2.GetBRKAccountInfosRequestType;
import at.mobilkom.eai.brk2.GetBRKAccountInfosResponseDocument;
import at.mobilkom.eai.brk2.GetBRKAccountInfosResponseType;
import at.mobilkom.eai.brk2.GetBRKAccounts4BANRequestDocument;
import at.mobilkom.eai.brk2.GetBRKAccounts4BANRequestType;
import at.mobilkom.eai.brk2.GetBRKAccounts4BANResponseDocument;
import at.mobilkom.eai.brk2.GetBRKAccounts4BANResponseType;
import at.mobilkom.eai.tracking.TrackingType;
import at.mobilkom.eai.tracking.TrackingType.TopServiceConsumer;

import com.telekomaustriagroup.esb.brksvc.BrkSvcStub;

@Service
public class BrkServiceClientImpl extends BaseEsbClient<BrkSvcStub> implements BrkServiceClient {

  @Autowired
  TextService textService;
  private static final Logger logger = LoggerFactory.getLogger(BrkServiceClientImpl.class);

  @Override
  public BRKAccountInfo getBRKAccountInfo(String brkAccountNumber) {
    GetBRKAccountInfosRequestType getBRKAccountInfosRequestType = GetBRKAccountInfosRequestType.Factory.newInstance();
    getBRKAccountInfosRequestType.setBRKAccountNumber(brkAccountNumber);
    addTrackingDetails(getBRKAccountInfosRequestType.addNewTracking());
    getBRKAccountInfosRequestType.setShowSpecialConditions(true);
    getBRKAccountInfosRequestType.setShowHandlingFee(true);
    GetBRKAccountInfosRequestDocument getBrkAccountInfosRequestDocument = GetBRKAccountInfosRequestDocument.Factory.newInstance();
    getBrkAccountInfosRequestDocument.setGetBRKAccountInfosRequest(getBRKAccountInfosRequestType);
    GetBRKAccountInfosResponseType getBRKAccountInfosResponse = null;
    try {
      GetBRKAccountInfosResponseDocument getBRKAccountInfosResponseDocument = stub.getBRKAccountInfos(getBrkAccountInfosRequestDocument, null);
      getBRKAccountInfosResponse = getBRKAccountInfosResponseDocument.getGetBRKAccountInfosResponse();
    } catch (Exception e) {
      logger.error(e.getMessage(), e);
      throw new RuntimeException("An error occurred during the getEquipmentConsignees call: " + e.getMessage(), e);
    }
    BRKAccountInfo brkAccountInfo = new BRKAccountInfo();
    brkAccountInfo.setAccountNumber(brkAccountNumber);
    brkAccountInfo.setHandlingFee("-");
    if (getBRKAccountInfosResponse != null) {
      brkAccountInfo.setAccountName(getBRKAccountInfosResponse.getBRKAccountName());
      if (getBRKAccountInfosResponse.isSetHandlingFee() && StringUtils.isNotEmpty(getBRKAccountInfosResponse.getHandlingFee())) {
        Map<String, String> handlingFeesMap = getHandlingFeesDisplayTextMap();
        brkAccountInfo.setHandlingFee(handlingFeesMap.get(getBRKAccountInfosResponse.getHandlingFee()));
      }
    }
    return brkAccountInfo;
  }

  private Map<String, String> getHandlingFeesDisplayTextMap() {
    Map<String, String> map = new HashMap<String, String>();
    String[] entries = textService.getByKeyWithDefaultText("brkSvc_handlingKeyResponseMappings", "").getText().split("##");
    for (String entry : entries) {
      String[] tokens = entry.trim().split("=");
      if (tokens != null && tokens.length == 2) {
        map.put(tokens[0].trim(), tokens[1].trim());
      }
    }

    return map;
  }

  @Override
  public String getBRKAccountNumber(String banNumber) {
    String brkAccountNumber = null;
    GetBRKAccounts4BANRequestType getBRKAccounts4BANRequestType = GetBRKAccounts4BANRequestType.Factory.newInstance();
    getBRKAccounts4BANRequestType.setBillingAccountNumber(banNumber);

    getBRKAccounts4BANRequestType.setTracking(addTrackingDetails(getBRKAccounts4BANRequestType.addNewTracking()));
    GetBRKAccounts4BANRequestDocument getBRKAccounts4BANRequestDocument = GetBRKAccounts4BANRequestDocument.Factory.newInstance();
    getBRKAccounts4BANRequestDocument.setGetBRKAccounts4BANRequest(getBRKAccounts4BANRequestType);
    GetBRKAccounts4BANResponseType getBRKAccounts4BANResponse = null;
    try {
      GetBRKAccounts4BANResponseDocument bRKAccounts4BANResponseDocument = stub.getBRKAccounts4BAN(getBRKAccounts4BANRequestDocument, null);
      getBRKAccounts4BANResponse = bRKAccounts4BANResponseDocument.getGetBRKAccounts4BANResponse();
    } catch (Exception e) {
      logger.error(e.getMessage(), e);
      throw new RuntimeException("An error occurred during the getEquipmentConsignees call: " + e.getMessage(), e);
    }
    if (getBRKAccounts4BANResponse != null && getBRKAccounts4BANResponse.isSetBRKAccountItems() && getBRKAccounts4BANResponse.getBRKAccountItems().sizeOfBRKAccountItemArray() > 0) {
      brkAccountNumber = getBRKAccounts4BANResponse.getBRKAccountItems().getBRKAccountItemArray(0).getBRKAccount().getBRKAccountNumber();
    }
    return brkAccountNumber;
  }

  private TrackingType addTrackingDetails(TrackingType trackingDetails) {
    trackingDetails.setEnvironment(TrackingType.Environment.TEST);
    TopServiceConsumer addNewTopServiceConsumer = trackingDetails.addNewTopServiceConsumer();
    addNewTopServiceConsumer.setCallerName("CUCO");
    addNewTopServiceConsumer.setCallerSessionID("1");
    addNewTopServiceConsumer.setCallerSessionName("1");
    addNewTopServiceConsumer.setTimestamp(Calendar.getInstance());
    addNewTopServiceConsumer.setTouchpointName(TopServiceConsumer.TouchpointName.CS);
    return trackingDetails;
  }

  @Override
  public BRKAccountInfo getBRKAccountInfoForBAN(String banNumber) {
    String brkAccountnumber = getBRKAccountNumber(banNumber);
    if (StringUtils.isNotEmpty(brkAccountnumber)) {
      return getBRKAccountInfo(brkAccountnumber);
    }
    return null;
  }
}
