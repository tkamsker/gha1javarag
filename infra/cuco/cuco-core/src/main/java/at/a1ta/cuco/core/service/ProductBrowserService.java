package at.a1ta.cuco.core.service;

import java.util.ArrayList;
import java.util.Map;

import at.a1ta.cuco.core.shared.dto.product.BaseNode;
import at.a1ta.cuco.core.shared.dto.product.ProductTree;
import at.a1ta.cuco.core.shared.dto.product.SubscriptionNode;
import at.a1ta.cuco.core.shared.dto.product.SubscriptionTree;
import at.a1telekom.eai.customerinventory.Product;
import at.a1telekom.eai.customerinventory.ProductPrice;

public interface ProductBrowserService {
  ProductTree getSubscriptionTree(ArrayList<Long> partyIds, String sessionId, boolean hasAuthorityToSeeCustomerInventoryXMLs);

  SubscriptionTree getSubscriptionTree(SubscriptionNode node, String sessionId, boolean hasAuthorityToSeeCustomerInventoryXMLs);

  Product[] getProductsForCustomerAccount(String ban, String partyId);

  void loadInventoryPricesForBAN(String ban, String partyId, Map<String, ProductPrice> socPriceMap);

  ArrayList<BaseNode> getSubscriptionsDataForCustomer(ArrayList<Long> partyIds, String sessionId, boolean hasAuthorityToSeeCustomerInventoryXMLs);
}
