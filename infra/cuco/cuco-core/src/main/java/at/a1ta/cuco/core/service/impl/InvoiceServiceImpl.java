package at.a1ta.cuco.core.service.impl;

import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;

import javax.xml.ws.WebServiceException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.dao.db.InvoiceDao;
import at.a1ta.cuco.core.service.ClearingAccountService;
import at.a1ta.cuco.core.service.InvoiceService;
import at.a1ta.cuco.core.shared.dto.ClearingAccount;
import at.a1ta.cuco.core.shared.dto.Invoice;
import at.a1ta.cuco.core.shared.dto.Invoice.InvoiceDateComparator;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSFault;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSHeader;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5IXOSAddress;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5IXOSAddressReq;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5IXOSAddressRes;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromDocument;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromDocument.WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFrom;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponseDocument;
import at.telekom.www.eai.wssap5_s_retrieveixosaddress.WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponseDocument.WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponse;

import com.telekomaustriagroup.esb.sap5billinginformation.SAP5BillingInformationStub;

@Service
public class InvoiceServiceImpl extends BaseEsbClient<SAP5BillingInformationStub> implements InvoiceService {
  private static InvoiceDateComparator invoiceDateComparator = new InvoiceDateComparator();
  private static Logger logger = LoggerFactory.getLogger(InvoiceServiceImpl.class);
  private static String EMPTY = "";
  private static String DOCUMENT_ID_PLACEHOLDER = "\\[documentId\\]";
  private static String REPOSITORY_ID_PLACEHOLDER = "\\[repositoryId\\]";
  private InvoiceDao invoiceDao;
  private SettingService settingService;
  private ClearingAccountService clearingAccountService;

  @Override
  public LinkedHashMap<Long, ArrayList<ClearingAccount>> getInvoiceData(ArrayList<Long> partyIds) {
    LinkedHashMap<Long, ClearingAccount> clearingAccounts = getClearingAccountsMap(partyIds);
    fillClearingAccountsWithInvoices(clearingAccounts, partyIds);
    return createPartyIdToClearingAccountsMap(partyIds, clearingAccounts.values());
  }

  private LinkedHashMap<Long, ArrayList<ClearingAccount>> createPartyIdToClearingAccountsMap(ArrayList<Long> partyIds, Collection<ClearingAccount> clearingAccounts) {
    LinkedHashMap<Long, ArrayList<ClearingAccount>> partyIdToClearingAccountsMap = new LinkedHashMap<Long, ArrayList<ClearingAccount>>(8);
    for (Long partyId : partyIds) {
      ArrayList<ClearingAccount> clearingAccountsForParty = getClearingAccountsForParty(partyId, clearingAccounts);
      partyIdToClearingAccountsMap.put(partyId, clearingAccountsForParty);
    }
    return partyIdToClearingAccountsMap;
  }

  private void fillClearingAccountsWithInvoices(LinkedHashMap<Long, ClearingAccount> clearingAccountsMap, ArrayList<Long> partyIds) {
    if (!clearingAccountsMap.isEmpty()) {
      ArrayList<Invoice> invoices = getInvoices(partyIds);
      linkInvoicesToClearingAccounts(invoices, clearingAccountsMap);
    }
  }

  private void linkInvoicesToClearingAccounts(ArrayList<Invoice> invoices, LinkedHashMap<Long, ClearingAccount> clearingAccountsMap) {
    for (Invoice invoice : invoices) {
      ClearingAccount clearingAccount = clearingAccountsMap.get(invoice.getClearingAccountNumber());
      if (clearingAccount != null) {
        invoice.setMobile(clearingAccount.isMobileAccount());
        clearingAccount.addInvoices(invoice);
      } else {
        logger.warn("No clearingAccount for ClearingAccountNumber: " + invoice.getClearingAccountNumber());
      }
    }
  }

  private LinkedHashMap<Long, ClearingAccount> getClearingAccountsMap(ArrayList<Long> partyIds) {
    ArrayList<ClearingAccount> clearingAccounts = getClearingAccounts(partyIds);
    LinkedHashMap<Long, ClearingAccount> clearingAccountsMap = new LinkedHashMap<Long, ClearingAccount>(clearingAccounts.size() * 2);
    for (ClearingAccount account : clearingAccounts) {
      clearingAccountsMap.put(account.getAccountNumber(), account);
    }
    return clearingAccountsMap;
  }

  private ArrayList<ClearingAccount> getClearingAccountsForParty(Long partyId, Collection<ClearingAccount> allClearingAccounts) {
    ArrayList<ClearingAccount> clearingAccountsForParty = new ArrayList<ClearingAccount>();
    ArrayList<Invoice> allInvoicesForParty = new ArrayList<Invoice>();

    for (ClearingAccount account : allClearingAccounts) {
      if (account.getPartyId().equals(partyId)) {
        clearingAccountsForParty.add(account);
        if (account.hasInvoices()) {
          allInvoicesForParty.addAll(account.getInvoices());
        }
      }
    }

    Collections.sort(allInvoicesForParty, invoiceDateComparator);

    if (clearingAccountsForParty.size() > 1) {
      clearingAccountsForParty.add(0, createVirtualClearingAccount(clearingAccountsForParty, allInvoicesForParty));
    }

    return clearingAccountsForParty;
  }

  private ClearingAccount createVirtualClearingAccount(ArrayList<ClearingAccount> allClearingAccounts, ArrayList<Invoice> invoicesToAdd) {
    ClearingAccount virtualClearingAccount = new ClearingAccount();
    virtualClearingAccount.setInvoices(invoicesToAdd);

    for (ClearingAccount account : allClearingAccounts) {
      if (account.isMobileAccount()) {
        virtualClearingAccount.setVirtualClearingAccountMobile(true);
      }
      if (account.isFixedLineAccount()) {
        virtualClearingAccount.setVirtualClearingAccountFixedLine(true);
      }
    }

    return virtualClearingAccount;
  }

  private ArrayList<Invoice> getInvoices(Collection<Long> partyIds) {
    return new ArrayList<Invoice>(invoiceDao.getByPartyIds(partyIds));
  }

  private ArrayList<ClearingAccount> getClearingAccounts(ArrayList<Long> partyIds) {
    return new ArrayList<ClearingAccount>(clearingAccountService.getByPartyIds(partyIds));
  }

  @Override
  public String getMobileInvoiceDownloadLink(Invoice invoice, ClearingAccount clearingAccount) {
    String urlPattern = settingService.getValue("ext_link_invoiceArchive_mobile");

    String url = urlPattern.replaceFirst("\\[ban\\]", Long.toString(clearingAccount.getBan()));
    url = url.replaceFirst("\\[ben\\]", Long.toString(clearingAccount.getBen()));
    url = url.replaceFirst("\\[billseqnr\\]", Long.toString(invoice.getInvoiceRunId()));

    return url;
  }

  @Override
  public String getFixedLineInvoiceDownloadLink(Invoice invoice) {
    // Get service parameters from config
    String verb = settingService.getValue("interfaces_ws_WSSAP5_S_RetrieveIXOSAddress_verb");
    String sourcesystem = settingService.getValue("interfaces_ws_WSSAP5_S_RetrieveIXOSAddress_sourcesystem");
    String documenttype = settingService.getValue("interfaces_ws_WSSAP5_S_RetrieveIXOSAddress_documenttype");
    String redirectUrl = settingService.getValue("ext_link_invoiceArchive");

    WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromDocument reqDoc = WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromDocument.Factory.newInstance();
    WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFrom request = reqDoc.addNewWSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFrom();

    try {
      // configure request
      WSSAP5IXOSAddress adr = WSSAP5IXOSAddress.Factory.newInstance();
      adr.setVerb(verb);

      WSHeader header = WSHeader.Factory.newInstance();
      header.setSourcesystem(sourcesystem);
      header.setTransaktion(EMPTY);
      header.setAPIArt(EMPTY);
      header.setParameter(EMPTY);
      adr.setHeader(header);

      WSSAP5IXOSAddressReq adrReq = WSSAP5IXOSAddressReq.Factory.newInstance();
      adrReq.setDocumentType(documenttype);
      adrReq.setInvoiceNumber("" + invoice.getInvoiceId());
      adr.setRequest(adrReq);

      WSSAP5IXOSAddressRes adrRes = WSSAP5IXOSAddressRes.Factory.newInstance();
      adrRes.setArchiveID(EMPTY);
      adrRes.setDocumentID(EMPTY);
      adr.setResponse(adrRes);

      WSFault fault = WSFault.Factory.newInstance();
      fault.setFaultActor(EMPTY);
      fault.setFaultCode(EMPTY);
      fault.setFaultSeverity(EMPTY);
      fault.setFaultString(EMPTY);
      fault.setFaultType(EMPTY);
      adr.setFault(fault);

      request.setWSSAP5IXOSAddress(adr);
      reqDoc.setWSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFrom(request);

      // Invoke Service
      WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponseDocument responseDoc;
      responseDoc = stub.retrieveIXOSAddress(reqDoc, null);
      WSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponse response = responseDoc.getWSSAP5SRetrieveIXOSAddressWSSAP5IXOSAddressFromResponse();

      // check the result for fault codes
      if (response.getWSSAP5IXOSAddress().getFault().getFaultString() != null && EMPTY.equals(response.getWSSAP5IXOSAddress().getFault().getFaultString())) {
        String repositoryId = response.getWSSAP5IXOSAddress().getResponse().getArchiveID();
        String documentId = response.getWSSAP5IXOSAddress().getResponse().getDocumentID();
        if (repositoryId != null && documentId != null) {
          String downloadLink = redirectUrl.replaceAll(DOCUMENT_ID_PLACEHOLDER, documentId);
          downloadLink = downloadLink.replaceAll(REPOSITORY_ID_PLACEHOLDER, repositoryId);
          return downloadLink;
        }
        throw new WebServiceException("Empty repositoryId, docuentId received");
      }
      throw new RuntimeException(response.getWSSAP5IXOSAddress().getFault().getFaultString());
    } catch (RemoteException e) {
      throw new WebServiceException(e);
    }
  }

  @Override
  public Invoice getById(long invoiceId) {
    return invoiceDao.getById(invoiceId);
  }

  @Autowired
  public void setClearingAccountService(ClearingAccountService clearingAccountService) {
    this.clearingAccountService = clearingAccountService;
  }

  @Autowired
  public void setInvoiceDao(InvoiceDao invoiceDao) {
    this.invoiceDao = invoiceDao;
  }

  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }
}
