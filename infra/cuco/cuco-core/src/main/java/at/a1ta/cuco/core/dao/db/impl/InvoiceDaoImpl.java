package at.a1ta.cuco.core.dao.db.impl;

import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.InvoiceDao;
import at.a1ta.cuco.core.shared.dto.Invoice;

public class InvoiceDaoImpl extends AbstractDao implements InvoiceDao {

  @Override
  public List<Invoice> getByPartyIds(Collection<Long> partyIds) {
    Map<String, Object> params = new HashMap<String, Object>(2);
    params.put("partyIds", partyIds);
    return performListQuery("Invoice.getByPartyIds", params);
  }

  @Override
  public Invoice getById(long invoiceId) {
    return performObjectQuery("Invoice.getById", invoiceId);
  }
}
