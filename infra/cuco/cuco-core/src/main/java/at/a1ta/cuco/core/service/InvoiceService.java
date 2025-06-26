package at.a1ta.cuco.core.service;

import java.util.ArrayList;
import java.util.LinkedHashMap;

import at.a1ta.cuco.core.shared.dto.ClearingAccount;
import at.a1ta.cuco.core.shared.dto.Invoice;

public interface InvoiceService {
  LinkedHashMap<Long, ArrayList<ClearingAccount>> getInvoiceData(ArrayList<Long> partyIds);

  String getMobileInvoiceDownloadLink(Invoice invoice, ClearingAccount clearingAccount);

  String getFixedLineInvoiceDownloadLink(Invoice invoice);

  Invoice getById(long invoiceId);
}
