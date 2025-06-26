package at.a1ta.cuco.core.service;

import static org.junit.Assert.assertEquals;
import static org.mockito.Matchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.List;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.dao.db.InvoiceDao;
import at.a1ta.cuco.core.service.impl.InvoiceServiceImpl;
import at.a1ta.cuco.core.shared.dto.ClearingAccount;
import at.a1ta.cuco.core.shared.dto.Invoice;
import at.mobilkom.eai.esb.EsbParam;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSFault;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5IXOSAddress;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5IXOSAddressRes;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromDocument;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponseDocument;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponseDocument.WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponse;

import com.telekomaustriagroup.esb.sap5billinginformation.SAP5BillingInformationStub;

@RunWith(MockitoJUnitRunner.class)
public class InvoiceServiceTest {
  @Mock
  private SAP5BillingInformationStub stub;
  @Mock
  private InvoiceDao invoiceDao;
  @Mock
  private SettingService settingService;

  private InvoiceServiceImpl service = new InvoiceServiceImpl();

  @Before
  public void setup() throws Exception {
    service.setStub(stub);
    service.setInvoiceDao(invoiceDao);
    service.setSettingService(settingService);

    when(settingService.getValue("interfaces_ws_WSSAP5_S_RetrieveIXOSAddress_verb")).thenReturn("verb");
    when(settingService.getValue("interfaces_ws_WSSAP5_S_RetrieveIXOSAddress_sourcesystem")).thenReturn("sourcesystem");
    when(settingService.getValue("interfaces_ws_WSSAP5_S_RetrieveIXOSAddress_documenttype")).thenReturn("doc");
    when(settingService.getValue("ext_link_invoiceArchive")).thenReturn("http://arcdb.pta.at:8080/archive?get&docId=[documentId]&contRep=[repositoryId]&pVersion=0045");
  }

  @Test
  public void testInvoiceData() {
    ArrayList<Long> partyIds = new ArrayList<Long>();
    partyIds.add(100L);
    partyIds.add(200L);

    ClearingAccountService clearingAccountService = mock(ClearingAccountService.class);
    service.setClearingAccountService(clearingAccountService);

    final List<ClearingAccount> clearingAccountsResults = new ArrayList<ClearingAccount>();
    final ClearingAccount account1 = new ClearingAccount(1L);
    account1.setPartyId(100L);
    final ClearingAccount account2 = new ClearingAccount(2L);
    account2.setPartyId(200L);

    clearingAccountsResults.add(account1);
    clearingAccountsResults.add(account2);

    when(clearingAccountService.getByPartyIds(partyIds)).thenReturn(clearingAccountsResults);

    service.getInvoiceData(partyIds);

    verify(invoiceDao, times(1)).getByPartyIds(partyIds);
  }

  @Test
  public void testGetDownloadLink() throws Exception {
    // Mocking the ESB service response
    WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponse response = WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponse.Factory.newInstance();
    response.setWSSAP5IXOSAddress(WSSAP5IXOSAddress.Factory.newInstance());
    response.getWSSAP5IXOSAddress().setFault(WSFault.Factory.newInstance());
    response.getWSSAP5IXOSAddress().getFault().setFaultString("");
    response.getWSSAP5IXOSAddress().setResponse(WSSAP5IXOSAddressRes.Factory.newInstance());
    response.getWSSAP5IXOSAddress().getResponse().setArchiveID("_archiveID_");
    response.getWSSAP5IXOSAddress().getResponse().setDocumentID("_documentID_");

    WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponseDocument responseDocument = mock(WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponseDocument.class);
    when(stub.retrieveIXOSAddress(any(WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromDocument.class), any(EsbParam.class))).thenReturn(responseDocument);
    when(responseDocument.getWSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponse()).thenReturn(response);

    String urlAfterExpected = "http://arcdb.pta.at:8080/archive?get&docId=_documentID_&contRep=_archiveID_&pVersion=0045";

    Invoice invoice = new Invoice();
    invoice.setInvoiceId(123456l);
    String urlAfter = service.getFixedLineInvoiceDownloadLink(invoice);
    assertEquals(urlAfterExpected, urlAfter);
  }
}
