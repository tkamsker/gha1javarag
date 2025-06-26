package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.PhoneNumberDao;
import at.a1ta.cuco.core.service.PhoneNumberService;
import at.a1ta.cuco.core.shared.dto.BillingAccountNumber;
import at.a1ta.cuco.core.shared.dto.MobileChurnLikeliness;
import at.a1ta.cuco.core.shared.dto.PhoneNumber;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

@Service
public class PhoneNumberServiceImpl implements PhoneNumberService {
  @Autowired
  private PhoneNumberDao phoneNumberDao;

  @Override
  public List<PhoneNumber> listPhoneNumbers4Contract(final Number contractId) {
    if (contractId == null) {
      throw new org.apache.commons.lang.NullArgumentException("contractId");
    }
    return this.phoneNumberDao.listPhoneNumbers(null, (Long) contractId, null, -1, -1);
  }

  @Override
  public List<PhoneNumber> listPhoneNumbers4Customer(final Number customerId) {
    return this.listPhoneNumbers4Customer(customerId, null);
  }

  @Override
  public List<PhoneNumber> listPhoneNumbers4Customer(final Number customerId, final Number contractId) {
    return this.listPhoneNumbers4Customer(customerId, contractId, null);
  }

  @Override
  public List<PhoneNumber> listPhoneNumbers4Customer(final Number customerId, final Number contractId, final Number locationId) {
    return this.listPhoneNumbers4Customer(customerId, contractId, locationId, -1, -1);
  }

  @Override
  public List<PhoneNumber> listPhoneNumbers4Customer(final Number customerId, final Number contractId, final Number locationId, final int skip, final int maxResults) {
    if (customerId == null) {
      throw new org.apache.commons.lang.NullArgumentException("customerId");
    }
    return this.phoneNumberDao.listPhoneNumbers((Long) customerId, (Long) contractId, (Long) locationId, skip, maxResults);
  }

  @Override
  public List<PhoneNumber> listPhoneNumbers4Location(final Number locationId) {
    return this.listPhoneNumbers4Location(locationId, null);
  }

  @Override
  public List<PhoneNumber> listPhoneNumbers4Location(final Number locationId, final Number customerId) {
    if (locationId == null) {
      throw new org.apache.commons.lang.NullArgumentException("locationId");
    }
    return this.phoneNumberDao.listPhoneNumbers((Long) customerId, null, (Long) locationId, -1, -1);
  }

  @Override
  public PhoneNumberStructure parse(final String phoneNumberAsString) {
    return phoneNumberDao.parse(phoneNumberAsString);
  }

  @Override
  public List<BillingAccountNumber> getBillingAccountNumbersForParty(long partyId) {
    return phoneNumberDao.getBillingAccountNumbersForParty(partyId);
  }

  @Override
  public Long getBillingAccountNumberForPhoneNumber(String countryCode, String onkz, String number) {
    return phoneNumberDao.getBillingAccountNumberForPhoneNumber(countryCode, onkz, number);
  }

  @Override
  public ArrayList<String> getPhoneNumbersForClearingAccountId(long clearingAccountId) {
    return (ArrayList<String>) phoneNumberDao.getPhoneNumbersForClearingAccountId(clearingAccountId);
  }

  @Override
  public List<PhoneNumber> getPhoneNumbersForBillingAccountNumber(BillingAccountNumber ban) {
    return phoneNumberDao.getPhoneNumbersForBillingAccountNumber(ban.getBan());
  }

  @Override
  public List<MobileChurnLikeliness> getMobileChurnLikelinessForParty(long partyId) {
    return phoneNumberDao.getMobileChurnLikelinessForParty(partyId);
  }
}
