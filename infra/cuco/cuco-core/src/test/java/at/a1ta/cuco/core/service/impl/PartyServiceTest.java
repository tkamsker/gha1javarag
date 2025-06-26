package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.server.dto.PartySearchEvent;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.server.service.UserTrackingService;
import at.a1ta.bite.data.solr.SolrApiUsageException;
import at.a1ta.bite.data.solr.core.query.BasicField;
import at.a1ta.bite.data.solr.core.query.Field;
import at.a1ta.bite.data.solr.core.query.result.BasicFacetResult;
import at.a1ta.bite.data.solr.core.query.result.FacetResult;
import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.dao.db.PhoneNumberDao;
import at.a1ta.cuco.core.service.PartySearchValueFormatHelper;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartySearch;
import at.a1ta.cuco.core.shared.dto.SimplePage;

@RunWith(MockitoJUnitRunner.class)
public class PartyServiceTest {

  private PartyServiceImpl customerService;

  private static final List<Party> SINGLE_PARTY_LIST = Arrays.asList(new Party(1l));
  private static final int NR_ENTRIES = 300;

  @Mock
  private PartyDao oraclePartyDaoMock;
  @Mock
  private PartyDao solrPartyRepositoryMock;
  @Mock
  private PartyDao solrPhoneRepositoryMock;
  @Mock
  private PhoneNumberDao phoneNumberDaoMock;

  @Mock
  private SettingService settingsServiceMock;
  
  @Mock
  private UserTrackingService userTrackingServiceMock;

  @Before
  public void setUp() {
    customerService = new PartyServiceImpl();

    Mockito.when(settingsServiceMock.getIntValue("Partysearch.maxResults", PartyServiceImpl.DEFAULT_MAX_ELEM)).thenReturn(NR_ENTRIES);
    Mockito.when(settingsServiceMock.getBooleanValue(PartyServiceImpl.PARTYSEARCH_SOLR_ENABLED, false)).thenReturn(true);
    Mockito.when(settingsServiceMock.getBooleanValue(PartyServiceImpl.PARTYSEARCH_SOLR_ENABLED, true)).thenReturn(true);

    Mockito.when(settingsServiceMock.getBooleanValue(PartyServiceImpl.FACETED_PARTYSEARCH_ENABLED, true)).thenReturn(true);

    customerService.setCustomerDao(oraclePartyDaoMock);
    customerService.setPartySolrRepository(solrPartyRepositoryMock);
    customerService.setPartySolrRepositoryWithPhoneNumbers(solrPhoneRepositoryMock);
    customerService.setSettingService(settingsServiceMock);
    customerService.setPartySearchFormatterHelper(new PartySearchValueFormatHelper(phoneNumberDaoMock));
    customerService.setUserTrackingService(userTrackingServiceMock);
  }

  @Test
  public void testPrimarySearch() {
    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setLastName("lastname");

    ArrayList<Party> list = new ArrayList<Party>();
    list.addAll(SINGLE_PARTY_LIST);

    SimplePage<Party> resultPage = new SimplePage<Party>();
    resultPage.setContent(list);
    Mockito.when(solrPartyRepositoryMock.search(searchCriteria, NR_ENTRIES)).thenReturn(resultPage);

    customerService.search(searchCriteria);

    Mockito.verify(solrPartyRepositoryMock, Mockito.times(1)).search(searchCriteria, NR_ENTRIES);
    Mockito.verifyZeroInteractions(oraclePartyDaoMock, solrPhoneRepositoryMock);
  }

  @Test
  public void testPrimarySearchWithNoResultFromSolr() {
    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setLastName("lastname");

    ArrayList<Party> list = new ArrayList<Party>();
    list.addAll(Collections.<Party> emptyList());

    SimplePage<Party> resultPage = new SimplePage<Party>();
    resultPage.setContent(list);
    Mockito.when(solrPartyRepositoryMock.search(searchCriteria, NR_ENTRIES)).thenReturn(resultPage);

    customerService.search(searchCriteria);

    Mockito.verify(solrPartyRepositoryMock, Mockito.times(1)).search(searchCriteria, NR_ENTRIES);
    Mockito.verify(oraclePartyDaoMock, Mockito.times(1)).search(searchCriteria, NR_ENTRIES);
    Mockito.verifyZeroInteractions(solrPhoneRepositoryMock);
  }

  @Test
  public void testPrimarySearchWithExceptionFromSolr() {
    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setLastName("lastname");

    Mockito.when(solrPartyRepositoryMock.search(searchCriteria, NR_ENTRIES)).thenThrow(new SolrApiUsageException());

    customerService.search(searchCriteria);

    Mockito.verify(solrPartyRepositoryMock, Mockito.times(1)).search(searchCriteria, NR_ENTRIES);
    Mockito.verify(oraclePartyDaoMock, Mockito.times(1)).search(searchCriteria, NR_ENTRIES);
    Mockito.verifyZeroInteractions(solrPhoneRepositoryMock);
  }

  @Test
  public void testBANSearch() {
    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setBillingAccountNumber("billingAccountNumber");

    ArrayList<Party> list = new ArrayList<Party>();
    list.addAll(SINGLE_PARTY_LIST);

    SimplePage<Party> resultPage = new SimplePage<Party>();
    resultPage.setContent(list);
    Mockito.when(solrPartyRepositoryMock.search(searchCriteria, NR_ENTRIES)).thenReturn(resultPage);

    customerService.search(searchCriteria);

    Mockito.verify(solrPhoneRepositoryMock, Mockito.times(1)).search(searchCriteria, NR_ENTRIES);
    Mockito.verifyZeroInteractions(solrPartyRepositoryMock);
  }

  @Test
  public void testAonAccountSearch() {
    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setAonAccountNumber("aonAccountNumber");

    ArrayList<Party> list = new ArrayList<Party>();
    list.addAll(SINGLE_PARTY_LIST);

    SimplePage<Party> resultPage = new SimplePage<Party>();
    resultPage.setContent(list);
    Mockito.when(oraclePartyDaoMock.search(searchCriteria, NR_ENTRIES)).thenReturn(resultPage);

    customerService.search(searchCriteria);

    Mockito.verify(oraclePartyDaoMock, Mockito.times(1)).search(searchCriteria, NR_ENTRIES);
    Mockito.verifyZeroInteractions(solrPartyRepositoryMock, solrPhoneRepositoryMock);
  }

  @Test
  public void testPhoneNumberSearch() {
    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setLkz("lkz");
    searchCriteria.setOkz("okz");
    searchCriteria.setCallNumber("callNumber");

    ArrayList<Party> list = new ArrayList<Party>();
    list.addAll(SINGLE_PARTY_LIST);

    SimplePage<Party> resultPage = new SimplePage<Party>();
    resultPage.setContent(list);
    Mockito.when(solrPhoneRepositoryMock.search(searchCriteria, NR_ENTRIES)).thenReturn(resultPage);

    customerService.search(searchCriteria);

    Mockito.verify(solrPhoneRepositoryMock, Mockito.times(1)).search(searchCriteria, NR_ENTRIES);
    Mockito.verifyZeroInteractions(solrPartyRepositoryMock, oraclePartyDaoMock);
  }

  @Test
  public void testFacetedSearch() {
    Field facetField = new BasicField("lastname_ci");
    FacetResult result = new BasicFacetResult(facetField.getName(), "lastname", 1);
    List<FacetResult> resultList = Arrays.asList(result);

    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setLastName("lastname");
    searchCriteria.setActiveSearchField(facetField.getName());

    Mockito.when(solrPartyRepositoryMock.facetedSearch(searchCriteria, facetField)).thenReturn(resultList);

    customerService.facetedSearch(searchCriteria, facetField);

    Mockito.verify(solrPartyRepositoryMock, Mockito.times(1)).facetedSearch(searchCriteria, facetField);
    Mockito.verifyZeroInteractions(oraclePartyDaoMock, solrPhoneRepositoryMock);
  }

  @Test
  public void testFacetedSearchWithExceptionFromSolr() {
    Field facetField = new BasicField("lastname");

    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setLastName("lastname");
    searchCriteria.setActiveSearchField(facetField.getName());

    Mockito.when(solrPartyRepositoryMock.facetedSearch(searchCriteria, facetField)).thenThrow(new SolrApiUsageException());

    customerService.facetedSearch(searchCriteria, facetField);

    Mockito.verify(solrPartyRepositoryMock, Mockito.times(1)).facetedSearch(searchCriteria, facetField);
    Mockito.verifyZeroInteractions(oraclePartyDaoMock, solrPhoneRepositoryMock);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testFacetedSearchWithNoActiveField() {
    Field facetField = null;

    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setLastName("lastname");

    customerService.facetedSearch(searchCriteria, facetField);

    Mockito.verify(solrPartyRepositoryMock, Mockito.times(1)).facetedSearch(searchCriteria, facetField);
    Mockito.verifyZeroInteractions(solrPartyRepositoryMock, oraclePartyDaoMock, solrPhoneRepositoryMock);
  }

  @Test
  public void testPrimarySearchConstraints() {
    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setLastName("la");

    SimplePage<Party> resultPage = new SimplePage<Party>();
    Mockito.when(solrPartyRepositoryMock.search(searchCriteria, NR_ENTRIES)).thenReturn(resultPage);

    SimplePage<Party> result = customerService.search(searchCriteria);

    Mockito.verify(solrPartyRepositoryMock, Mockito.times(1)).search(searchCriteria, NR_ENTRIES);
    Mockito.verifyZeroInteractions(oraclePartyDaoMock, solrPhoneRepositoryMock);
    Assert.assertFalse(result.isInputValid());
  }
  
  
  @Test
  public void testSearchTrackingWithSolrResultAvailable() {
    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setLastName("lastname");
    searchCriteria.setSearchExecutingUserName("myUsername");

    ArrayList<Party> list = new ArrayList<Party>();
    list.addAll(SINGLE_PARTY_LIST);

    SimplePage<Party> resultPage = new SimplePage<Party>();
    resultPage.setContent(list);
    Mockito.when(solrPartyRepositoryMock.search(searchCriteria, NR_ENTRIES)).thenReturn(resultPage);

    customerService.search(searchCriteria);
    
    ArgumentCaptor<PartySearchEvent> captor = ArgumentCaptor.forClass(PartySearchEvent.class);

    Mockito.verify(userTrackingServiceMock, Mockito.times(1)).trackUserEvent(captor.capture());
    
    Assert.assertEquals(searchCriteria.getSearchExecutingUserName(), captor.getValue().getUserName());
    Assert.assertEquals("SEARCH_SOL", captor.getValue().getEventName());
  }
  
  @Test
  public void testSearchTrackingWithDatabaseFallback() {
    PartySearch searchCriteria = new PartySearch();
    searchCriteria.setLastName("lastname");
    searchCriteria.setSearchExecutingUserName("myUsername");

    ArrayList<Party> list = new ArrayList<Party>();

    SimplePage<Party> resultPage = new SimplePage<Party>();
    resultPage.setContent(list);
    Mockito.when(solrPartyRepositoryMock.search(searchCriteria, NR_ENTRIES)).thenReturn(resultPage);

    customerService.search(searchCriteria);
    
    ArgumentCaptor<PartySearchEvent> captor = ArgumentCaptor.forClass(PartySearchEvent.class);

    Mockito.verify(userTrackingServiceMock, Mockito.times(2)).trackUserEvent(captor.capture());
    List<PartySearchEvent> values = captor.getAllValues();
    Assert.assertEquals(searchCriteria.getSearchExecutingUserName(), captor.getValue().getUserName());
    Assert.assertEquals("SEARCH_SOL", values.get(0).getEventName());
    Assert.assertEquals("SEARCH_FB", values.get(1).getEventName());
  }
  
  @Test
  public void testSearchTrackingWithFulltextSearch() {
      PartySearch searchCriteria = new PartySearch();
      searchCriteria.setFulltextTerm("fulltextTerm");
      searchCriteria.setFulltext(true);

      ArrayList<Party> list = new ArrayList<Party>();

      SimplePage<Party> resultPage = new SimplePage<Party>();
      resultPage.setContent(list);
      Mockito.when(solrPartyRepositoryMock.search(searchCriteria, NR_ENTRIES)).thenReturn(resultPage);

      customerService.search(searchCriteria);
      
      ArgumentCaptor<PartySearchEvent> captor = ArgumentCaptor.forClass(PartySearchEvent.class);

      Mockito.verify(userTrackingServiceMock, Mockito.times(1)).trackUserEvent(captor.capture());

      Assert.assertEquals(searchCriteria.getSearchExecutingUserName(), captor.getValue().getUserName());
      Assert.assertEquals("SEARCH_FT", captor.getValue().getEventName());
  }
  
}
