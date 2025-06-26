package at.a1ta.cuco.core.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import at.a1ta.cuco.core.dao.db.PhoneNumberDao;
import at.a1ta.cuco.core.dao.util.PhoneNumberParser;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

@Component
public class PartySearchValueFormatHelper {

  private static final String LEADING_ZERO = "0";
  private static final int COMMERCIAL_REG_NUMBER_LEN = 9;

  private final PhoneNumberParser phoneNumberParser;

  @Autowired
  public PartySearchValueFormatHelper(PhoneNumberDao phoneNumberDao) {
    this.phoneNumberParser = new PhoneNumberParser(phoneNumberDao);
  }

  public PhoneNumberStructure parsePhoneNumber(String phoneNumber) {
    return phoneNumberParser.parse(phoneNumber);
  }

  public String formatCommectialRegisterNumber(String commectialRegisterNumber) {
    if (commectialRegisterNumber == null || commectialRegisterNumber.length() > COMMERCIAL_REG_NUMBER_LEN) {
      return commectialRegisterNumber;
    }

    final int max = COMMERCIAL_REG_NUMBER_LEN - commectialRegisterNumber.length();
    final StringBuilder paddingLeft = new StringBuilder(max * 2);
    for (int i = 0; i < max; i++) {
      paddingLeft.append(LEADING_ZERO);
    }
    return paddingLeft.toString() + commectialRegisterNumber;

  }
}
