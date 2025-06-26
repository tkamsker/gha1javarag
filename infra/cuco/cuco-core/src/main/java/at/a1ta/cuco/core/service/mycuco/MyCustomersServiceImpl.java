package at.a1ta.cuco.core.service.mycuco;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.dao.db.PhoneNumberDao;
import at.a1ta.cuco.core.dao.db.VbmProductsDao;
import at.a1ta.cuco.core.shared.dto.CustomerFilter;
import at.a1ta.cuco.core.shared.dto.CustomerFilter.Churn;
import at.a1ta.cuco.core.shared.dto.CustomerFilter.FlashInfo;
import at.a1ta.cuco.core.shared.dto.CustomerFilter.Indexation;
import at.a1ta.cuco.core.shared.dto.CustomerFilter.Vip;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartySearch;
import at.a1ta.cuco.core.shared.dto.Tupel;
import at.a1ta.cuco.core.shared.dto.nbo.VBMProductDetails;
import at.a1ta.cuco.core.shared.model.DualSegment;
import at.a1ta.cuco.core.shared.model.PartyModelFactory;

@Service
public class MyCustomersServiceImpl implements MyCustomersService {

  private PartyDao partyDao;

  private SettingService settingService;

  private PhoneNumberDao phoneNumberDao;

  private VbmProductsDao vbmProductsDao;

  private static final Comparator<BigDecimal> customerTypeIdComparator = new Comparator<BigDecimal>() {

    @Override
    public int compare(BigDecimal o1, BigDecimal o2) {
      if (o1 == null) {
        return 1;
      }
      if (o2 == null) {
        return -1;
      }
      return o1.compareTo(o2);
    }

  };

  private static final Comparator<String> worthclassComparator = new Comparator<String>() {

    @Override
    public int compare(String o1, String o2) {
      return getCustomerWorthclassValue(o1).compareTo(getCustomerWorthclassValue(o2));
    }

    private Integer getCustomerWorthclassValue(String worthclassValue) {
      if ("NEU".equalsIgnoreCase(worthclassValue)) {
        return 0;
      }
      if ("GOLD".equalsIgnoreCase(worthclassValue)) {
        return 1;
      }
      if ("SILBER".equalsIgnoreCase(worthclassValue)) {
        return 2;
      }
      if ("BRONZE".equalsIgnoreCase(worthclassValue)) {
        return 3;
      }
      if ("BLEI".equalsIgnoreCase(worthclassValue)) {
        return 4;
      }
      return 5;
    }

  };

  @Override
  public int loadNumberOfCustomersForSupportUser(String uUser) {
    return partyDao.loadNumberOfCustomersForSupportUser(uUser);
  }

  @Override
  public int loadNumberOfCustomersWithChurnForSupportUser(String uUser) {
    return partyDao.loadNumberOfCustomersWithChurnForSupportUser(uUser) + phoneNumberDao.loadNumberOfCustomersWithMobileChurnForSupportUser(uUser);
  }

  @Override
  public int loadNumberOfCustomersWithIndexationForSupportUser(String uUser) {
    return partyDao.loadNumberOfCustomersWithIndexationForSupportUser(uUser);
  }

  @Override
  public int loadNumberOfCustomersWithFlashInfosForSupportUser(String uUser) {
    return partyDao.loadNumberOfCustomersWithFlashInfosForSupportUser(uUser);
  }

  @Override
  public int loadNumberOfCustomersWithVIPForSupportUser(String uUser) {
    return partyDao.loadNumberOfCustomersWithVIPForSupportUser(uUser);
  }

  @Override
  public Map<String, Integer> loadNumberOfCustomersByTypeForSupportUser(String uUser) {
    Map<BigDecimal, BigDecimal> partyTypeCounts = new TreeMap<BigDecimal, BigDecimal>(customerTypeIdComparator);
    partyTypeCounts.putAll(partyDao.loadNumberOfCustomersByTypeForSupportUser(uUser));
    Map<String, Integer> result = new LinkedHashMap<String, Integer>(partyTypeCounts.size() * 2);
    for (Entry<BigDecimal, BigDecimal> entry : partyTypeCounts.entrySet()) {
      String titleString = PartyModelFactory.getTitle(entry.getKey() != null ? entry.getKey().intValue() : -1);
      result.put(titleString, entry.getValue().intValue());
    }
    return result;
  }

  @Override
  public Map<String, Integer> loadNumberOfCustomersByWorthclassForSupportUser(String uUser) {
    Map<String, BigDecimal> partyWorthCounts = partyDao.loadNumberOfCustomersByWorthclassForSupportUser(uUser);
    Map<String, Integer> result = new TreeMap<String, Integer>(worthclassComparator);
    for (Entry<String, BigDecimal> entry : partyWorthCounts.entrySet()) {
      if (entry.getKey() != null && !entry.getKey().equals("UNKNOWN")) {
        result.put(entry.getKey(), entry.getValue().intValue());
      } else {
        Integer value = result.get("Keine Angabe");
        if (value != null) {
          value += entry.getValue().intValue();
        } else {
          value = entry.getValue().intValue();
        }
        result.put("Keine Angabe", value);
      }
    }
    return result;
  }

  @Override
  public Map<String, Integer> loadNumberOfCustomersByTurnoverRangesForSupportUser(String uUser) {
    List<BigDecimal> ranges = loadRanges(uUser);
    List<Tupel<Long, BigDecimal>> turnovers = partyDao.loadNumberOfCustomersTurnoverForSupportUser(uUser);

    Map<String, Integer> result = new LinkedHashMap<String, Integer>(ranges.size() * 2);
    BigDecimal min = BigDecimal.ZERO;
    int numberOfCustomersWithTurnOver = 0;
    for (BigDecimal range : ranges) {
      if (range.compareTo(min) < 0) {
        throw new IllegalArgumentException("invalid ranges");
      }

      int numberOfCustomers = getNumbersForRange(turnovers, min, range);
      if (numberOfCustomers > 0) {
        numberOfCustomersWithTurnOver += numberOfCustomers;
        result.put(min + " - " + range + "\u20AC", numberOfCustomers);
      }
      min = range;
    }
    int numberOfCustomers = getNumbersForRange(turnovers, min, new BigDecimal(Integer.MAX_VALUE));
    if (numberOfCustomers > 0) {
      numberOfCustomersWithTurnOver += numberOfCustomers;
      result.put("> " + min + "\u20AC", numberOfCustomers);
    }
    int numberOfAllCustomers = loadNumberOfCustomersForSupportUser(uUser);
    if (numberOfAllCustomers > numberOfCustomersWithTurnOver) {
      Integer customersInFirstRange = result.get("0 - " + ranges.get(0) + "\u20AC");
      if (customersInFirstRange == null) {
        customersInFirstRange = 0;
      }
      customersInFirstRange += (numberOfAllCustomers - numberOfCustomersWithTurnOver);
      result.put("0 - " + ranges.get(0) + "\u20AC", customersInFirstRange);
    }
    return result;
  }

  private int getNumbersForRange(List<Tupel<Long, BigDecimal>> turnovers, BigDecimal min, BigDecimal range) {
    int customers = 0;
    for (Tupel<Long, BigDecimal> turnover : turnovers) {
      if (turnover.getValue2().compareTo(min) >= 0 && turnover.getValue2().compareTo(range) == -1) {
        customers++;
      }
    }
    return customers;
  }

  private List<BigDecimal> loadRanges(String uUser) {
    String[] rangeValues = settingService.getValuesForUserIgnoreMissing("mycuco.turnover.ranges", uUser);
    List<BigDecimal> ranges = new ArrayList<BigDecimal>(rangeValues.length);
    for (String rangeValue : rangeValues) {
      ranges.add(new BigDecimal(rangeValue));
    }
    return ranges;
  }

  @Override
  public SearchResult<Party> filterCustomersForSupportUser(CustomerFilter customerFilter, String username, boolean showNonCustomers) {

    SearchResult<Party> filteredCustomersForSupportUser = partyDao.filterCustomersForSupportUser(customerFilter, username);
    if (showNonCustomers && (customerFilter.getDualSegments().contains(DualSegment.ALL) || customerFilter.getDualSegments().contains(DualSegment.NONCUSTOMER))
        && customerFilter.getVip().equals(Vip.ALL) && customerFilter.getFlashInfo().equals(FlashInfo.ALL) && customerFilter.getChurn().equals(Churn.ALL)
        && customerFilter.getIndexation().equals(Indexation.ALL) && customerFilter.getTurnoverRanges().contains("ALL") && customerFilter.getProductDetailsFilter() != null
        && customerFilter.getProductDetailsFilter().contains(VBMProductDetails.NO_PROD_FILTER)) {
      PartySearch nonCustomerSearch = new PartySearch();
      nonCustomerSearch.setSupportUserId(username);
      nonCustomerSearch.setLeadId(customerFilter.getPartyId());
      nonCustomerSearch.setPostcode(customerFilter.getPlz());
      filteredCustomersForSupportUser.getResults().addAll(partyDao.searchNonCustomerFull(nonCustomerSearch, settingService.getIntValue("Partysearch.maxResults", 2000)).getContent());
    }

    return filteredCustomersForSupportUser;
  }

  @Override
  public List<Party> filterCustomersForSupportUserUnlimited(CustomerFilter customerFilter, String username) {
    List<Party> filterCustomersForSupportUserUnlimited = partyDao.filterCustomersForSupportUserUnlimited(customerFilter, username);
    if ((customerFilter.getDualSegments().contains(DualSegment.ALL) || customerFilter.getDualSegments().contains(DualSegment.NONCUSTOMER)) && customerFilter.getVip().equals(Vip.ALL)
        && customerFilter.getFlashInfo().equals(FlashInfo.ALL) && customerFilter.getChurn().equals(Churn.ALL) && customerFilter.getIndexation().equals(Indexation.ALL)
        && customerFilter.getTurnoverRanges().contains("ALL") && customerFilter.getProductDetailsFilter() != null
        && customerFilter.getProductDetailsFilter().contains(VBMProductDetails.NO_PROD_FILTER)) {
      PartySearch nonCustomerSearch = new PartySearch();
      nonCustomerSearch.setSupportUserId(username);
      nonCustomerSearch.setLeadId(customerFilter.getPartyId());
      nonCustomerSearch.setPostcode(customerFilter.getPlz());
      filterCustomersForSupportUserUnlimited.addAll(partyDao.searchNonCustomerFull(nonCustomerSearch, settingService.getIntValue("Partysearch.maxResults", 2000)).getContent());
    }

    return filterCustomersForSupportUserUnlimited;
  }

  @Autowired
  public void setPartyDao(@Qualifier("cucoCustomerDao") PartyDao partyDao) {
    this.partyDao = partyDao;
  }

  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }

  @Autowired
  public void setPhoneNumberDao(PhoneNumberDao phoneNumberDao) {
    this.phoneNumberDao = phoneNumberDao;
  }

  @Override
  public int loadNumberOfCustomersWithVBMForSupportUser(String uUser) {
    return partyDao.loadNumberOfCustomersWithVBMForSupportUser(uUser);
  }

  @Override
  public Map<String, List<String>> getFilters(List<String> filterNames, String uUser) {
    Map<String, List<String>> results = new HashMap<String, List<String>>();
    if (filterNames.contains("mycuco.turnover.ranges")) {
      String valueForUserOrNull = settingService.getValueForUserOrNull("mycuco.turnover.ranges", uUser);
      List<String> ranges = new ArrayList<String>();
      if (valueForUserOrNull != null) {
        ranges.addAll(Arrays.asList(valueForUserOrNull.split(";")));
      }
      results.put("mycuco.turnover.ranges", ranges);
    }
    if (filterNames.contains("mycuco.vbm.products")) {
      List<String> productNames = new ArrayList<String>();
      List<VBMProductDetails> listAllVBMProductDetails = vbmProductsDao.listAllVBMProductDetails();
      listAllVBMProductDetails.add(0, VBMProductDetails.ALL_PROD);
      listAllVBMProductDetails.add(0, VBMProductDetails.NO_PROD_FILTER);
      for (VBMProductDetails product : listAllVBMProductDetails) {
        productNames.add(product.getProductId() + ":" + product.getProductName());
      }
      results.put("mycuco.vbm.products", productNames);
    }
    return results;
  }

  @Autowired
  public void setVbmProductsDao(VbmProductsDao vbmProductsDao) {
    this.vbmProductsDao = vbmProductsDao;
  }
}
