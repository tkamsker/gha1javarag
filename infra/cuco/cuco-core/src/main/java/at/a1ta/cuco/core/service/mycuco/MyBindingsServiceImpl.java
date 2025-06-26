package at.a1ta.cuco.core.service.mycuco;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.joda.time.DateMidnight;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.dao.db.InventoryDao;
import at.a1ta.cuco.core.shared.dto.BindingsFilter;
import at.a1ta.cuco.core.shared.dto.CustomerBinding;

@Service
public class MyBindingsServiceImpl implements MyBindingsService {

  private InventoryDao inventoryDao;
  private SettingService settingsService;

  private static final String bindingTimerange1 = "mycuco.binding.timerange1.days";
  private static final String bindingTimerange2 = "mycuco.binding.timerange2.days";
  private static final String bindingTimerange3 = "mycuco.binding.timerange3.days";

  @Override
  public Map<String, Integer> getBindingsInfo(String uUser) {
    List<Date> list = inventoryDao.getExpiringContractDates(uUser, Integer.valueOf(settingsService.getIntValue(bindingTimerange3)));
    Map<String, Integer> map = getExpiringContractsDateMap(list);
    int expiredContracts = inventoryDao.getExpiredContracts(uUser);
    map.put("expiredContracts", expiredContracts);
    return map;
  }

  private Map<String, Integer> getExpiringContractsDateMap(List<Date> dates) {
    if (dates == null) {
      return new HashMap<String, Integer>();
    }
    DateMidnight dateTimeRange1 = new DateMidnight();
    DateMidnight dateTimeRange2 = new DateMidnight();
    dateTimeRange1 = dateTimeRange1.plusDays(settingsService.getIntValue(bindingTimerange1) + 1);
    dateTimeRange2 = dateTimeRange2.plusDays(settingsService.getIntValue(bindingTimerange2) + 1);
    int timeRange1Counter = 0;
    int timeRange2Counter = 0;

    for (Date bindingDate : dates) {
      if (bindingDate != null) {
        if (bindingDate.before(dateTimeRange1.toDate())) {
          timeRange1Counter++;
        } else if (bindingDate.before(dateTimeRange2.toDate())) {
          timeRange2Counter++;
        }
      }
    }
    HashMap<String, Integer> map = new HashMap<String, Integer>();
    map.put("timeRange1", timeRange1Counter);
    map.put("timeRange2", timeRange2Counter + timeRange1Counter);
    map.put("timeRange3", dates.size());
    return map;
  }

  @Override
  public SearchResult<CustomerBinding> filterBindings(BindingsFilter bindingsFilter, String uUser) {
    SearchResult<CustomerBinding> result = inventoryDao.filterBindingsInfo(bindingsFilter, uUser);
    for (CustomerBinding binding : result) {
      if (binding.getProductCategory() != null && binding.getProductCategory().contains("V") && binding.getAonCustomerNumber() == null) {
        binding.setAonCustomerNumber(inventoryDao.getAonNumber(binding.getPartyId() == null ? null : Long.valueOf(binding.getPartyId()), binding.getContractId(), binding.getProductNumber()));
      }
      if (binding.getProductDescription() == null) {
        binding.setProductDescription(inventoryDao.getProductName(binding.getPartyId() == null ? null : Long.valueOf(binding.getPartyId()), binding.getContractId(), binding.getAonCustomerNumber()));
      }
    }
    return result;
  }

  @Autowired
  public void setInventoryDao(InventoryDao inventoryDao) {
    this.inventoryDao = inventoryDao;
  }

  @Autowired
  public void setSettingsService(SettingService settingsService) {
    this.settingsService = settingsService;
  }
}
