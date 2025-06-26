package at.a1ta.cuco.core.dao.db;

import java.math.BigDecimal;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.bite.data.solr.core.query.Field;
import at.a1ta.bite.data.solr.core.query.result.FacetResult;
import at.a1ta.cuco.core.shared.dto.CustomerFilter;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartySearch;
import at.a1ta.cuco.core.shared.dto.SimplePage;
import at.a1ta.cuco.core.shared.dto.Tupel;

public interface PartyDao {
  List<Party> loadParties(List<Long> partyIds);

  Party loadParty(Long partyId);

  SimplePage<Party> search(PartySearch customerSearch, int maxResults);

  List<Party> getCustomers4Header(long headerId, int skip, int maxResults);

  int countCustomers4Header(long headerId);

  boolean isSubsidised(long customerId, String[] subsidisedTarifs);

  List<String> getAllSegments();

  void saveCucoCustomer(Party cucoCustomer);

  List<Party> getHierarchyForParty(long partyId);

  List<FacetResult> facetedSearch(PartySearch customerSearch, Field facetField);

  int loadNumberOfCustomersForSupportUser(String uUser);

  int loadNumberOfCustomersWithChurnForSupportUser(String uUser);

  int loadNumberOfCustomersWithIndexationForSupportUser(String uUser);

  int loadNumberOfCustomersWithFlashInfosForSupportUser(String uUser);

  int loadNumberOfCustomersWithVIPForSupportUser(String uUser);

  Map<BigDecimal, BigDecimal> loadNumberOfCustomersByTypeForSupportUser(String uUser);

  Map<String, BigDecimal> loadNumberOfCustomersByWorthclassForSupportUser(String uUser);

  List<Tupel<Long, BigDecimal>> loadNumberOfCustomersTurnoverForSupportUser(String uUser);

  List<Long> getCustomerIdsForSupportUser(String uUser);

  SearchResult<Party> filterCustomersForSupportUser(CustomerFilter customerFilter, String username);

  List<Party> filterCustomersForSupportUserUnlimited(CustomerFilter customerFilter, String uUser);

  List<Party> loadPartiesOfFlashInfo(Long flashInfoId, String username);

  SimplePage<Party> searchNonCustomer(PartySearch partySearch, int maxResults);

  void insertNonCustomerContact(Party party);

  void markNonCustomerMerged(Party party);

  void mergeNonCustomerAndTransferOffers(Party party);

  SimplePage<Party> searchNonCustomerFull(PartySearch partySearch, int maxResults);

  int loadNumberOfCustomersWithVBMForSupportUser(String uUser);

  String getPartyIdForQuoteNumber(String offerNumber);

}
