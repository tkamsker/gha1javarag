package at.a1ta.cuco.core.dao.db;

import java.util.Date;
import java.util.List;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.shared.dto.BindingsFilter;
import at.a1ta.cuco.core.shared.dto.CustomerBinding;

public interface InventoryDao {

  // List<Inventory> listInventory4Customers(List<Long> customerIds, List<Long> contractIds, ProductDetailFilter productFilter);

  List<Date> getExpiringContractDates(String uUser, int maxTimeRange);

  int getExpiredContracts(String uUser);

  String getProductName(Long customerId, Long contractId, Long aonNumber);

  SearchResult<CustomerBinding> filterBindingsInfo(BindingsFilter bindingsFilter, String uUser);

  Long getAonNumber(Long customerId, Long contractId, String productNumber);
}
