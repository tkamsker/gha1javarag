package at.a1ta.cuco.core.service;

import at.a1ta.cuco.core.shared.dto.InsuranceBrokerInfo;
import at.a1ta.cuco.core.shared.dto.product.SubscriptionNode;

public interface InsuranceBrokerCpiService {
  InsuranceBrokerInfo getCpiContractQuickInfo(SubscriptionNode subscriptionNode);
}
