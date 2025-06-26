package at.a1ta.cuco.core.dao.solr;

import java.util.Collections;

import junit.framework.Assert;

import org.apache.commons.lang.NotImplementedException;
import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.Matchers;
import org.mockito.Mockito;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;

import at.a1ta.bite.data.solr.core.query.Query;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartySearch;

public class SolrPartyRepositoryTest extends AbstractSolrRepositoryTest {

  private SolrPartyRepository repository;
  
  @Before
  public void setUp() {
    repository = new SolrPartyRepository();
    initMockedRepository(repository);
    
    Page<Party> page = new PageImpl<Party>(Collections.<Party>emptyList());
    Mockito.when(solrTemplateMock.executeObjectQuery(Matchers.any(Query.class), Matchers.eq(Party.class))).thenReturn(new Party());
    Mockito.when(solrTemplateMock.executeListQuery(Matchers.any(Query.class), Matchers.eq(Party.class))).thenReturn(page);
  }
  
  
  @Test
  public void testFindOne()  {
    repository.findOne(Long.valueOf(1));
    ArgumentCaptor<Query> queryCaptor = ArgumentCaptor.forClass(Query.class);
    Mockito.verify(solrTemplateMock, Mockito.times(1)).executeObjectQuery(queryCaptor.capture(), Matchers.eq(Party.class));
    
    Assert.assertEquals("customernumber:1", queryCaptor.getValue().getQueryString());
  }
  
  @Test
  public void testLoadParty()  {
    repository.loadParty(Long.valueOf(1));
    ArgumentCaptor<Query> queryCaptor = ArgumentCaptor.forClass(Query.class);
    Mockito.verify(solrTemplateMock, Mockito.times(1)).executeObjectQuery(queryCaptor.capture(), Matchers.eq(Party.class));
    
    Assert.assertEquals("customernumber:1", queryCaptor.getValue().getQueryString());
  }
  
  @Test(expected=IllegalArgumentException.class)
  public void testFindOneWithNullValue()  {
    repository.findOne(null);
  }
  
  @Test(expected=IllegalArgumentException.class)
  public void testLoadPartyWithNull()  {
    repository.loadParty(null);
  }
  
  @Test
  public void testSearch() {
    PartySearch partySearch = new PartySearch();
    partySearch.setLastName("lastname");
    
    repository.search(partySearch, 300);
    ArgumentCaptor<Query> queryCaptor = ArgumentCaptor.forClass(Query.class);
    
    Mockito.verify(solrTemplateMock, Mockito.times(1)).executeListQuery(queryCaptor.capture(), Matchers.eq(Party.class));
    Assert.assertEquals(300, queryCaptor.getValue().getPageRequest().getPageSize());
    Assert.assertEquals(0, queryCaptor.getValue().getPageRequest().getPageNumber());
  }
  
  @Test(expected=IllegalArgumentException.class)
  public void testSearchWithNullParameter() {
    repository.search(null, 300);
  }
  
  @Test
  public void testFacetedSearch() {
    PartySearch partySearch = new PartySearch();
    partySearch.setLastName("lastname");
    
    repository.facetedSearch(partySearch, SolrPartyQuery.SearchField.FIRSTNAME);
    ArgumentCaptor<Query> queryCaptor = ArgumentCaptor.forClass(Query.class);
    
    Mockito.verify(solrTemplateMock, Mockito.times(1)).executeFacetQuery(queryCaptor.capture());
    Assert.assertEquals(SolrPartyQuery.SearchField.FIRSTNAME, queryCaptor.getValue().getFacets().get(0));
  }
  
  @Test(expected=IllegalArgumentException.class)
  public void testFacetedSearchWithNullField() {
    PartySearch partySearch = new PartySearch();
    partySearch.setLastName("lastname");
    
    repository.facetedSearch(partySearch, null);
  }
  
  @Test(expected=NotImplementedException.class)
  public void testGetCustomers4Header() {
    repository.getCustomers4Header(1, 1, 1);
  }
  
  @Test(expected=NotImplementedException.class)
  public void testCountCustomers4Header() {
    repository.countCustomers4Header(1);
  }
  
  @Test(expected=NotImplementedException.class)
  public void testIsSubsidised() {
    repository.isSubsidised(1, null);
  }
  
  @Test(expected=NotImplementedException.class)
  public void testGetAllSegments() {
    repository.getAllSegments();
  }
  
  @Test(expected=NotImplementedException.class)
  public void testSaveCucoCustomer() {
    repository.saveCucoCustomer(null);
  }
  
  @Test(expected=NotImplementedException.class)
  public void testGetHierarchyForParty() {
    repository.getHierarchyForParty(1);
  }
  
  
}
