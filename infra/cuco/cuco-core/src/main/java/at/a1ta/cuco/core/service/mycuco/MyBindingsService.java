package at.a1ta.cuco.core.service.mycuco;

import java.util.Map;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.shared.dto.BindingsFilter;
import at.a1ta.cuco.core.shared.dto.CustomerBinding;

public interface MyBindingsService {
  Map<String, Integer> getBindingsInfo(String uUser);

  SearchResult<CustomerBinding> filterBindings(BindingsFilter bindingsFilter, String uUser);
}
