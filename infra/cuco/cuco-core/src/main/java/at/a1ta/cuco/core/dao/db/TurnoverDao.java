package at.a1ta.cuco.core.dao.db;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.Turnover;

public interface TurnoverDao {

  List<Turnover> getAllForParty(long partyId);

}
