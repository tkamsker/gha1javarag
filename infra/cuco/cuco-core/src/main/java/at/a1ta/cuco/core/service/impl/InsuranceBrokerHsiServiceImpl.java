package at.a1ta.cuco.core.service.impl;

import java.io.File;
import java.util.ArrayList;

import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.EnumTestDataCd;
import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.GetContractQuickInfoSoapMethodRequestDocument;
import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.GetContractQuickInfoSoapMethodRequestDocument.GetContractQuickInfoSoapMethodRequest;
import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.GetContractQuickInfoSoapMethodResponseDocument;
import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.GetContractQuickInfoSoapMethodResponseDocument.GetContractQuickInfoSoapMethodResponse;
import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.GetCostFreeClaimInfoSoapMethodRequestDocument;
import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.GetCostFreeClaimInfoSoapMethodRequestDocument.GetCostFreeClaimInfoSoapMethodRequest;
import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.GetCostFreeClaimInfoSoapMethodResponseDocument;
import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.GetCostFreeClaimInfoSoapMethodResponseDocument.GetCostFreeClaimInfoSoapMethodResponse;
import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.InsuranceContract;
import mergedhsi01soapv1controller.controller.core.remoteclient.standard.hsi01.hhi.lamie.b2b.eneon.RuntimeInformationFacade;

import org.apache.commons.io.FileUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.service.InsuranceBrokerHsiService;
import at.a1ta.cuco.core.shared.dto.InsuranceBrokerContractInfo;
import at.a1ta.cuco.core.shared.dto.InsuranceBrokerInfo;
import at.a1ta.cuco.core.shared.dto.product.SubscriptionNode;

import com.telekomaustriagroup.esb.insurancebrokerhsi.InsuranceBrokerHSIStub;

@Service
public class InsuranceBrokerHsiServiceImpl extends BaseEsbClient<InsuranceBrokerHSIStub> implements InsuranceBrokerHsiService {

  private static final Logger LOGGER = LoggerFactory.getLogger(InsuranceBrokerHsiServiceImpl.class);
  @Autowired
  private SettingService settingService;

  @Override
  public InsuranceBrokerInfo getCostFreeClaimInfo(SubscriptionNode subscriptionNode) {
    InsuranceBrokerInfo insuranceBrokerInfo = new InsuranceBrokerInfo(InsuranceBrokerInfo.LOADING);

    try {
      GetCostFreeClaimInfoSoapMethodRequestDocument getCostFreeClaimInfoRequestDocument = GetCostFreeClaimInfoSoapMethodRequestDocument.Factory.newInstance();
      GetCostFreeClaimInfoSoapMethodRequest request = GetCostFreeClaimInfoSoapMethodRequest.Factory.newInstance();
      RuntimeInformationFacade getRunTimeInformation = RuntimeInformationFacade.Factory.newInstance();
      getRunTimeInformation.setTestDataCd(EnumTestDataCd.PRODUCTIVE);
      request.addNewRequest().addNewIM().setBillingMSISDN(subscriptionNode.getSubscriptionCallNumber());
      request.getRequest().addNewIMM().setRuntimeInformation(getRunTimeInformation);
      getCostFreeClaimInfoRequestDocument.setGetCostFreeClaimInfoSoapMethodRequest(request);
      insuranceBrokerInfo.setStatus(InsuranceBrokerInfo.NOT_RECEIVED);

      GetCostFreeClaimInfoSoapMethodResponse response;
      GetCostFreeClaimInfoSoapMethodResponseDocument responseDoc;
      responseDoc = stub.GetCostFreeClaimInfo(getCostFreeClaimInfoRequestDocument, null);
      response = responseDoc.getGetCostFreeClaimInfoSoapMethodResponse();
      if (response != null && response.getGetCostFreeClaimInfoResult() != null && response.getGetCostFreeClaimInfoResult().getIM() != null) {
        insuranceBrokerInfo.setStatus(InsuranceBrokerInfo.LOADED);
        insuranceBrokerInfo.setMonthLeft(response.getGetCostFreeClaimInfoResult().getIM().getMonthLeft());
        insuranceBrokerInfo.setCostFreeClaimInd(response.getGetCostFreeClaimInfoResult().getIM().getCostFreeClaimInd());
      } else {
        insuranceBrokerInfo.setStatus(InsuranceBrokerInfo.NOT_RECEIVED);
      }
    } catch (Exception ex) {
      insuranceBrokerInfo.setStatus(InsuranceBrokerInfo.ERROR);
      LOGGER.error("Error while loading InsuranceBrokerHsi service", ex);
    }
    return insuranceBrokerInfo;
  }

  @Override
  public InsuranceBrokerInfo getHsiContractQuickInfo(SubscriptionNode subscriptionNode) {
    InsuranceBrokerInfo insuranceBrokerInfo = new InsuranceBrokerInfo(InsuranceBrokerInfo.LOADING);
    ArrayList<InsuranceBrokerContractInfo> insuranceBrokerContractInfo = new ArrayList<InsuranceBrokerContractInfo>();
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
      String mockResponseFileName = System.getProperty("catalina.base") + "//mocks//GetContractQuickInfoResponse.xml";
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
        if (response.getGetContractQuickInfoResult().getIM().getInsuranceContracts().getInsuranceContractArray().length != 0) {
          for (InsuranceContract insuranceContract : response.getGetContractQuickInfoResult().getIM().getInsuranceContracts().getInsuranceContractArray()) {
            insuranceBrokerContractInfo.add(new InsuranceBrokerContractInfo(
                insuranceContract.getContractInfo() != null ? (insuranceContract.getContractInfo().getMarketingContractTypeName() != null ? insuranceContract.getContractInfo()
                    .getMarketingContractTypeName() : "-") : "-", insuranceContract.getDevice() != null ? (insuranceContract.getDevice().getDeviceMarketingName() != null ? insuranceContract
                    .getDevice().getDeviceMarketingName() : "-") : "-", insuranceContract.getIMEI() != null ? insuranceContract.getIMEI() : "-"));
          }
          insuranceBrokerInfo.setContractInfo(insuranceBrokerContractInfo);
        } else {
          insuranceBrokerInfo.addToContractInfo(new InsuranceBrokerContractInfo("-", "-", "-"));
        }
      } else {
        insuranceBrokerInfo.setStatus(InsuranceBrokerInfo.NOT_RECEIVED);
      }
    } catch (Exception ex) {
      insuranceBrokerInfo.setStatus(InsuranceBrokerInfo.ERROR);
      LOGGER.error("Error while loading InsuranceBrokerHsi service", ex);
    }
    return insuranceBrokerInfo;
  }
}
