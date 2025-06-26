package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.PhoneNumberDao;
import at.a1ta.cuco.core.dao.util.PhoneNumberParser;
import at.a1ta.cuco.core.shared.dto.BillingAccountNumber;
import at.a1ta.cuco.core.shared.dto.MobileChurnLikeliness;
import at.a1ta.cuco.core.shared.dto.PhoneNumber;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;
import at.a1ta.cuco.core.shared.dto.ProductDetailFilter;

public class PhoneNumberDaoImpl extends AbstractDao implements PhoneNumberDao {

  private static final String PARAM_CUSTOMER_ID = "customerId";
  private static final String PARAM_CUSTOMER_IDS = "customerIds";
  private static final String PARAM_CONTRACT_ID = "contractId";
  private static final String PARAM_LOCATION_ID = "locationId";
  private static final String QUERY_GET_PHONE_NUMBERS = "PhoneNumber.GetPhoneNumbers";
  private static final String QUERY_DISTINCT_COUNTRY_CODES = "PhoneNumber.getCountryCodes";
  private static final String QUERY_DISTINCT_ONKZS = "PhoneNumber.getOnkzs";
  private static final String QUERY_DISTINCT_SPECIAL_ONKZS = "PhoneNumber.getSpecialOnkzs";
  private static final String QUERY_FIND_BY_TN = "PhoneNumber.findByTN";

  @Override
  public List<PhoneNumber> listPhoneNumbers(final Long customerId, final Long contractId, final Long locationId, final int skip, final int maxResults) {
    final Map<String, Object> params = new HashMap<String, Object>(3);
    if (customerId != null) {
      params.put(PARAM_CUSTOMER_ID, customerId);
    }
    if (contractId != null) {
      params.put(PARAM_CONTRACT_ID, contractId);
    }
    if (locationId != null) {
      params.put(PARAM_LOCATION_ID, locationId);
    }
    return performListQuery(QUERY_GET_PHONE_NUMBERS, params, skip, maxResults);
  }

  @Override
  public List<PhoneNumber> listPhoneNumbers(List<Long> customerIds, ProductDetailFilter productFilter) {
    Map<String, Object> params = new HashMap<String, Object>();

    params.put(PARAM_CUSTOMER_IDS, customerIds);
    params.put("filter", productFilter);

    return performListQuery(QUERY_GET_PHONE_NUMBERS, params);
  }

  @Override
  public List<String> getCountryCodes() {
    return performListQuery(QUERY_DISTINCT_COUNTRY_CODES);
  }

  @Override
  public List<String> getOnkzs() {
    return performListQuery(QUERY_DISTINCT_ONKZS);
  }

  @Override
  public List<String> getSpecialOnkzs() {
    return performListQuery(QUERY_DISTINCT_SPECIAL_ONKZS);
  }

  @Override
  public String findByTN(List<String> possibleNumbers, String onkz) {
    final Map<String, Object> params = new HashMap<String, Object>(2);
    params.put("onkz", onkz);
    params.put("numbers", possibleNumbers);

    final List<String> numbers = performListQuery(QUERY_FIND_BY_TN, params);
    return numbers != null && numbers.size() > 0 ? numbers.get(0) : null;
  }

  @Override
  public PhoneNumberStructure parse(final String phoneNumberAsString) {
    final PhoneNumberParser parser = new PhoneNumberParser(this);
    return parser.parse(phoneNumberAsString);
  }

  @Override
  public List<BillingAccountNumber> getBillingAccountNumbersForParty(long partyId) {
    return performListQuery("PhoneNumber.getBillingAccountNumbersForParty", partyId);
  }

  @Override
  public Long getBillingAccountNumberForPhoneNumber(String countryCode, String onkz, String number) {
    Map<String, Object> params = new HashMap<String, Object>(2);
    params.put("countryCode", countryCode);
    params.put("onkz", onkz);
    params.put("number", number);

    return performObjectQuery("PhoneNumber.getBillingAccountNumberForPhoneNumber", params);
  }

  @Override
  public List<String> getPhoneNumbersForClearingAccountId(long clearingAccountId) {
    return performListQuery("PhoneNumber.getPhoneNumbersForClearingAccountId", clearingAccountId);
  }

  @Override
  public List<PhoneNumber> getPhoneNumbersForBillingAccountNumber(long banId) {
    return performListQuery("PhoneNumber.getPhoneNumbersForBillingAccountNumber", banId);
  }

  @Override
  public List<MobileChurnLikeliness> getMobileChurnLikelinessForParty(long partyId) {
    return performListQuery("PhoneNumber.getMobileChurnLikelinessForParty", partyId);
  }

  @Override
  public int loadNumberOfCustomersWithMobileChurnForSupportUser(String uUser) {
    return (Integer) performObjectQuery("PhoneNumber.GetNumberOfCustomersWithChurnForSupportUser", uUser.toLowerCase());
  }
}
