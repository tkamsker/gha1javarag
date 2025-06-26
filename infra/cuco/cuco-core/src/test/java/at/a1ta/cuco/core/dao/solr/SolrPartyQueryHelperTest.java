package at.a1ta.cuco.core.dao.solr;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

import org.apache.commons.lang.StringUtils;
import org.junit.Assert;
import org.junit.Test;

import at.a1ta.bite.data.solr.core.query.Field;
import at.a1ta.bite.data.solr.core.query.Query;
import at.a1ta.cuco.core.shared.dto.PartySearch;

public class SolrPartyQueryHelperTest {

  @Test
  public void testConvertToQueryWithEmptyCriteria() {
    Query query = SolrPartyQueryHelper.convertToQuery(new PartySearch());
    Assert.assertNotNull(query);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testConvertToQueryWithNullCriteria() {
    SolrPartyQueryHelper.convertToQuery(null);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testConvertToQueryWithAonAccountNumber() {
    PartySearch partySearch = new PartySearch();
    partySearch.setAonAccountNumber("aonNumber");
    SolrPartyQueryHelper.convertToQuery(partySearch);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testConvertToFindCustomersByIdQueryWithNullValue() {
    SolrPartyQueryHelper.convertToFindCustomersByIdQuery(null);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testConvertToFindCustomersByIdQueryWithEmptyList() {
    SolrPartyQueryHelper.convertToFindCustomersByIdQuery(Collections.<Long> emptyList());
  }

  @Test
  public void testToFindCustomersByIdQueryWithSingleId() {
    List<Long> ids = Arrays.asList(Long.valueOf(1));
    Query query = SolrPartyQueryHelper.convertToFindCustomersByIdQuery(ids);
    assertQueryField(SolrPartyQuery.SearchField.CUSTOMER_NUMBER, Long.valueOf(1), query);
  }

  @Test
  public void testToFindCustomersByIdQueryWithMultipleIds() {
    List<Long> ids = Arrays.asList(Long.valueOf(1), Long.valueOf(2), Long.valueOf(3));
    Query query = SolrPartyQueryHelper.convertToFindCustomersByIdQuery(ids);

    assertQueryField(SolrPartyQuery.SearchField.CUSTOMER_NUMBER, Long.valueOf(1), query);
    assertQueryField(SolrPartyQuery.SearchField.CUSTOMER_NUMBER, Long.valueOf(2), query);
    assertQueryField(SolrPartyQuery.SearchField.CUSTOMER_NUMBER, Long.valueOf(3), query);

    Assert.assertTrue(query.getQueryString().contains(" OR "));
    Assert.assertFalse(query.getQueryString().contains(" AND "));
  }

  @Test
  public void testConvertToQueryWithMultipleCriterias() {
    // incrementally add new parameters and verify result
    PartySearch partySearch = new PartySearch();

    partySearch.setFirstName("firstname");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setLastName("lastname");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setStreet("street");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setPostcode("postcode");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setHouseNumber("housenumber");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setCity("city");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setId("customernumber");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setBillingAccountNumber("billingaccountnumber");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setCallNumber("callNumber");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setOkz("okz");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setLkz("lkz");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);

    partySearch.setCommercialRegisterNumber("commercialRegisterNumber");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);
  }

  @Test
  public void testConvertToQueryWithMultiValuedFields() {
    PartySearch partySearch = new PartySearch();

    partySearch.setFirstName("ANNA   MARIA");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);
  }

  @Test
  public void testConvertToQueryWithFulltext() {
    PartySearch partySearch = new PartySearch();
    partySearch.setFulltext(true);
    partySearch.setFulltextTerm("huber al");
    validateQuery(SolrPartyQueryHelper.convertToQuery(partySearch), partySearch);
  }

  @Test
  public void testConvertToQueryWithBlankFulltext() {
    PartySearch partySearch = new PartySearch();
    partySearch.setFulltext(true);
    partySearch.setFulltextTerm("   ");
    Query query = SolrPartyQueryHelper.convertToQuery(partySearch);
    Assert.assertTrue(query.getQueryString().equals("*:*"));
  }

  @Test
  public void testConvertToQueryWithSpecialCharacters() {
    PartySearch partySearch = new PartySearch();
    partySearch.setFulltext(true);
    partySearch.setFulltextTerm("huber & al");
    Query query = SolrPartyQueryHelper.convertToQuery(partySearch);
    Assert.assertTrue(query.getQueryString().contains("(huber* al*)"));
  }

  @Test
  public void testReservedCharacterReplacementForSearch() {
    validateReservedCharacterReplacement("i_j", "i j");
    validateReservedCharacterReplacement("i/j", "i j");
    validateReservedCharacterReplacement("i%j", "i j");
    validateReservedCharacterReplacement("i;j", "i j");
    validateReservedCharacterReplacement("i'j", "i j");
    validateReservedCharacterReplacement("i#j", "i j");
    validateReservedCharacterReplacement("i@j", "i j");
    validateReservedCharacterReplacement("i,j", "i j");
    validateReservedCharacterReplacement("i.j", "i j");
    validateReservedCharacterReplacement("i\"j", "i j");
    validateReservedCharacterReplacement("i+j", "i j");
    validateReservedCharacterReplacement("i-j", "i j");
    validateReservedCharacterReplacement("i&j", "i j");
    validateReservedCharacterReplacement("i|j", "i j");
    validateReservedCharacterReplacement("i!j", "i j");
    validateReservedCharacterReplacement("i(j", "i j");
    validateReservedCharacterReplacement("i)j", "i j");
    validateReservedCharacterReplacement("i{j", "i j");
    validateReservedCharacterReplacement("i}j", "i j");
    validateReservedCharacterReplacement("i[j", "i j");
    validateReservedCharacterReplacement("i]j", "i j");
    validateReservedCharacterReplacement("i^j", "i j");
    validateReservedCharacterReplacement("i~j", "i j");
    validateReservedCharacterReplacement("i*j", "i j");
    validateReservedCharacterReplacement("i?j", "i j");
    validateReservedCharacterReplacement("i:j", "i j");
    validateReservedCharacterReplacement("i\\j", "i j");
  }

  @Test
  public void testReplaceSingleCustomerNumbersAtBeginningForFulltextSearch() {
    validateReseredCharacterReplacement("1 i", "i", true);
    validateReseredCharacterReplacement("10 i", "i", true);
    validateReseredCharacterReplacement("100 i", "i", true);
  }

  @Test
  public void testReplaceMultipleCustomerNumbersAtBeginningForFulltextSearch() {
    validateReseredCharacterReplacement("1 100 i", "i", true);
    validateReseredCharacterReplacement("10 10 i", "i", true);
    validateReseredCharacterReplacement("100 1 i", "i", true);
  }

  @Test
  public void testReplaceSingleCustomerNumbersInMiddleForFulltextSearch() {
    validateReseredCharacterReplacement("i 1 j", "i j", true);
    validateReseredCharacterReplacement("i 10 j", "i j", true);
    validateReseredCharacterReplacement("i 100 j", "i j", true);
  }

  public void testReplaceMultipleCustomerNumbersInMiddleForFulltextSearch() {
    validateReseredCharacterReplacement("i 1 1 j", "i j", true);
    validateReseredCharacterReplacement("i 10 10 j", "i j", true);
    validateReseredCharacterReplacement("i 100 100 j", "i j", true);

    validateReseredCharacterReplacement("i 1 100 j", "i j", true);
    validateReseredCharacterReplacement("i 10 10 j", "i j", true);
    validateReseredCharacterReplacement("i 100 1 j", "i j", true);
  }

  @Test
  public void testReplaceSingleCustomerNumbersAtEndForFulltextSearch() {
    validateReseredCharacterReplacement("i 1", "i", true);
    validateReseredCharacterReplacement("i 10", "i", true);
    validateReseredCharacterReplacement("i 100", "i", true);
  }

  @Test
  public void testReplaceMultipleCustomerNumbersAtEndForFulltextSearch() {
    validateReseredCharacterReplacement("i 1 100", "i", true);
    validateReseredCharacterReplacement("i 10 10", "i", true);
    validateReseredCharacterReplacement("i 100 1", "i", true);
  }

  @Test
  public void testReplaceSoleCustomerNumber() {
    validateReseredCharacterReplacement("1", "*:*", true);
    validateReseredCharacterReplacement("10", "*:*", true);
    validateReseredCharacterReplacement("100", "*:*", true);

    validateReseredCharacterReplacement("1 100", "*:*", true);
    validateReseredCharacterReplacement("10 10", "*:*", true);
    validateReseredCharacterReplacement("100 1", "*:*", true);
  }

  @Test
  public void testDontReplaceCustomerNumber() {
    validateReseredCharacterReplacement("1000", "1000", true);
    validateReseredCharacterReplacement("1001", "1001", true);
    validateReseredCharacterReplacement("2", "2", true);
    validateReseredCharacterReplacement("11", "11", true);
    validateReseredCharacterReplacement("101", "101", true);
  }

  private void validateReservedCharacterReplacement(String character, String expectedQuery) {
    validateReseredCharacterReplacement(character, expectedQuery, false);
  }

  private void validateReseredCharacterReplacement(String searchString, String expectedQuery, boolean isFulltext) {
    PartySearch partySearch = new PartySearch();
    if (isFulltext) {
      partySearch.setFulltext(true);
      partySearch.setFulltextTerm(searchString);
    } else {
      partySearch.setLastName(searchString);
    }
    Query query = SolrPartyQueryHelper.convertToQuery(partySearch);
    if (StringUtils.isBlank(expectedQuery)) {
      Assert.assertTrue("Expecined to replace '" + searchString + "' with '" + expectedQuery + "' .", query.getQueryString()
          .contains("*:*"));
    } else {
      String[] replacements = StringUtils.split(expectedQuery);
      Assert.assertTrue("Expecined to replace '" + searchString + "' with '" + expectedQuery + "' .",
          query.getQueryString().contains(StringUtils.join(replacements, "* ")));
    }
  }

  private void validateQuery(Query query, PartySearch partySearch) {
    assertQueryField(SolrPartyQuery.SearchField.FIRSTNAME, partySearch.getFirstName(), query);
    assertQueryField(SolrPartyQuery.SearchField.LASTNAME, partySearch.getLastName(), query);
    assertQueryField(SolrPartyQuery.SearchField.STREET, partySearch.getStreet(), query);
    assertQueryField(SolrPartyQuery.SearchField.POSTCODE, partySearch.getPostcode(), query);
    assertQueryField(SolrPartyQuery.SearchField.HOUSENUMBER, partySearch.getHouseNumber(), query);
    assertQueryField(SolrPartyQuery.SearchField.CITY, partySearch.getCity(), query);
    assertQueryField(SolrPartyQuery.SearchField.CUSTOMER_NUMBER, partySearch.getId(), query);
    assertQueryField(SolrPartyQuery.SearchField.BAN, partySearch.getBillingAccountNumber(), query);
    assertQueryField(SolrPartyQuery.SearchField.PHONE_SUBSCRIBER_NUMBER, partySearch.getCallNumber(), query);
    assertQueryField(SolrPartyQuery.SearchField.PHONE_DESTINATION_CODE, partySearch.getOkz(), query);
    assertQueryField(SolrPartyQuery.SearchField.PHONE_COUNTRY_CODE, partySearch.getLkz(), query);
    assertQueryField(SolrPartyQuery.SearchField.COMMERCIAL_REGISTER_NUMBER, partySearch.getCommercialRegisterNumber(), query);
  }

  private void assertQueryField(Field field, Object value, Query query) {
    if (value == null || (value instanceof String && StringUtils.isEmpty((String) value))) {
      Assert.assertFalse("Found unexpected field \"" + field + "\" in query.", query.getQueryString().contains(field.getName()));
    } else {
      String searchString = StringUtils.lowerCase(value.toString());
      Assert.assertTrue("Expected to find field \"" + field + "\" in query.", query.getQueryString().contains(field.getName()));
      if (searchString.contains(" ")) {
        Assert.assertTrue("Expected to find field \"" + searchString + "\" for field \"" + field + "\"  in query.", query.getQueryString()
            .contains(field.getName() + ":("));
      } else {
        Assert.assertTrue("Expected to find field \"" + searchString + "\" for field \"" + field + "\"  in query.", query.getQueryString()
            .contains(field.getName() + ":" + searchString));
      }
    }
  }

}
