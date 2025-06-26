package at.a1ta.cuco.core.service;

import a1.gdpr.webservice.Brand;
import a1.gdpr.webservice.UserType;
import at.a1ta.cuco.core.shared.dto.PartyDeclarationOfConsentInfo;

public interface PartyDeclarationOfConsentService {
  PartyDeclarationOfConsentInfo getCurrentDeclarationOfConsentForParty(final String partyID, final String userId, final Brand.Enum brand, final UserType.Enum userType);
}
