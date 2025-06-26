package at.a1ta.cuco.core.dao.solr;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.junit.Before;
import org.junit.Test;
import org.mockito.ArgumentCaptor;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

import at.a1ta.bite.data.solr.core.query.Query;
import at.a1ta.cuco.core.dao.db.PhoneNumberDao;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PartySearch;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

public class SolrPartyRepositoryWithPhoneNumbersTest extends AbstractSolrRepositoryTest {

  private SolrPartyRepositoryWithPhoneNumbers repository;
  private Page<Party> page;

  @Mock
  private PhoneNumberDao phoneNumberDaoMock;

  @Before
  public void setUp() {
    repository = new SolrPartyRepositoryWithPhoneNumbers();
    initMockedRepository(repository);

    repository.setPhoneNumberDao(phoneNumberDaoMock);

    page = new PageImpl<Party>(Collections.<Party> emptyList());
    Mockito.when(solrTemplateMock.executeObjectQuery(Matchers.any(Query.class), Matchers.eq(Party.class))).thenReturn(new Party());
    Mockito.when(solrTemplateMock.executeListQuery(Matchers.any(Query.class), Matchers.eq(Party.class))).thenReturn(page);
  }

  @Test
  public void testSearch() {
    PartySearch partySearch = new PartySearch();
    partySearch.setLastName("lastname");

    repository.search(partySearch, 300);
    ArgumentCaptor<Query> queryCaptor = ArgumentCaptor.forClass(Query.class);

    Mockito.verify(solrTemplateMock, Mockito.times(1)).executeListQuery(queryCaptor.capture(), Matchers.eq(Party.class));
    assertEquals(300, queryCaptor.getValue().getPageRequest().getPageSize());
    assertEquals(0, queryCaptor.getValue().getPageRequest().getPageNumber());
  }

  @Test
  public void testSearchPhoneNumberNotParsable() {
    PartySearch customerSearch = new PartySearch();
    String phoneNumber = "789789";
    customerSearch.setPhoneNumber(phoneNumber);

    Mockito.when(phoneNumberDaoMock.parse(phoneNumber)).thenReturn(null);
    Page<Party> page = repository.search(customerSearch, new PageRequest(0, 10));

    Mockito.verify(phoneNumberDaoMock, Mockito.times(1)).parse(Matchers.eq(phoneNumber));
    assertNull(customerSearch.getLkz());
    assertNull(customerSearch.getOkz());
    assertNull(customerSearch.getCallNumber());
    assertEquals(0, page.getTotalElements());
  }

  @Test
  public void testSearchPhoneNumberParsable() {
    PartySearch customerSearch = new PartySearch();
    String phoneNumber = "789789";
    customerSearch.setPhoneNumber(phoneNumber);

    Mockito.when(phoneNumberDaoMock.parse(Matchers.eq(phoneNumber))).thenReturn(new PhoneNumberStructure("TestCode", "TestOnkz", "TestNumber"));
    Page<Party> page = repository.search(customerSearch, new PageRequest(0, 10));

    Mockito.verify(phoneNumberDaoMock, Mockito.times(1)).parse(Matchers.eq(phoneNumber));
    assertEquals(customerSearch.getLkz(), "TestCode");
    assertEquals(customerSearch.getOkz(), "TestOnkz");
    assertEquals(customerSearch.getCallNumber(), "TestNumber");
    assertEquals(0, page.getTotalElements()); // nothing will be found anyway
  }

  @Test
  public void testRemoveDuplicates() {
    ArrayList<Party> parties = new ArrayList<Party>();
    parties.add(new Party(1));
    parties.add(new Party(2));
    parties.add(new Party(1));

    List<Party> filtered = repository.removeDuplicates(parties);
    assertEquals(2, filtered.size());
  }

  @Test
  public void testRippleLoad() {
    PartySearch partySearch = new PartySearch();
    partySearch.setLastName("lastname");

    page = new PageImpl<Party>(Arrays.asList(new Party(1), new Party(1)));
    Mockito.when(solrTemplateMock.executeListQuery(Matchers.any(Query.class), Matchers.eq(Party.class))).thenReturn(page);

    repository.search(partySearch, 2);
    ArgumentCaptor<Query> queryCaptor = ArgumentCaptor.forClass(Query.class);

    Mockito.verify(solrTemplateMock, Mockito.times(1)).executeListQuery(queryCaptor.capture(), Matchers.eq(Party.class));
  }

  @Test
  public void testRippleLoadWithTrim() {
    PartySearch partySearch = new PartySearch();
    partySearch.setLastName("lastname");

    page = new PageImpl<Party>(Arrays.asList(new Party(1), new Party(2), new Party(3)));
    Mockito.when(solrTemplateMock.executeListQuery(Matchers.any(Query.class), Matchers.eq(Party.class))).thenReturn(page);

    List<Party> result = repository.search(partySearch, 2).getContent();
    ArgumentCaptor<Query> queryCaptor = ArgumentCaptor.forClass(Query.class);

    Mockito.verify(solrTemplateMock, Mockito.times(1)).executeListQuery(queryCaptor.capture(), Matchers.eq(Party.class));
    assertEquals(2, result.size());

  }

}
