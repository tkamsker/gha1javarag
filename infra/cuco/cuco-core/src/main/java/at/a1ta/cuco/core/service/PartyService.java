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

import at.a1ta.bite.data.solr.core.query.Field;
import at.a1ta.bite.data.solr.core.query.result.FacetResult;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartyAdditionalInfo;
import at.a1ta.cuco.core.shared.dto.PartySearch;
import at.a1ta.cuco.core.shared.dto.SimplePage;

public interface PartyService {

  Party get(long id);

  SimplePage<Party> search(PartySearch customerSearch);

  /**
   * Get the list of customers assigned to a given header<br />
   * <b>Note:</b> if headerId == customerId the result will be same customer as requested
   * 
   * @param headerId The id of the header the customers are assigned to
   * @return empty list if no data found
   */
  List<Party> getCustomers4Header(Number headerId);

  /**
   * Get the list of customers assigned to a given header<br />
   * <b>Note:</b> if headerId == customerId the result will be same customer as requested
   * 
   * @param headerId The id of the header the customers are assigned to
   * @param skip The number of entries to be skipped at the beginning of the result
   * @param maxResults The total number of items to be contained in result
   * @return empty list if no data found
   */
  List<Party> getCustomers4Header(Number headerId, int skip, int maxResults);

  int countCustomers4Header(Long headerId);

  boolean isSubsidised(long customerId);

  List<String> getAllSegments();

  Party getHierarchyForParty(long partyId);

  List<FacetResult> facetedSearch(PartySearch partySearch, Field facetedField);

  boolean isIndexedSearchEnabled();

  SimplePage<Party> searchNonCustomers(PartySearch partySearch);

  void saveNonCustomer(Party party);

  void mergeNonCustomerAndTransferOffers(Party party);

  PartyAdditionalInfo getPartyAdditionalInfo(long partyId, String userName);

  PartyAdditionalInfo getPartyAdditionalInfo(long partyId);

  String getPartyIdForQuoteNumber(String offerNumber);
}
