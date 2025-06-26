package at.a1ta.cuco.core.service.impl;

import static org.junit.Assert.*;
import static org.mockito.Matchers.*;
import static org.mockito.Mockito.*;

import java.rmi.RemoteException;

import net.sf.ehcache.CacheManager;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.server.dto.EsbAccessParameter;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.shared.dto.VipStatus;
import at.mobilkom.eai.esb.EsbParam;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSUCHEPRIMBERECHT2;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSUCHEPRIMBERECHTAttr;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSUCHEPRIMBERECHTOutput2;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument;
import at.telekom.www.eai.wskums_s_wstokumssucheprimberecht.WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponseDocument;

import com.telekomaustriagroup.esb.kumscustomer.KUMSCustomerStub;

@RunWith(MockitoJUnitRunner.class)
public class KumsCustomerServiceImplTest {

  final static EsbAccessParameter STUB_PARAMS = new EsbAccessParameter("DEV", "ems1e.a1telekom.inside:17322", "ems1e.a1telekom.inside:17322", "ta-cuco", "ta", 60000l, "ta-dev", "http://esb-e.a1telekom.inside:8080/esb/si:ta-dev");

  private static final String PARTY_ID = "12345678";

  @Mock
  private SettingService settingService;

  @Mock
  private KUMSCustomerStub stub;

  private KumsCustomerServiceImpl customerService = new KumsCustomerServiceImpl();

  @Before
  public void setUp() {
    customerService.setStub(stub);
    customerService.setSettingService(settingService);
    CacheManager.getInstance().getCache("VIPCache").removeAll();
  }

  @Test
  public void webserviceError() throws RemoteException {
    when(stub.SuchePrimaer((WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument) any(), (EsbParam) isNull())).thenThrow(new RuntimeException());
    VipStatus vipStatus = customerService.getVipStatus(PARTY_ID);

    verify(stub).SuchePrimaer((WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument) any(), (EsbParam) isNull());
    assertEquals(VipStatus.State.UNKNOWN, vipStatus.getState());
  }

  @Test
  public void workingCallVip() throws RemoteException {
    when(stub.SuchePrimaer((WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument) any(), (EsbParam) isNull())).thenReturn(createResponseDocument());
    VipStatus vipStatus = customerService.getVipStatus(PARTY_ID);

    verify(stub).SuchePrimaer((WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument) any(), (EsbParam) isNull());
    assertEquals(VipStatus.State.VIP, vipStatus.getState());
  }

  @Test
  public void workingCallAndCacheHitVip() throws RemoteException {
    when(stub.SuchePrimaer((WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument) any(), (EsbParam) isNull())).thenReturn(createResponseDocument());
    VipStatus vipStatus = customerService.getVipStatus(PARTY_ID);
    customerService.getVipStatus(PARTY_ID);

    verify(stub, times(1)).SuchePrimaer((WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument) any(), (EsbParam) isNull());
    assertEquals(VipStatus.State.VIP, vipStatus.getState());
  }

  @Test
  public void workingCallNoVip() throws RemoteException {
    WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponseDocument response = createResponseDocument();
    response.getWSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponse().getWSKUMSSUCHEPRIMBERECHT2().getWSKUMSSUCHEPRIMBERECHTOutput().setSbText(null);
    when(stub.SuchePrimaer((WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument) any(), (EsbParam) isNull())).thenReturn(response);

    VipStatus vipStatus = customerService.getVipStatus(PARTY_ID);

    verify(stub).SuchePrimaer((WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument) any(), (EsbParam) isNull());
    assertEquals(VipStatus.State.NO_VIP, vipStatus.getState());
  }

  @Test
  public void workingCallFault() throws RemoteException {
    WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponseDocument response = createResponseDocument();
    response.getWSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponse().getWSKUMSSUCHEPRIMBERECHT2().getFault().setFaultString("irgendwas");
    when(stub.SuchePrimaer((WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument) any(), (EsbParam) isNull())).thenReturn(response);

    VipStatus vipStatus = customerService.getVipStatus(PARTY_ID);

    verify(stub).SuchePrimaer((WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromDocument) any(), (EsbParam) isNull());
    assertEquals(VipStatus.State.UNKNOWN, vipStatus.getState());
  }

  private WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponseDocument createResponseDocument() {
    WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponseDocument doc = WSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponseDocument.Factory.newInstance();
    WSKUMSSUCHEPRIMBERECHT2 response = doc.addNewWSKUMSSWSToKUMSSuchePrimBerechtWSKUMSSUCHEPRIMBERECHT2FromResponse().addNewWSKUMSSUCHEPRIMBERECHT2();
    response.addNewFault();

    WSKUMSSUCHEPRIMBERECHTOutput2 output = response.addNewWSKUMSSUCHEPRIMBERECHTOutput();
    WSKUMSSUCHEPRIMBERECHTAttr sbText = WSKUMSSUCHEPRIMBERECHTAttr.Factory.newInstance();
    sbText.setValue("1");
    output.setSbText(sbText);
    return doc;
  }
}
