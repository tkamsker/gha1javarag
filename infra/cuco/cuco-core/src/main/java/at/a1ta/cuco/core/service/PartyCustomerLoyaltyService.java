package at.a1ta.cuco.core.service;

import at.a1ta.cuco.core.shared.dto.PartyCustomerLoyaltyInfo;

public interface PartyCustomerLoyaltyService {
  PartyCustomerLoyaltyInfo getParty(final long partyId);
}
