package at.a1ta.cuco.core.service.impl;

import java.rmi.RemoteException;

import javax.xml.ws.WebServiceException;

import net.sf.ehcache.Cache;
import net.sf.ehcache.CacheManager;
import net.sf.ehcache.Element;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import wskums_s_wstokumskundebearbeiten_wskums_s_wstokumskundebearbeiten.EditCustomerType;
import wskums_s_wstokumskundebearbeiten_wskums_s_wstokumskundebearbeiten.WSKUMSKUNDEBEARBEITEN;
import wskums_s_wstokumskundebearbeiten_wskums_s_wstokumskundebearbeiten.WSKUMSKUNDEBEARBEITENInput;
import wskums_s_wstokumskundebearbeiten_wskums_s_wstokumskundebearbeiten.WSKUMSKUNDEBEARBEITENReturnCode;
import wskums_s_wstokumskundebearbeiten_wskums_s_wstokumskundebearbeiten.WSKUMSSWSToKUMSKundeBearbeitenWSKUMSKUNDEBEARBEITENFromDocument;
import wskums_s_wstokumskundebearbeiten_wskums_s_wstokumskundebearbeiten.WSKUMSSWSToKUMSKundeBearbeitenWSKUMSKUNDEBEARBEITENFromResponseDocument;
import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.service.KumsCustomerService;
import at.a1ta.cuco.core.shared.dto.KumsCustomerInfo;
import at.a1ta.cuco.core.shared.dto.VipStatus;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSHeader;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSUCHEPRIMBERECHT2;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSUCHEPRIMBERECHTInput2;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSUCHEPRIMBERECHTOutput2;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponseDocument;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponseType;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromType;

import com.telekomaustriagroup.esb.kumscustomer.KUMSCustomerStub;

@Service
public class KumsCustomerServiceImpl extends BaseEsbClient<KUMSCustomerStub> implements KumsCustomerService {

  private static final String EMPTY = "";

  private static final Logger logger = LoggerFactory.getLogger(KumsCustomerServiceImpl.class);

  private static final String SETTING_VIP_BEARBEITER = "vip.bearbeiter";

  private static final String SETTING_VIP_SOURCESYSTEM = "vip.sourcesystem";

  private static final String VERB = "Retrieve";

  private Cache cache = CacheManager.getInstance().getCache("VIPCache");

  private SettingService settingService;

  @Override
  public VipStatus getVipStatus(String customerId) {
    Element e = getVipStatusFromCache(customerId, cache);

    if (e != null) {
      logger.debug("VIPCache hit: " + customerId);
      return new VipStatus((Integer) e.getValue());
    }

    try {
      Integer intStatus = getVipStatusFromKums(customerId);
      cache.put(new Element(customerId, intStatus));
      logger.debug("VIPCache put: " + customerId + ":" + intStatus);

      return new VipStatus(intStatus);
    } catch (Exception ex) {
      logger.error("Error during getting VIP status for customer " + customerId);
      return new VipStatus();
    }
  }

  private Element getVipStatusFromCache(String customerId, Cache cache) {
    try {
      return cache.get(customerId);
    } catch (Throwable ex) {
      logger.error(ex.getMessage(), ex);
    }
    return null;
  }

  private Integer getVipStatusFromKums(String customerId) {
    WSKUMSSUCHEPRIMBERECHTOutput2 output = getCustomerData(customerId);

    if (output.getSbText() == null) {
      return null;
    }
    String vip = output.getSbText().getValue();

    return vip != null ? Integer.valueOf(vip) : null;
  }

  @Override
  public String getLastChangeDate(String customerId) {
    WSKUMSSUCHEPRIMBERECHTOutput2 output = getCustomerData(customerId);

    return output.getLetzteaend().getValue();
  }

  @Override
  public KumsCustomerInfo getKumsCustomerInfo(String customerId) {
    WSKUMSSUCHEPRIMBERECHTOutput2 output = getCustomerData(customerId);

    KumsCustomerInfo info = new KumsCustomerInfo();
    info.setLastChangeDate(output.getLetzteaend().getValue());
    String vip = output.getSbText().getValue();
    info.setVipStatus(vip != null ? Integer.valueOf(vip) : null);

    return info;
  }

  private WSKUMSSUCHEPRIMBERECHTOutput2 getCustomerData(String customerId) {
    try {
      WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument reqDocument = WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument.Factory.newInstance();
      WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromType request = reqDocument.addNewWSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2From();

      WSKUMSSUCHEPRIMBERECHT2 wskumssucheprimberecht2 = request.addNewWSKUMSSUCHEPRIMBERECHT2();
      wskumssucheprimberecht2.setVerb(VERB);
      WSHeader header = wskumssucheprimberecht2.addNewHeader();
      WSKUMSSUCHEPRIMBERECHTInput2 input = wskumssucheprimberecht2.addNewWSKUMSSUCHEPRIMBERECHTInput();

      header.setSourcesystem(settingService.getValue(SETTING_VIP_SOURCESYSTEM));
      input.setBearbeiter(settingService.getValue(SETTING_VIP_BEARBEITER));
      input.setPartnerid(customerId);

      WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponseDocument responseDoc;
      responseDoc = stub.SuchePrimaer(reqDocument, null);
      WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponseType response = responseDoc.getWSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponse();
      WSKUMSSUCHEPRIMBERECHTOutput2 output = response.getWSKUMSSUCHEPRIMBERECHT2().getWSKUMSSUCHEPRIMBERECHTOutput();

      if (response.getWSKUMSSUCHEPRIMBERECHT2().getFault().getFaultString() != null && !response.getWSKUMSSUCHEPRIMBERECHT2().getFault().getFaultString().isEmpty()) {
        String faultMessage = response.getWSKUMSSUCHEPRIMBERECHT2().getFault().getFaultString();
        throw new WebServiceException(faultMessage);
      }
      return output;
    } catch (RemoteException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  public void saveVipStatus(String customerId, String lastChangeDate, String vipStatus, String user) {
    try {
      WSKUMSSWSToKUMSKundeBearbeitenWSKUMSKUNDEBEARBEITENFromDocument reqDocument = prepareWSKUMSKUNDEBEARBEITENRequest(customerId, lastChangeDate, vipStatus, user);
      WSKUMSSWSToKUMSKundeBearbeitenWSKUMSKUNDEBEARBEITENFromResponseDocument responseDoc = stub.editCustomer(reqDocument, null);

      EditCustomerType response = responseDoc.getWSKUMSSWSToKUMSKundeBearbeitenWSKUMSKUNDEBEARBEITENFromResponse();
      WSKUMSKUNDEBEARBEITENReturnCode returnCode = response.getWSKUMSKUNDEBEARBEITEN().getWSKUMSKUNDEBEARBEITENReturnCode();
      if (returnCode != null && returnCode.getFEHLERTEXT() != null && !returnCode.getFEHLERTEXT().isEmpty()) {
        logger.error(returnCode.getFEHLERTEXT());
        throw new EsbException(returnCode.getFEHLERTEXT());
      }

    } catch (RemoteException e) {
      throw new EsbException(e);
    }
    cache.remove(customerId);
  }

  private WSKUMSSWSToKUMSKundeBearbeitenWSKUMSKUNDEBEARBEITENFromDocument prepareWSKUMSKUNDEBEARBEITENRequest(String customerId, String lastChangeDate, String vipStatus, String user) {
    WSKUMSSWSToKUMSKundeBearbeitenWSKUMSKUNDEBEARBEITENFromDocument reqDocument = WSKUMSSWSToKUMSKundeBearbeitenWSKUMSKUNDEBEARBEITENFromDocument.Factory.newInstance();
    EditCustomerType request = reqDocument.addNewWSKUMSSWSToKUMSKundeBearbeitenWSKUMSKUNDEBEARBEITENFrom();

    WSKUMSKUNDEBEARBEITEN wskumskundebearbeiten = request.addNewWSKUMSKUNDEBEARBEITEN();

    WSKUMSKUNDEBEARBEITENReturnCode addNewWSKUMSKUNDEBEARBEITENReturnCode = wskumskundebearbeiten.addNewWSKUMSKUNDEBEARBEITENReturnCode();
    addNewWSKUMSKUNDEBEARBEITENReturnCode.setRC(EMPTY);
    addNewWSKUMSKUNDEBEARBEITENReturnCode.setFEHLERNR(EMPTY);
    addNewWSKUMSKUNDEBEARBEITENReturnCode.setFEHLERTEXT(EMPTY);

    WSKUMSKUNDEBEARBEITENInput input = wskumskundebearbeiten.addNewWSKUMSKUNDEBEARBEITENInput();
    input.setBearbeiter(this.settingService.getValue(SETTING_VIP_BEARBEITER));
    input.setSystem(this.settingService.getValue(SETTING_VIP_SOURCESYSTEM));
    input.setKundennummer(customerId);
    input.setPvorname("N");
    input.setPgeburtsdatum("N");
    input.setLetzteaenderung(lastChangeDate);
    input.setSbText(vipStatus);
    input.setGz(user);
    return reqDocument;
  }

  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }
}
