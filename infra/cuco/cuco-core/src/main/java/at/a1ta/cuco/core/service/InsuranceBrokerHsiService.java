package at.a1ta.cuco.core.service;

import at.a1ta.cuco.core.shared.dto.InsuranceBrokerInfo;
import at.a1ta.cuco.core.shared.dto.product.SubscriptionNode;

public interface InsuranceBrokerHsiService {
  InsuranceBrokerInfo getCostFreeClaimInfo(SubscriptionNode subscriptionNode);

  InsuranceBrokerInfo getHsiContractQuickInfo(SubscriptionNode subscriptionNode);
}
