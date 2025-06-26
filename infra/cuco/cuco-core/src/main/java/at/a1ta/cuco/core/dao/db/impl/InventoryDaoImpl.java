package at.a1ta.cuco.core.dao.db.impl;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.lang.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.dao.db.InventoryDao;
import at.a1ta.cuco.core.shared.dto.BindingsFilter;
import at.a1ta.cuco.core.shared.dto.CustomerBinding;

public class InventoryDaoImpl extends AbstractDao implements InventoryDao {

  private static final String SEARCH_RESULT_LIMIT_SETTING_KEY = "mycuco.table.searchresult.limit";
  private static final String BINDING_TIMERANGE_1 = "mycuco.binding.timerange1.days";
  private static final String BINDING_TIMERANGE_2 = "mycuco.binding.timerange2.days";
  private static final String BINDING_TIMERANGE_3 = "mycuco.binding.timerange3.days";

  private SettingService settingService;

  // @Override
  // public List<Inventory> listInventory4Customers(List<Long> customerIds, List<Long> contractIds, ProductDetailFilter productFilter) {
  // Map<String, Object> params = new HashMap<String, Object>();
  // params.put("customerIds", customerIds);
  // if (contractIds != null) {
  // params.put("contractIds", contractIds);
  // }
  // params.put("filter", productFilter);
  // if (productFilter.getSecretLevel() != null) {
  // params.put(productFilter.getSecretLevel() ? "secretNumber" : "noSecretNumber", true);
  // }
  //
  // return performListQuery("Inventory.GetInventory4Customer", params);
  // }

  @Override
  public List<Date> getExpiringContractDates(String uUser, int maxTimeRange) {
    HashMap<String, Object> paramMap = new HashMap<String, Object>();

    paramMap.put("uUser", uUser.toLowerCase());
    paramMap.put("maxTimeRange", maxTimeRange);

    return performListQuery("Inventory.getExpiringContractDatesForNextMonth", paramMap);
  }

  @Override
  public String getProductName(Long customerId, Long contractId, Long aonNumber) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("customerId", customerId);
    params.put("contractId", contractId);
    params.put("aonNumber", aonNumber);
    List<String> names = performListQuery("Inventory.getProductName", params);
    if (names.size() > 0) {
      return names.get(0);
    }
    return null;
  }

  @Override
  public Long getAonNumber(Long customerId, Long contractId, String productNumber) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("customerId", customerId);
    params.put("contractId", contractId);
    params.put("productNumber", productNumber);
    List<Long> aonNumbers = performListQuery("Inventory.getAonNumber", params);
    if (aonNumbers.size() > 0) {
      return aonNumbers.get(0);
    }
    return null;
  }

  @Override
  @SuppressWarnings("unchecked")
  public SearchResult<CustomerBinding> filterBindingsInfo(BindingsFilter bindingsFilter, String uUser) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("uUser", uUser.toLowerCase());

    if (bindingsFilter != null) {
      if (bindingsFilter.getContractEnd() != null) {
        if (bindingsFilter.getContractEnd() == BindingsFilter.Contract.TIMERANGE_1) {
          params.put("expireInDays", getIntSetting(BINDING_TIMERANGE_1));
        } else if (bindingsFilter.getContractEnd() == BindingsFilter.Contract.TIMERANGE_2) {
          params.put("expireInDays", getIntSetting(BINDING_TIMERANGE_2));
        } else if (bindingsFilter.getContractEnd() == BindingsFilter.Contract.TIMERANGE_3) {
          params.put("expireInDays", getIntSetting(BINDING_TIMERANGE_3));
        } else if (bindingsFilter.getContractEnd() == BindingsFilter.Contract.LARGER_TIMERANGE_3) {
          params.put("expireInFuture", getIntSetting(BINDING_TIMERANGE_3));
        } else {
          params.put("contractFilter", bindingsFilter.getContractEnd().name());
        }
      }
      if (StringUtils.isNotBlank(bindingsFilter.getPartyId())) {
        params.put("partyId", bindingsFilter.getPartyId());
      }
      if (StringUtils.isNotBlank(bindingsFilter.getProductDescription())) {
        params.put("productDescription", StringUtils.trimToEmpty(bindingsFilter.getProductDescription()));
      }
      params.put("contractStart", bindingsFilter.getContractStart());
    }

    return (SearchResult<CustomerBinding>) performLimitedListQuery("Inventory.filterBindingsInfo", params, settingService.getIntValue(SEARCH_RESULT_LIMIT_SETTING_KEY));
  }

  private int getIntSetting(String key) {
    return settingService.getIntValue(key);
  }

  @Override
  public int getExpiredContracts(String uUser) {
    return (Integer) performObjectQuery("Inventory.getExpiredContracts", uUser);
  }

  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }
}
