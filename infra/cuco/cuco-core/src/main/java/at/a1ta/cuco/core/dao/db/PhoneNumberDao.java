package at.a1ta.cuco.core.dao.db;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.BillingAccountNumber;
import at.a1ta.cuco.core.shared.dto.MobileChurnLikeliness;
import at.a1ta.cuco.core.shared.dto.PhoneNumber;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;
import at.a1ta.cuco.core.shared.dto.ProductDetailFilter;

public interface PhoneNumberDao {
  List<PhoneNumber> listPhoneNumbers(final Long customerId, final Long contractId, final Long locationId, final int skip, final int maxResults);

  List<String> getCountryCodes();

  List<String> getOnkzs();

  List<String> getSpecialOnkzs();

  String findByTN(List<String> possibleNumbers, String onkz);

  PhoneNumberStructure parse(String phoneNumber);

  List<BillingAccountNumber> getBillingAccountNumbersForParty(long partyId);

  List<PhoneNumber> listPhoneNumbers(List<Long> partyIds, ProductDetailFilter productFilter);

  Long getBillingAccountNumberForPhoneNumber(String countryCode, String onkz, String number);

  List<String> getPhoneNumbersForClearingAccountId(long clearingAccountId);

  List<PhoneNumber> getPhoneNumbersForBillingAccountNumber(long banId);

  List<MobileChurnLikeliness> getMobileChurnLikelinessForParty(long partyId);

  int loadNumberOfCustomersWithMobileChurnForSupportUser(String uUser);
}
