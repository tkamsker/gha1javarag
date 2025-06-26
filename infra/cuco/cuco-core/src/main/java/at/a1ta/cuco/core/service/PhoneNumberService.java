/*
 * Copyright 2009 - 2012 by A1 Telekom Austria AG
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
package at.a1ta.cuco.core.service;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.BillingAccountNumber;
import at.a1ta.cuco.core.shared.dto.MobileChurnLikeliness;
import at.a1ta.cuco.core.shared.dto.PhoneNumber;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

public interface PhoneNumberService {

  /**
   * Geth the list of phonenumbers owned by a customer
   * 
   * @param customerId The id of the customer to get the number for
   * @return empty list if no data found
   */
  List<PhoneNumber> listPhoneNumbers4Customer(Number customerId);

  /**
   * Get the list of phonenumber owned by given customer with given contract
   * 
   * @param customerId The id of the customer to get the number for
   * @param contractId The contract assigned to the number
   * @return empty list if no data found
   */
  List<PhoneNumber> listPhoneNumbers4Customer(Number customerId, Number contractId);

  /**
   * Get the list of phonenumbers owned by given customer
   * 
   * @param customerId The id of the customer to get the number for
   * @param contractId The contract assigned to the number
   * @param locationId The location the phone is settled
   * @return empty list if no data found
   */
  List<PhoneNumber> listPhoneNumbers4Customer(Number customerId, Number contractId, Number locationId);

  /**
   * Get the list of phonenumbers owned by given customer
   * 
   * @param customerId The id of the customer to get the number for
   * @param contractId The contract assigned to the number
   * @param locationId The location the phone is settled
   * @param skip The number of entries to be skipped at the beginning of the result
   * @param maxResults The total number of items to be contained in result
   * @return empty list if no data found
   */
  List<PhoneNumber> listPhoneNumbers4Customer(Number customerId, Number contractId, Number locationId, int skip, int maxResults);

  /**
   * Get the list of phonenumbers for a given location
   * 
   * @param locationId The if of the location the number is settled at
   * @return empty list if no data found
   */
  List<PhoneNumber> listPhoneNumbers4Location(Number locationId);

  /**
   * Get the list of phonenumbers for a given location owned by a given customer
   * 
   * @param locationId The if of the location the number is settled at
   * @param customerId The id of the customer to get the number for
   * @return empty list if no data found
   */
  List<PhoneNumber> listPhoneNumbers4Location(Number locationId, Number customerId);

  /**
   * Get the list of phonenumbers for a given contract
   * 
   * @param contractId The id of the contract the number belongs to
   * @return empty list if no data found
   */
  List<PhoneNumber> listPhoneNumbers4Contract(Number contractId);

  PhoneNumberStructure parse(final String input);

  List<BillingAccountNumber> getBillingAccountNumbersForParty(long partyId);

  Long getBillingAccountNumberForPhoneNumber(String countryCode, String onkz, String number);

  ArrayList<String> getPhoneNumbersForClearingAccountId(long clearingAccountId);

  List<PhoneNumber> getPhoneNumbersForBillingAccountNumber(BillingAccountNumber ban);

  List<MobileChurnLikeliness> getMobileChurnLikelinessForParty(long partyId);

}
