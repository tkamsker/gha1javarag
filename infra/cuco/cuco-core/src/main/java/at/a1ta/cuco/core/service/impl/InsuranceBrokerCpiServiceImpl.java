package at.a1ta.cuco.core.service.impl;

import java.io.File;

import mergedcpi01soapv1controller.controller.core.remoteclient.standard.cpi01.hhi.lamie.b2b.eneon.EnumTestDataCd;
import mergedcpi01soapv1controller.controller.core.remoteclient.standard.cpi01.hhi.lamie.b2b.eneon.GetContractQuickInfoSoapMethodRequestDocument;
import mergedcpi01soapv1controller.controller.core.remoteclient.standard.cpi01.hhi.lamie.b2b.eneon.GetContractQuickInfoSoapMethodRequestDocument.GetContractQuickInfoSoapMethodRequest;
import mergedcpi01soapv1controller.controller.core.remoteclient.standard.cpi01.hhi.lamie.b2b.eneon.GetContractQuickInfoSoapMethodResponseDocument;
import mergedcpi01soapv1controller.controller.core.remoteclient.standard.cpi01.hhi.lamie.b2b.eneon.GetContractQuickInfoSoapMethodResponseDocument.GetContractQuickInfoSoapMethodResponse;
import mergedcpi01soapv1controller.controller.core.remoteclient.standard.cpi01.hhi.lamie.b2b.eneon.RuntimeInformationFacade;

import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.service.InsuranceBrokerCpiService;
import at.a1ta.cuco.core.shared.dto.InsuranceBrokerInfo;
import at.a1ta.cuco.core.shared.dto.product.SubscriptionNode;

import com.telekomaustriagroup.esb.insurancebrokercpi.InsuranceBrokerCPIStub;

@Service
public class InsuranceBrokerCpiServiceImpl extends BaseEsbClient<InsuranceBrokerCPIStub> implements InsuranceBrokerCpiService {

  private static final Logger LOGGER = LoggerFactory.getLogger(InsuranceBrokerCpiServiceImpl.class);
  @Autowired
  private SettingService settingService;

  @Override
  public InsuranceBrokerInfo getCpiContractQuickInfo(SubscriptionNode subscriptionNode) {
    InsuranceBrokerInfo insuranceBrokerInfo = new InsuranceBrokerInfo(InsuranceBrokerInfo.LOADING);

    try {
      GetContractQuickInfoSoapMethodRequestDocument getContractQuickInfoRequestDocument = GetContractQuickInfoSoapMethodRequestDocument.Factory.newInstance();
      GetContractQuickInfoSoapMethodRequest request = GetContractQuickInfoSoapMethodRequest.Factory.newInstance();
      RuntimeInformationFacade getRunTimeInformation = RuntimeInformationFacade.Factory.newInstance();
      getRunTimeInformation.setTestDataCd(EnumTestDataCd.PRODUCTIVE);
      request.addNewRequest().addNewIM().setBillingMSISDN(subscriptionNode.getSubscriptionCallNumber());
      request.getRequest().addNewIMM().setRuntimeInformation(getRunTimeInformation);
      getContractQuickInfoRequestDocument.setGetContractQuickInfoSoapMethodRequest(request);
      insuranceBrokerInfo.setStatus(InsuranceBrokerInfo.NOT_RECEIVED);

      GetContractQuickInfoSoapMethodResponse response;
      GetContractQuickInfoSoapMethodResponseDocument responseDoc;
      String mockResponseFileName = System.getProperty("catalina.base") + "//mocks//GetContractQuickInfoResponseCpi.xml";
      if (settingService.getBooleanValue("testModeActive", false) && new File(mockResponseFileName).exists()) {
        response = GetContractQuickInfoSoapMethodResponseDocument.Factory.parse(FileUtils.readFileToString(new File(mockResponseFileName))).getGetContractQuickInfoSoapMethodResponse();
      } else {
        responseDoc = stub.GetContractQuickInfo(getContractQuickInfoRequestDocument, null);
        response = responseDoc.getGetContractQuickInfoSoapMethodResponse();
      }
      if (response != null && response.getGetContractQuickInfoResult() != null && response.getGetContractQuickInfoResult().getIM() != null) {
        insuranceBrokerInfo.setStatus(InsuranceBrokerInfo.LOADED);
        insuranceBrokerInfo.setContractInd(response.getGetContractQuickInfoResult().getIM().getCoverage() != null ? response.getGetContractQuickInfoResult().getIM().getCoverage().getContractInd()
            : false);
        insuranceBrokerInfo.setContractTypeEligible(response.getGetContractQuickInfoResult().getIM().getCoverage() != null ? response.getGetContractQuickInfoResult().getIM().getCoverage()
            .getContractTypeEligible() : false);
        insuranceBrokerInfo.setMarketingContractTypeName(response.getGetContractQuickInfoResult().getIM().getContractInfo() != null ? (response.getGetContractQuickInfoResult().getIM()
            .getContractInfo().getMarketingContractTypeName() != null ? response.getGetContractQuickInfoResult().getIM().getContractInfo().getMarketingContractTypeName() : "-") : "-");
        insuranceBrokerInfo.setDeviceMarketingName("-");
        insuranceBrokerInfo.setImei("-");
      } else {
        insuranceBrokerInfo.setStatus(InsuranceBrokerInfo.NOT_RECEIVED);
      }
    } catch (Exception ex) {
      insuranceBrokerInfo.setStatus(InsuranceBrokerInfo.ERROR);
      LOGGER.error("Error while loading InsuranceBrokerCpi service", ex);
    }
    return insuranceBrokerInfo;
  }
}
