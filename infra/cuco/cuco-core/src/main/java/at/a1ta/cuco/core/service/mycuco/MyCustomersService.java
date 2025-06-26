package at.a1ta.cuco.core.service.mycuco;

import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.shared.dto.CustomerFilter;
import at.a1ta.cuco.core.shared.dto.Party;

public interface MyCustomersService {

  int loadNumberOfCustomersForSupportUser(String uUser);

  int loadNumberOfCustomersWithChurnForSupportUser(String uUser);

  int loadNumberOfCustomersWithIndexationForSupportUser(String uUser);

  int loadNumberOfCustomersWithFlashInfosForSupportUser(String uUser);

  int loadNumberOfCustomersWithVIPForSupportUser(String uUser);

  Map<String, Integer> loadNumberOfCustomersByTypeForSupportUser(String uUser);

  Map<String, Integer> loadNumberOfCustomersByWorthclassForSupportUser(String uUser);

  Map<String, Integer> loadNumberOfCustomersByTurnoverRangesForSupportUser(String uUser);

  SearchResult<Party> filterCustomersForSupportUser(CustomerFilter customerFilter, String username, boolean showNonCustomers);

  List<Party> filterCustomersForSupportUserUnlimited(CustomerFilter customerFilter, String uUser);

  int loadNumberOfCustomersWithVBMForSupportUser(String uUser);

  Map<String, List<String>> getFilters(List<String> filterNames, String userName);
}
