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

import java.util.List;

import at.a1ta.cuco.core.shared.dto.ContactPerson;

public interface ContactPersonService {

  /**
   * Get list of contact persons for customer with given id
   * 
   * @param customerId
   *          The id of the customer to get the contacts for
   * @return empty list if no data found
   */
  List<ContactPerson> listContactPersons(List<Long> partyIds);

  void insertLocalContact(ContactPerson contact);

  void updateLocalContact(ContactPerson contact);

  void updateLocalContactStatus(ContactPerson contact);

  void updateDWHContactStatus(ContactPerson contact);

  void deleteLocalContact(ContactPerson contact);

  void markLocalContactDeleted(ContactPerson contact);

  List<ContactPerson> listContactPersonsIncludingDeleted(List<Long> partyIds);

  Boolean checkIfReferenceExists(Long partyId, Long id);

}
