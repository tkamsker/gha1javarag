package at.a1ta.cuco.core.dao.esb;

import at.a1ta.cuco.core.shared.dto.EsbParty;
import at.a1telekom.eai.party.Party;

public interface EsbPartyDao {

  Party getParty(long partyId);
  
  EsbParty getESBParty(long partyId);

}
