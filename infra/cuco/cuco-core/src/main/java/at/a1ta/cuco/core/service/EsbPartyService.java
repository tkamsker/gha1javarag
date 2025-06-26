package at.a1ta.cuco.core.service;

import at.a1ta.cuco.core.shared.dto.EsbParty;
import at.a1telekom.eai.party.Party;

public interface EsbPartyService {

  EsbParty getESBParty(long partyId);
  
  Party getParty(long partyId);

}
