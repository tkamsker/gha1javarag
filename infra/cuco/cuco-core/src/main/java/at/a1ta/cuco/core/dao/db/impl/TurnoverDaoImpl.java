package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.TurnoverDao;
import at.a1ta.cuco.core.shared.dto.Turnover;

public class TurnoverDaoImpl extends AbstractDao implements TurnoverDao {

  @Override
  public List<Turnover> getAllForParty(long partyId) {
    return performListQuery("Turnover.get", partyId);
  }
}
