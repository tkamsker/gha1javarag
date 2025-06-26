package at.a1ta.cuco.core.service;

import at.a1ta.cuco.core.shared.dto.PartyProfileInfo;

public interface PartyProfileService {
  PartyProfileInfo getParty(final long partyId);

  String getBvkUser(String bvkUserId);

  String getOneTVUser(String oneTVUserId);

}
