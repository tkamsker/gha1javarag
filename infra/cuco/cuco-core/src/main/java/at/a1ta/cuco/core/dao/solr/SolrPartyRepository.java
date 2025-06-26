package at.a1ta.cuco.core.dao.solr;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.commons.lang.NotImplementedException;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.util.Assert;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.bite.data.solr.core.query.BasicQuery;
import at.a1ta.bite.data.solr.core.query.Criteria;
import at.a1ta.bite.data.solr.core.query.Field;
import at.a1ta.bite.data.solr.core.query.Query;
import at.a1ta.bite.data.solr.core.query.result.FacetResult;
import at.a1ta.bite.data.solr.repository.support.SimpleSolrRepository;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.shared.dto.CustomerFilter;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartySearch;
import at.a1ta.cuco.core.shared.dto.SimplePage;
import at.a1ta.cuco.core.shared.dto.Tupel;

import com.codahale.metrics.annotation.Metered;

public class SolrPartyRepository extends SimpleSolrRepository<Party, Long> implements PartyDao {

  private static final int FACET_LIMIT = 5;

  @Override
  public List<Party> loadParties(List<Long> partyIds) {
    Query query = SolrPartyQueryHelper.convertToFindCustomersByIdQuery(partyIds);
    return getSolrTemplate().executeListQuery(query, Party.class).getContent();
  }

  @Override
  public Party findOne(Long id) {
    return loadParty(id);
  }

  @Override
  @Metered(name = "CustomerLoad", absolute = true)
  public Party loadParty(Long partyId) {
    Assert.notNull(partyId);
    return getSolrTemplate().executeObjectQuery(new BasicQuery(new Criteria(SolrPartyQuery.SearchField.CUSTOMER_NUMBER).is(partyId)), Party.class);
  }

  @Override
  @Metered(name = "CustomerSearch", absolute = true)
  public SimplePage<Party> search(PartySearch customerSearch, int maxResults) {
    Page<Party> page = search(customerSearch, new PageRequest(0, maxResults));

    ArrayList<Party> list = new ArrayList<Party>();
    list.addAll(page.getContent());

    SimplePage<Party> result = new SimplePage<Party>();
    result.setContent(list);
    result.setCount(page.getTotalElements());
    return result;
  }

  public Page<Party> search(PartySearch customerSearch, Pageable pageable) {
    Query query = SolrPartyQueryHelper.convertToQuery(customerSearch);
    query.setPageRequest(pageable);
    return getSolrTemplate().executeListQuery(query, Party.class);
  }

  @Override
  public List<FacetResult> facetedSearch(PartySearch customerSearch, Field facetField) {
    Query query = SolrPartyQueryHelper.convertToQuery(customerSearch);
    query.addFacetField(facetField);
    query.setFacetLimit(FACET_LIMIT);
    return getSolrTemplate().executeFacetQuery(query);
  }

  @Override
  public List<Party> getCustomers4Header(long headerId, int skip, int maxResults) {
    throw new NotImplementedException();
  }

  @Override
  public int countCustomers4Header(long headerId) {
    throw new NotImplementedException();
  }

  @Override
  public boolean isSubsidised(long customerId, String[] subsidisedTarifs) {
    throw new NotImplementedException();
  }

  @Override
  public List<String> getAllSegments() {
    throw new NotImplementedException();
  }

  @Override
  public void saveCucoCustomer(Party cucoCustomer) {
    throw new NotImplementedException();
  }

  @Override
  public List<Party> getHierarchyForParty(long partyId) {
    throw new NotImplementedException();
  }

  @Override
  public int loadNumberOfCustomersForSupportUser(String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public int loadNumberOfCustomersWithChurnForSupportUser(String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public int loadNumberOfCustomersWithFlashInfosForSupportUser(String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public int loadNumberOfCustomersWithVIPForSupportUser(String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public Map<BigDecimal, BigDecimal> loadNumberOfCustomersByTypeForSupportUser(String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public Map<String, BigDecimal> loadNumberOfCustomersByWorthclassForSupportUser(String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public List<Tupel<Long, BigDecimal>> loadNumberOfCustomersTurnoverForSupportUser(String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public List<Long> getCustomerIdsForSupportUser(String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public SearchResult<Party> filterCustomersForSupportUser(CustomerFilter customerFilter, String username) {
    throw new NotImplementedException();
  }

  @Override
  public List<Party> filterCustomersForSupportUserUnlimited(CustomerFilter customerFilter, String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public List<Party> loadPartiesOfFlashInfo(Long flashInfoId, String username) {
    throw new NotImplementedException();
  }

  @Override
  public SimplePage<Party> searchNonCustomer(PartySearch partySearch, int maxResults) {
    throw new NotImplementedException();
  }

  @Override
  public void insertNonCustomerContact(Party party) {
    throw new NotImplementedException();

  }

  @Override
  public void markNonCustomerMerged(Party party) {
    throw new NotImplementedException();
  }

  @Override
  public void mergeNonCustomerAndTransferOffers(Party party) {
    throw new NotImplementedException();
  }

  @Override
  public SimplePage<Party> searchNonCustomerFull(PartySearch partySearch, int maxResults) {
    throw new NotImplementedException();
  }

  @Override
  public int loadNumberOfCustomersWithIndexationForSupportUser(String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public int loadNumberOfCustomersWithVBMForSupportUser(String uUser) {
    throw new NotImplementedException();
  }

  @Override
  public String getPartyIdForQuoteNumber(String offerNumber) {
    throw new NotImplementedException();
  }

}
