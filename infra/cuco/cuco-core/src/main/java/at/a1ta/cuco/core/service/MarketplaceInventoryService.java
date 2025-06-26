package at.a1ta.cuco.core.service;

import at.a1ta.cuco.core.shared.dto.product.LocationNode;

public interface MarketplaceInventoryService {

  LocationNode getMarketplaceAccountsWithSubscriptionsForParty(long partyId);

}
