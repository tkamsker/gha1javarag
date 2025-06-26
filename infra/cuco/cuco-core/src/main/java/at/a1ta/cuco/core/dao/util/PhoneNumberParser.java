/*
 * Copyright 2009 - 2014 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.core.dao.util;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.lang.ArrayUtils;
import org.apache.commons.lang.StringUtils;

import at.a1ta.cuco.core.dao.db.PhoneNumberDao;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

public class PhoneNumberParser {

  private static final String ILLEGAL_CHARS = "() -\\/.";
  private List<String> countryCodes;
  private List<String> onkzs;
  private List<String> specialOnkzs;
  private PhoneNumberDao phonenumberDao;

  private static final String DIGITS = "0123456789";
  private static final String DEFAULT_COUNTRY_CODE = "43";
  private static final String AUSTRIAN_PREFIX = "00";

  public PhoneNumberParser(final PhoneNumberDao phonenumberDao) {
    this.phonenumberDao = phonenumberDao;
    countryCodes = phonenumberDao.getCountryCodes();
    onkzs = phonenumberDao.getOnkzs();
    specialOnkzs = phonenumberDao.getSpecialOnkzs();
  }

  /**
   * Parses a given international phone number
   * 
   * @param originalInput phone number string
   * @return field[0]=CountryCode, field[1]=Oknz, field[2]=Number OR null if the string could not be parsed
   */
  public PhoneNumberStructure parse(final String originalInput) {
    final String[] result = parse(originalInput, true);
    return result == null ? null : new PhoneNumberStructure(result[0], result[1], result[2], result[3]);
  }

  /**
   * Parses a given international phone number
   * 
   * @param phoneNumber phone number string
   * @param useMissingPlusLogic indicates if after a failed parsing process the logic should check for a missing "+"
   *          e.g. 43 732 1234 is not parseable as the format is invalid. Attaching a "+" will lead to a parseable string
   *          as +43 732 1234 is a valid format
   * @return field[0]=CountryCode, field[1]=Oknz, field[2]=Number OR null if the string could not be parsed
   */
  private String[] parse(final String phoneNumber, final boolean useMissingPlusLogic) {
    try {
      String countryCode = null;
      String onkz = null;
      String number = null;
      String extension = null;

      // remove whitespaces and other illeagal characters
      final String trimmedAndCleaned = trimAndClean(phoneNumber);

      // split after country code
      final String[] countryCodeAndNumber = splitAfterCountryCode(trimmedAndCleaned, countryCodes); // [0]=countryCode [1]=the rest (without
                                                                                                    // the
      // country code)
      countryCode = countryCodeAndNumber[0]; // e.g. 43
      final String numberWithoutCountryCode = countryCodeAndNumber[1]; // e.g. 664 123456

      // get the onkz
      final String[] onkzAndNumber = splitAfterOnkz(numberWithoutCountryCode, onkzs, specialOnkzs); // [0]=onkz [1]=the rest (without the
                                                                                                    // onkz)
      onkz = onkzAndNumber[0]; // e.g. 664
      final String numberAndExt = onkzAndNumber[1]; // e.g. 123456

      // check for alph. chars
      if (containsNonDigits(numberAndExt)) {
        return null;
      }

      if (onkz == null && useMissingPlusLogic) {
        // assertion: parse failed; usemissingPlusLogic flag indicates to perform another parsing logic...
        // the whole number will be packaged inside the number variable; a '+' might be missing
        // call the parse method with useMissingPlusLogic==false to avoid endless recursive calling of the method
        return parse("+" + phoneNumber, false);
      }

      // assertion: number - only has digits AND may include an extension

      // austrian phone numbers have max. 7 digits the rest are surely extension digits; e.g. 123456789 -> 89 is the exension
      // performance: ... number = numberAndExt.length() > 7 ? numberAndExt.substring(0, 7) : numberAndExt;
      // assertion: number is now max 7 digits long

      // look for an matching number in the database
      number = findNumberInDatabase(numberAndExt, onkz);
      if (number == null) {

        if (useMissingPlusLogic) {
          return parse("+" + phoneNumber, false);
        }

        return null;
      }

      // assertion: number is now max 7 digits long AND does not contain an extension

      extension = calculateExtension(numberAndExt, number);

      final String[] phoneNumberParts = new String[] {countryCode, onkz, number, extension};
      return isFullyParsed(phoneNumberParts) ? phoneNumberParts : null; // return all fields or nothing (null)
    } catch (Exception e) {
      return null;
    }
  }

  /**
   * Calculates the extension part
   * 
   * @param numberAndExt e.g. 123456
   * @param number e.g. 1234
   * @return e.g. 56
   */
  private static String calculateExtension(final String numberAndExt, final String number) {
    if (number.length() < numberAndExt.length()) {
      return numberAndExt.substring(number.length());
    }
    return StringUtils.EMPTY; // No extension
  }

  private String findNumberInDatabase(final String number, final String onkz) {
    final List<String> possibleNumbers = generateListOfPossibleNumbers(number);
    return phonenumberDao.findByTN(possibleNumbers, onkz);
  }

  /**
   * e.g. for number = 1234567 the result list of possibleNumbers will be ["1234567", "123456", "12345", "1234", "123"]
   * 
   * @param number
   * @return
   */
  static List<String> generateListOfPossibleNumbers(final String number) {
    final List<String> possibleNumbers = new ArrayList<String>(number.length());
    for (int i = number.length(); i >= 3; i--) {
      possibleNumbers.add(number.substring(0, i));
    }
    return possibleNumbers;
  }

  /**
   * Checks if a number string has any non digital (a-zA-Z etc.) character
   * 
   * @param input string
   * @return true if it contains any non digital chars; false otherwise
   */
  static boolean containsNonDigits(final String input) {
    if (StringUtils.isBlank(input)) {
      return false;
    }
    return StringUtils.containsNone(input, DIGITS);
  }

  /**
   * Determines if the parsed result is complete (every field available: countrycode and onkz and number and extension
   * 
   * @param phoneNumberParts parsed phone number result
   * @return true if complete; false othwerwise
   */
  static boolean isFullyParsed(final String[] phoneNumberParts) {
    return (phoneNumberParts != null) && (phoneNumberParts.length == 4) && !ArrayUtils.contains(phoneNumberParts, null);
  }

  /**
   * Trims and cleans a given string from whitespaces, brakes and other illegal chars
   * 
   * @param originalInput
   * @return trimmed and cleaned string
   */
  static String trimAndClean(final String phoneNumber) {
    final String zeroInBrackets = "\\(\\s*0\\s*\\)"; // bracket, whitespaces, 0, whitespaces, bracket
    String cleanPhoneNumber = phoneNumber.replaceAll(zeroInBrackets, StringUtils.EMPTY);

    return StringUtils.replaceChars(cleanPhoneNumber, ILLEGAL_CHARS, null);
  }

  static String[] splitAfterOnkz(final String phoneNumberWithoutCountryCode, final List<String> onkzs, final List<String> specialOnkzs) {
    String s = phoneNumberWithoutCountryCode;

    // Search for special ONKZ (starting with zero, e.g. 0800 national free calls)
    for (final String onkz : specialOnkzs) {
      if (s.startsWith(onkz)) {
        return new String[] {onkz, s.substring(onkz.length())}; // returns the country code and the phone number without the country code
      }
    }

    // assertion: the number does not start with an special ONKZ (starting with a zero);

    // TODO: I think there shouldn't be any case with a leading zero, see comment above
    s = StringUtils.removeStart(s, "0"); // remove a possible leading zero character

    for (final String onkz : onkzs) {
      if (s.startsWith(onkz)) {
        return new String[] {onkz, s.substring(onkz.length())}; // returns the ONKZ and the phone number without the ONKZ
      }
    }

    return new String[] {null, s};
  }

  static String[] splitAfterCountryCode(final String phoneNumber, final List<String> countryCodes) {
    String withoutPrefix = null;
    if (phoneNumber.startsWith("+")) {
      withoutPrefix = phoneNumber.substring(1);
    } else if (phoneNumber.startsWith(AUSTRIAN_PREFIX)) {
      withoutPrefix = phoneNumber.substring(AUSTRIAN_PREFIX.length());
    }

    if (withoutPrefix != null) {
      for (final String countryCode : countryCodes) {
        if (withoutPrefix.startsWith(countryCode)) {
          return new String[] {countryCode, withoutPrefix.substring(countryCode.length())}; // returns the country code and the phone number
          // without the country code
        }
      }
    }

    return new String[] {DEFAULT_COUNTRY_CODE, phoneNumber};
  }

  // not in use - alternative logic for parsing
  @SuppressWarnings("unused")
  private static String[] parseAlternative(final String orig) {
    String transformed = transform(orig);
    final String[] parts = transformed.split("@");

    if (parts.length < 2) {
      return null;
    }
    if (parts.length == 2) {
      final String countryCode = DEFAULT_COUNTRY_CODE;
      String onkz = parts[0]; // part[0] is the onkz
      onkz = removeLeadingZero(onkz);
      return new String[] {countryCode, onkz, parts[1]};
    }
    // more than 2 parts
    if (parts[0].charAt(0) == '0') {
      final String countryCode = DEFAULT_COUNTRY_CODE;
      String onkz = parts[0]; // part[0] is the onkz
      onkz = removeLeadingZero(onkz);
      final String number = arrayToString(parts, "", 1, parts.length - 1);
      return new String[] {countryCode, onkz, number};
    }
    final String countryCode = parts[0]; // part[0] is the country code
    String onkz = parts[1]; // part[1] is the onkz
    onkz = removeLeadingZero(onkz);
    final String number = arrayToString(parts, "", 2, parts.length - 1);
    return new String[] {countryCode, onkz, number};
  }

  // not in use - alternative logic for parsing
  private static String removeLeadingZero(final String onkz) {
    return onkz.replaceAll("^0+", "");
  }

  // not in use - alternative logic for parsing
  private static String arrayToString(final String[] parts, final String seperator, final int startIdx, final int endIdx) {
    final StringBuilder sb = new StringBuilder();
    for (int i = startIdx; i <= endIdx; i++) {
      sb.append(parts[i]);
      sb.append(seperator);
    }
    return sb.toString();
  }

  // not in use - alternative logic for parsing
  private static String transform(final String s) {
    String str = s.trim(); // trim
    str = str.replaceFirst("00", ""); // replace first 00 (prefix)
    str = str.replaceFirst("\\+", ""); // replace first + for country code
    str = str.replaceAll("\\(0\\)", "");
    str = str.replaceAll("\\(", "");
    str = str.replaceAll("\\)", "");
    str = str.replaceAll("\\s+|-+|\\\\|/|\\.", "@"); // seperator
    return str;
  }

  public static PhoneNumberStructure parseSimple(final String phoneNumber) {
    final String[] parts = phoneNumber.split(" ");
    final PhoneNumberStructure structure = new PhoneNumberStructure();
    structure.setCountryCode(parts[0]);
    structure.setOnkz(parts[1]);
    structure.setNumber(parts[2]);
    if (parts.length == 4) {
      structure.setExtension(parts[3]);
    }
    return structure;
  }
}
