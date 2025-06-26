package at.a1ta.cuco.core.dao.db.impl;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.bite.data.solr.core.query.Field;
import at.a1ta.bite.data.solr.core.query.result.FacetResult;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.dao.db.PhoneNumberDao;
import at.a1ta.cuco.core.shared.dto.CustomerFilter;
import at.a1ta.cuco.core.shared.dto.CustomerFilter.WorthClass;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartySearch;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;
import at.a1ta.cuco.core.shared.dto.SimplePage;
import at.a1ta.cuco.core.shared.dto.Tupel;
import at.a1ta.cuco.core.shared.dto.nbo.VBMProductDetails;
import at.a1ta.cuco.core.shared.model.DualSegment;

public class PartyDaoImpl extends AbstractDao implements PartyDao {
  private static final String SQL_WILDCARD = "%";
  private static final String QUERY_SEARCH_CUSTOMER = "Customer.SearchCustomer";
  private static final String QUERY_SEARCH_NON_CUSTOMER = "Customer.SearchNonCustomerNonMerged";
  private static final String QUERY_SEARCH_NON_CUSTOMER_FULL = "Customer.SearchNonCustomerAll";
  private static final String INSERT_NON_CUSTOMER = "Customer.InsertNonCustomer";
  private static final String MARK_NC_MERGED = "Customer.markNonCustomerMerged";
  private static final String MERGE_NC_TRANSFER_OFFERS = "Customer.mergeNonCustomerAndTransferOffers";
  private static final String QUERY_GET_CUSTOMER_FOR_HEADER = "Customer.GetCustomer4Header";
  private static final String QUERY_COUNT_CUSTOMER_FOR_HEADER = "Customer.CountCustomer4Header";
  private static final String QUERY_IS_SUBSIDISED = "Customer.IsSubsidised";
  private static final String PARAM_CUSTOMER_ID = "customerId";
  private static final String PARAM_TARIFS = "tarifs";
  private static final String QUERY_COUNT_CUSTOMER_FOR_USER = "Customer.GetNumberOfCustomersForSupportUser";
  private static final String QUERY_COUNT_CUSTOMER_WITH_CHURN_FOR_USER = "Customer.GetNumberOfCustomersWithChurnForSupportUser";
  private static final String QUERY_COUNT_CUSTOMER_WITH_INDEXATION_FOR_USER = "Customer.GetNumberOfCustomersWithIndexationForSupportUser";
  private static final String QUERY_COUNT_CUSTOMER_WITH_FLASH_FOR_USER = "Customer.GetNumberOfCustomersWithFlashInfosForSupportUser";
  private static final String QUERY_COUNT_CUSTOMER_WITH_VIP_FOR_USER = "Customer.GetNumberOfCustomersWithVIPForSupportUser";
  private static final String QUERY_COUNT_CUSTOMER_WITH_VBM_FOR_USER = "Customer.GetNumberOfCustomersWithVBMForSupportUser";
  private static final String QUERY_COUNT_CUSTOMER_BY_TYPE_FOR_USER = "Customer.GetNumberOfCustomersByTypeForSupportUser";
  private static final String QUERY_COUNT_CUSTOMER_BY_WORTHCLASS_FOR_USER = "Customer.GetNumberOfCustomersByWorthclassForSupportUser";
  private static final String QUERY_COUNT_CUSTOMER_IN_TURNOVERRANGE_FOR_USER = "Customer.GetNumberOfCustomersInTurnoverRangeForSupportUser";
  private static final String QUERY_GET_CUSTOMER_IDS_FOR_USER = "Customer.GetCustomerIdsForSupportUser";
  private static final String QUERY_LOAD_PARTIES_OF_FLASHINFO = "Customer.LoadPartiesOfFlashInfo";
  private static final String QUERY_LOAD_PARTIES_FOR_QUOTENUMBER = "Customer.getPartyIdForQuoteNumber";
  private static final String SEARCH_RESULT_LIMIT_SETTING_KEY = "mycuco.table.searchresult.limit";

  @Autowired
  private SettingService settingService;
  @Autowired
  private PhoneNumberDao phoneNumberDao;

  @SuppressWarnings({"unchecked", "deprecation"})
  @Override
  public SimplePage<Party> search(PartySearch partySearch, final int maxResults) {
    SimplePage<Party> page = new SimplePage<Party>();

    if (partySearch.getLastName() != null) {
      partySearch.setLastName(partySearch.getLastName() + SQL_WILDCARD);
    }
    if (partySearch.getFirstName() != null) {
      partySearch.setFirstName(partySearch.getFirstName() + SQL_WILDCARD);
    }
    if (partySearch.getCity() != null) {
      partySearch.setCity(partySearch.getCity() + SQL_WILDCARD);
    }
    if (partySearch.getVillage() != null) {
      partySearch.setVillage(partySearch.getVillage() + SQL_WILDCARD);
    }
    if (partySearch.getStreet() != null) {
      partySearch.setStreet(partySearch.getStreet() + SQL_WILDCARD);
    }
    if (partySearch.getHouseNumber() != null) {
      partySearch.setHouseNumber(partySearch.getHouseNumber() + SQL_WILDCARD);
    }
    if (partySearch.getPhoneNumber() != null) {
      final PhoneNumberStructure phoneNumberStructure = parsePhoneNumber(partySearch);

      if (phoneNumberStructure == null) {
        return page;
      }

      partySearch.setLkz(phoneNumberStructure.getCountryCode());
      partySearch.setOkz(phoneNumberStructure.getOnkz());
      partySearch.setCallNumber(phoneNumberStructure.getNumber());
    }
    ArrayList<Party> result = new ArrayList<Party>();
    result.addAll(getSqlMapClientTemplate().queryForList(QUERY_SEARCH_CUSTOMER, partySearch, 0, maxResults));

    page.setContent(result);
    page.setCount(result.size());
    return page;
  }

  @Override
  public SimplePage<Party> searchNonCustomer(PartySearch partySearch, final int maxResults) {
    SimplePage<Party> page = new SimplePage<Party>();
    ArrayList<Party> result = new ArrayList<Party>();
    if ((partySearch.getLeadId() == null || partySearch.getLeadId().trim().isEmpty()) && (partySearch.getId() == null || partySearch.getId().trim().isEmpty())
        && (partySearch.getFirstName() == null || partySearch.getFirstName().trim().isEmpty()) && (partySearch.getLastName() == null || partySearch.getLastName().trim().isEmpty())
        && (partySearch.getCity() == null || partySearch.getCity().trim().isEmpty()) && (partySearch.getPostcode() == null || partySearch.getPostcode().trim().isEmpty())
        && (partySearch.getStreet() == null || partySearch.getStreet().trim().isEmpty()) && partySearch.getBirthDate() == null
        && (partySearch.getVillage() == null || partySearch.getVillage().trim().isEmpty()) && (partySearch.getHouseNumber() == null || partySearch.getHouseNumber().trim().isEmpty())) {
      page.setContent(result);
      page.setCount(0);
      return page;
    }
    if (partySearch.getLastName() != null) {
      partySearch.setLastName(partySearch.getLastName() + SQL_WILDCARD);
    }
    if (partySearch.getPostcode() != null) {
      partySearch.setPostcode(partySearch.getPostcode() + SQL_WILDCARD);
    }
    if (partySearch.getFirstName() != null) {
      partySearch.setFirstName(partySearch.getFirstName() + SQL_WILDCARD);
    }
    if (partySearch.getCity() != null) {
      partySearch.setCity(partySearch.getCity() + SQL_WILDCARD);
    }
    if (partySearch.getVillage() != null) {
      partySearch.setVillage(partySearch.getVillage() + SQL_WILDCARD);
    }
    if (partySearch.getStreet() != null) {
      partySearch.setStreet(partySearch.getStreet() + SQL_WILDCARD);
    }
    if (partySearch.getHouseNumber() != null) {
      partySearch.setHouseNumber(partySearch.getHouseNumber() + SQL_WILDCARD);
    }

    result.addAll(getSqlMapClientTemplate().queryForList(QUERY_SEARCH_NON_CUSTOMER, partySearch, 0, maxResults));

    page.setContent(result);
    page.setCount(result.size());
    return page;
  }

  @Override
  public SimplePage<Party> searchNonCustomerFull(PartySearch partySearch, final int maxResults) {
    SimplePage<Party> page = new SimplePage<Party>();
    ArrayList<Party> result = new ArrayList<Party>();
    if ((partySearch.getSupportUserId() == null || partySearch.getSupportUserId().trim().isEmpty()) && (partySearch.getLeadId() == null || partySearch.getLeadId().trim().isEmpty())
        && (partySearch.getId() == null || partySearch.getId().trim().isEmpty()) && (partySearch.getFirstName() == null || partySearch.getFirstName().trim().isEmpty())
        && (partySearch.getLastName() == null || partySearch.getLastName().trim().isEmpty()) && (partySearch.getCity() == null || partySearch.getCity().trim().isEmpty())
        && (partySearch.getPostcode() == null || partySearch.getPostcode().trim().isEmpty()) && (partySearch.getStreet() == null || partySearch.getStreet().trim().isEmpty())
        && partySearch.getBirthDate() == null && (partySearch.getVillage() == null || partySearch.getVillage().trim().isEmpty())
        && (partySearch.getHouseNumber() == null || partySearch.getHouseNumber().trim().isEmpty())) {
      page.setContent(result);
      page.setCount(0);
      return page;
    }

    if (partySearch.getLastName() != null) {
      partySearch.setLastName(partySearch.getLastName() + SQL_WILDCARD);
    }
    if (partySearch.getFirstName() != null) {
      partySearch.setFirstName(partySearch.getFirstName() + SQL_WILDCARD);
    }

    if (partySearch.getPostcode() != null) {
      partySearch.setPostcode(partySearch.getPostcode() + SQL_WILDCARD);
    }
    if (partySearch.getCity() != null) {
      partySearch.setCity(partySearch.getCity() + SQL_WILDCARD);
    }
    if (partySearch.getVillage() != null) {
      partySearch.setVillage(partySearch.getVillage() + SQL_WILDCARD);
    }
    if (partySearch.getStreet() != null) {
      partySearch.setStreet(partySearch.getStreet() + SQL_WILDCARD);
    }
    if (partySearch.getHouseNumber() != null) {
      partySearch.setHouseNumber(partySearch.getHouseNumber() + SQL_WILDCARD);
    }

    result.addAll(getSqlMapClientTemplate().queryForList(QUERY_SEARCH_NON_CUSTOMER_FULL, partySearch, 0, maxResults));

    page.setContent(result);
    page.setCount(result.size());
    return page;
  }

  private PhoneNumberStructure parsePhoneNumber(PartySearch partySearch) {
    return phoneNumberDao.parse(partySearch.getPhoneNumber());
  }

  @Override
  public List<Party> getCustomers4Header(long headerId, int skip, int maxResults) {
    return performListQuery(QUERY_GET_CUSTOMER_FOR_HEADER, Long.valueOf(headerId), skip, maxResults);
  }

  @Override
  public int countCustomers4Header(final long headerId) {
    return (Integer) performObjectQuery(QUERY_COUNT_CUSTOMER_FOR_HEADER, Long.valueOf(headerId));
  }

  @Override
  public boolean isSubsidised(long customerId, String[] subsidisedTarifs) {
    final Map<String, Object> params = new HashMap<String, Object>(2);
    params.put(PARAM_CUSTOMER_ID, Long.valueOf(customerId));
    params.put(PARAM_TARIFS, Arrays.asList(subsidisedTarifs));
    return ((Integer) performObjectQuery(QUERY_IS_SUBSIDISED, params)) > 0;
  }

  @Override
  public List<String> getAllSegments() {
    return performListQuery("Customer.getAllSegments");
  }

  @Override
  public void saveCucoCustomer(Party cucoCustomer) {
    if (executeUpdate("Customer.update", cucoCustomer) == 0) {
      executeInsert("Customer.insert", cucoCustomer);
    }
  }

  @Override
  public List<Party> loadParties(List<Long> partyIds) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("partyIds", partyIds);

    return performListQuery("Customer.loadParties", params);
  }

  @Override
  public Party loadParty(Long partyId) {
    return (Party) performObjectQuery("Customer.loadParty", partyId);
  }

  @Override
  public List<Party> getHierarchyForParty(long partyId) {
    return performListQuery("Customer.getHierarchy", partyId);
  }

  @Override
  public List<FacetResult> facetedSearch(PartySearch customerSearch, Field facetField) {
    return Collections.<FacetResult> emptyList();
  }

  @Override
  public int loadNumberOfCustomersForSupportUser(String uUser) {
    return (Integer) performObjectQuery(QUERY_COUNT_CUSTOMER_FOR_USER, uUser.toLowerCase());
  }

  @Override
  public int loadNumberOfCustomersWithChurnForSupportUser(String uUser) {
    return (Integer) performObjectQuery(QUERY_COUNT_CUSTOMER_WITH_CHURN_FOR_USER, uUser.toLowerCase());
  }

  @Override
  public int loadNumberOfCustomersWithIndexationForSupportUser(String uUser) {
    return (Integer) performObjectQuery(QUERY_COUNT_CUSTOMER_WITH_INDEXATION_FOR_USER, uUser.toLowerCase());
  }

  @Override
  public int loadNumberOfCustomersWithFlashInfosForSupportUser(String uUser) {
    return (Integer) performObjectQuery(QUERY_COUNT_CUSTOMER_WITH_FLASH_FOR_USER, uUser.toLowerCase());
  }

  @Override
  public int loadNumberOfCustomersWithVIPForSupportUser(String uUser) {
    return (Integer) performObjectQuery(QUERY_COUNT_CUSTOMER_WITH_VIP_FOR_USER, uUser.toLowerCase());
  }

  @Override
  @SuppressWarnings("unchecked")
  public Map<BigDecimal, BigDecimal> loadNumberOfCustomersByTypeForSupportUser(String uUser) {
    return (Map<BigDecimal, BigDecimal>) performMapQuery(QUERY_COUNT_CUSTOMER_BY_TYPE_FOR_USER, uUser.toLowerCase(), "key", "value");
  }

  @Override
  @SuppressWarnings("unchecked")
  public Map<String, BigDecimal> loadNumberOfCustomersByWorthclassForSupportUser(String uUser) {
    return (Map<String, BigDecimal>) performMapQuery(QUERY_COUNT_CUSTOMER_BY_WORTHCLASS_FOR_USER, uUser.toLowerCase(), "key", "value");
  }

  @Override
  public List<Tupel<Long, BigDecimal>> loadNumberOfCustomersTurnoverForSupportUser(String uUser) {
    return performListQuery(QUERY_COUNT_CUSTOMER_IN_TURNOVERRANGE_FOR_USER, uUser.toLowerCase());
  }

  @Override
  public List<Party> loadPartiesOfFlashInfo(Long flashInfoId, String username) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("flashId", flashInfoId);
    params.put("username", username);

    return performListQuery(QUERY_LOAD_PARTIES_OF_FLASHINFO, params);
  }

  @Override
  public List<Long> getCustomerIdsForSupportUser(String uUser) {
    List<Long> list = performListQuery(QUERY_GET_CUSTOMER_IDS_FOR_USER, uUser.toLowerCase());
    return list != null && list.size() > 0 ? list : null;
  }

  @SuppressWarnings("unchecked")
  @Override
  public SearchResult<Party> filterCustomersForSupportUser(CustomerFilter customerFilter, String uUser) {
    Map<String, Object> params = createParams(customerFilter, uUser.toLowerCase());
    SearchResult<Party> performLimitedListQuery;
    int resultsSizeLimit = settingService.getIntValue(SEARCH_RESULT_LIMIT_SETTING_KEY);
    if (customerFilter.getProductDetailsFilter() == null || customerFilter.getProductDetailsFilter().contains(VBMProductDetails.NO_PROD_FILTER)) {
      performLimitedListQuery = (SearchResult<Party>) performLimitedListQuery("Customer.FilterCustomersForSupportUser", params, resultsSizeLimit);
    } else {
      List<Party> results = performListQuery("Customer.FilterCustomersForSupportUser", params);
      SearchResult<Party> searchResult = new SearchResult<Party>(new ArrayList<Party>(), results.size() > resultsSizeLimit);
      searchResult.getResults().addAll(results);
      performLimitedListQuery = searchResult;
    }
    ArrayList<Party> results = new ArrayList<Party>();

    if (customerFilter.getProductDetailsFilter() != null && customerFilter.getProductDetailsFilter().contains(VBMProductDetails.ALL_PROD)) {
      for (Party party : performLimitedListQuery.getResults()) {
        if (results.size() >= resultsSizeLimit) {
          break;
        }
        if (party.getAvailableVbmProducts() == null || party.getAvailableVbmProducts().size() == 0) {
          // Tbd
        } else {
          results.add(party);
        }
      }
      performLimitedListQuery.getResults().retainAll(results);
    } else if (customerFilter.getProductDetailsFilter() != null && !customerFilter.getProductDetailsFilter().contains(VBMProductDetails.NO_PROD_FILTER)) {
      for (Party party : performLimitedListQuery.getResults()) {
        if (party.getAvailableVbmProducts() != null && party.getAvailableVbmProducts().size() > 0) {
          boolean shouldRemove = true;
          for (VBMProductDetails filter : customerFilter.getProductDetailsFilter()) {
            if (Arrays.asList(party.getVbmProductsAsString().split(",")).contains(filter.getProductName())) {
              shouldRemove = false;
            }
          }
          if (!shouldRemove) {
            if (results.size() >= resultsSizeLimit) {
              break;
            }
            results.add(party);
          }
        }
      }
      performLimitedListQuery.getResults().retainAll(results);
    }

    return performLimitedListQuery;
  }

  @Override
  public List<Party> filterCustomersForSupportUserUnlimited(CustomerFilter customerFilter, String uUser) {
    // TODO: pass customerFilter directly to sqlmap, move all logic to sqlmap
    Map<String, Object> params = createParams(customerFilter, uUser.toLowerCase());
    List<Party> performLimitedListQuery = performListQuery("Customer.FilterCustomersForSupportUser", params);
    ArrayList<Party> results = new ArrayList<Party>();

    if (customerFilter.getProductDetailsFilter() != null && customerFilter.getProductDetailsFilter().contains(VBMProductDetails.ALL_PROD)) {
      for (Party party : performLimitedListQuery) {
        if (party.getAvailableVbmProducts() == null || party.getAvailableVbmProducts().size() == 0) {
          // Tbd
        } else {
          results.add(party);
        }
      }
      performLimitedListQuery.retainAll(results);
    } else if (customerFilter.getProductDetailsFilter() != null && !customerFilter.getProductDetailsFilter().contains(VBMProductDetails.NO_PROD_FILTER)) {
      for (Party party : performLimitedListQuery) {
        if (party.getAvailableVbmProducts() != null && party.getAvailableVbmProducts().size() > 0) {
          boolean shouldRemove = true;
          for (VBMProductDetails filter : customerFilter.getProductDetailsFilter()) {
            if (Arrays.asList(party.getVbmProductsAsString().split(",")).contains(filter.getProductName())) {
              shouldRemove = false;
            }
          }
          if (!shouldRemove) {
            results.add(party);
          }
        }
      }
      performLimitedListQuery.retainAll(results);
    }
    return performLimitedListQuery;
  }

  private Map<String, Object> createParams(CustomerFilter customerFilter, String uUser) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("uUser", uUser.toLowerCase());
    addChurnFilterParams(customerFilter, params);
    addFlashInfoFilterParams(customerFilter, params);
    addVipFilterParams(customerFilter, params);
    addDualSegmentsFilterParams(customerFilter, params);
    addWorthClassesFilterParams(customerFilter, params);
    addTurnoverRangesFilterParams(customerFilter, params);
    params.put("partyId", customerFilter.getPartyId());
    params.put("plz", customerFilter.getPlz());
    addIndexationFilterParams(customerFilter, params);

    /*
     * if (customerFilter.getProductDetailsFilter() != null) {
     * if (!customerFilter.getProductDetailsFilter().contains(VBMProductDetails.NO_PROD_FILTER)) {
     * List<String> prodIds = new ArrayList<String>();
     * for (VBMProductDetails details : customerFilter.getProductDetailsFilter()) {
     * if (NumberUtils.isNumber(details.getProductId())) {
     * prodIds.add(details.getProductId());
     * }
     * }
     * if (!prodIds.isEmpty()) {
     * params.put("productId", prodIds);
     * } else {
     * params.put("productId", null);
     * }
     * }
     * }
     */

    return params;
  }

  private void addTurnoverRangesFilterParams(CustomerFilter customerFilter, Map<String, Object> params) {
    List<Tupel<BigDecimal, BigDecimal>> turnoverRanges = new ArrayList<Tupel<BigDecimal, BigDecimal>>();
    if (customerFilter.getTurnoverRanges() != null && !customerFilter.getTurnoverRanges().contains("ALL")) {
      for (String turnOverRangesString : customerFilter.getTurnoverRanges()) {
        String[] turnOverRangeStrings = turnOverRangesString.split(";");
        BigDecimal lowerRange = new BigDecimal(turnOverRangeStrings[0]);
        BigDecimal upperRange = new BigDecimal(turnOverRangeStrings[1]);
        Tupel<BigDecimal, BigDecimal> tupel = new Tupel<BigDecimal, BigDecimal>(lowerRange, upperRange);
        turnoverRanges.add(tupel);
      }
    }
    params.put("turnoverRanges", turnoverRanges);
  }

  private void addWorthClassesFilterParams(CustomerFilter customerFilter, Map<String, Object> params) {
    List<String> worthClasses = new ArrayList<String>();
    if (customerFilter.getWorthClasses() != null) {
      for (WorthClass worthClass : customerFilter.getWorthClasses()) {
        switch (worthClass) {
          case GOLD:
          case SILBER:
          case BRONZE:
          case BLEI:
            worthClasses.add(worthClass.name());
            break;
          case UNKNOWN:
            worthClasses.add(null);
            break;
        }
      }
    }
    params.put("worthClasses", worthClasses);
  }

  private void addDualSegmentsFilterParams(CustomerFilter customerFilter, Map<String, Object> params) {
    List<Integer> dualSegments = new ArrayList<Integer>();
    if (customerFilter.getDualSegments() != null) {
      for (DualSegment dualSegment : customerFilter.getDualSegments()) {
        switch (dualSegment) {
          case WIRED:
          case MOBILE:
          case DUAL:
          case CONVERGENT:
          case CONVERGENTWIRED:
          case CONVERGENTMOBILE:
          case DUALCONVERGENT:
            dualSegments.add(dualSegment.getCode());
            break;
          case UNKNOWN:
            dualSegments.add(null);
            break;
        }
      }
    }
    params.put("dualSegments", dualSegments);
  }

  private void addVipFilterParams(CustomerFilter customerFilter, Map<String, Object> params) {
    if (customerFilter.getVip() != null) {
      switch (customerFilter.getVip()) {
        case VIP:
        case NOVIP:
          params.put("vip", customerFilter.getVip().name());
      }
    }
  }

  private void addFlashInfoFilterParams(CustomerFilter customerFilter, Map<String, Object> params) {
    if (customerFilter.getFlashInfo() != null) {
      switch (customerFilter.getFlashInfo()) {
        case FLASH:
        case NOFLASH:
          params.put("flash", customerFilter.getFlashInfo().name());
      }
    }
  }

  private void addChurnFilterParams(CustomerFilter customerFilter, Map<String, Object> params) {
    if (customerFilter.getChurn() != null) {
      switch (customerFilter.getChurn()) {
        case DANGER:
        case NODANGER:
          params.put("churn", customerFilter.getChurn().name());
      }
    }
  }

  private void addIndexationFilterParams(CustomerFilter customerFilter, Map<String, Object> params) {
    if (customerFilter.getIndexation() != null) {
      switch (customerFilter.getIndexation()) {
        case MitIndexierung:
        case MitIndexanpassung:
        case OhneIndexierung:
          params.put("indexation", customerFilter.getIndexation().name());
      }
    }
  }

  @Override
  public void insertNonCustomerContact(Party party) {
    executeInsert(INSERT_NON_CUSTOMER, party);
  }

  @Override
  public void markNonCustomerMerged(Party party) {
    executeUpdate(MARK_NC_MERGED, party);
  }

  @Override
  public void mergeNonCustomerAndTransferOffers(Party party) {
    executeUpdate(MERGE_NC_TRANSFER_OFFERS, party);
  }

  @Override
  public int loadNumberOfCustomersWithVBMForSupportUser(String uUser) {
    return (Integer) performObjectQuery(QUERY_COUNT_CUSTOMER_WITH_VBM_FOR_USER, uUser.toLowerCase());
  }

  @Override
  public String getPartyIdForQuoteNumber(String offerNumber) {
    String result = performObjectQuery(QUERY_LOAD_PARTIES_FOR_QUOTENUMBER, offerNumber);

    return result == null ? "" : result;
  }
}
