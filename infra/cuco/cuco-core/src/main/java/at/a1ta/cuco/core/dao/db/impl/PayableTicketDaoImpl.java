package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.PayableTicketDao;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PayableTicket;

public class PayableTicketDaoImpl extends AbstractDao implements PayableTicketDao {

  @Override
  public List<PayableTicket> getTicketsForParties(List<Party> parties) {
    Map<String, Object> m = new HashMap<String, Object>();
    m.put("parties", parties);
    return performListQuery("PayableTicket.getTicketsForParties", m);
  }

  @Override
  public void insertTicket(PayableTicket ticket) {
    executeInsert("PayableTicket.insert", ticket);
  }
}
