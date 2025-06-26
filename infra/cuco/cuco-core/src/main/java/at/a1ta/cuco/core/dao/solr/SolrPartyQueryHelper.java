package at.a1ta.cuco.core.dao.solr;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

import org.apache.commons.lang.StringUtils;
import org.springframework.util.Assert;

import at.a1ta.bite.data.solr.core.query.Criteria;
import at.a1ta.bite.data.solr.core.query.Field;
import at.a1ta.bite.data.solr.core.query.Query;
import at.a1ta.cuco.core.shared.dto.PartySearch;

public final class SolrPartyQueryHelper {

  private static final Pattern RESERVED_CHARS_PATTERN = Pattern.compile("\\p{Punct}");
  private static final Pattern FULLTEXT_EXCLUSION_PATTERN = Pattern.compile("\\b10{0,2}\\b|\\b43\\b");
  private static final Criteria ANY = new Criteria(Criteria.WILDCARD).expression(Criteria.WILDCARD);

  private SolrPartyQueryHelper() {}

  public static synchronized Query convertToFindCustomersByIdQuery(List<Long> ids) {
    Assert.notNull(ids, "Cannot construct query for null.");
    Assert.notEmpty(ids, "Cannot load empty list of ids.");

    Query query = new SolrPartyQuery();
    Criteria criteria = new Criteria(SolrPartyQuery.SearchField.CUSTOMER_NUMBER);
    criteria.is(ids.get(0));

    if (ids.size() > 1) {
      for (int i = 1; i < ids.size(); i++) {
        criteria = criteria.or(SolrPartyQuery.SearchField.CUSTOMER_NUMBER).is(ids.get(i));
      }
    }
    query.addCriteria(criteria);
    return query;
  }

  public static synchronized Query convertToQuery(PartySearch searchCriteria) {
    Assert.notNull(searchCriteria, "Parameter searchCriteria must not be null.");
    return createQuery(searchCriteria);
  }

  private static Query createQuery(PartySearch searchCriteria) {
    Query query = new SolrPartyQuery();
    if (searchCriteria.isFulltext()) {
      addFulltextCriteria(searchCriteria, query);
    } else {
      addCriterias(searchCriteria, query);
    }
    return query;
  }

  private static void addFulltextCriteria(PartySearch searchCriteria, Query query) {
    String searchString = filterSpecialCharactersForSearch(searchCriteria.getFulltextTerm());
    searchString = filterSearchValueForFullTextSearch(searchString);

    Criteria fulltextCriteria = new Criteria(SolrPartyQuery.SearchField.FULLTEXT);
    if (StringUtils.isNotBlank(searchString)) {
      fulltextCriteria = splitAndSetCriteriaValue(fulltextCriteria, StringUtils.lowerCase(searchString));
    } else {
      fulltextCriteria = ANY;
    }
    query.addCriteria(fulltextCriteria);
  }

  private static void addCriterias(PartySearch searchCriteria, Query query) {
    List<Criteria> criterias = extractCriteriaList(searchCriteria);
    if (!criterias.isEmpty()) {
      for (Criteria criteria : criterias) {
        if (criteria != null) {
          query.addCriteria(criteria);
        }
      }
    } else {
      query.addCriteria(ANY);
    }
  }

  static List<Criteria> extractCriteriaList(PartySearch searchCriteria) {
    if (StringUtils.isNotBlank(searchCriteria.getAonAccountNumber())) {
      throw new IllegalArgumentException("Searching for 'AON Account Number' is not supported.");
    }

    List<Criteria> criterias = new ArrayList<Criteria>(12);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.FIRSTNAME, searchCriteria.getFirstName(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.LASTNAME, searchCriteria.getLastName(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.STREET, searchCriteria.getStreet(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.POSTCODE, searchCriteria.getPostcode(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.HOUSENUMBER, searchCriteria.getHouseNumber(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.CITY, searchCriteria.getCity(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.CUSTOMER_NUMBER, searchCriteria.getId(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.BAN, searchCriteria.getBillingAccountNumber(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.PHONE_SUBSCRIBER_NUMBER, searchCriteria.getCallNumber(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.PHONE_DESTINATION_CODE, searchCriteria.getOkz(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.PHONE_COUNTRY_CODE, searchCriteria.getLkz(), criterias);
    lowerAndAppendCriteria(SolrPartyQuery.SearchField.COMMERCIAL_REGISTER_NUMBER, searchCriteria.getCommercialRegisterNumber(), criterias);

    return criterias;
  }

  private static void lowerAndAppendCriteria(Field field, Object value, List<Criteria> criterias) {
    if (value != null) {
      if (value instanceof String) {
        String searchString = filterSpecialCharactersForSearch((String) value);
        if (StringUtils.isNotBlank(searchString)) {
          criterias.add(splitAndSetCriteriaValue(new Criteria(field), StringUtils.lowerCase(searchString)));
        }
        return;
      }
      criterias.add(new Criteria(field).is(value));
    }
  }

  static Criteria splitAndSetCriteriaValue(Criteria criteria, String value) {
    if (!StringUtils.contains(value, Criteria.CRITERIA_VALUE_SEPERATOR)) {
      return criteria.startsWith(value);
    }
    String strippedValue = StringUtils.strip(value);
    for (String criteriaFragment : StringUtils.split(strippedValue)) {
      criteria.startsWith(criteriaFragment);
    }
    // the above for statement can be written as expression too, but be aware that
    // value escaping will not work in that case
    // criteria.expression("("+StringUtils.replace(strippedValue, Criteria.CRITERIA_VALUE_SEPERATOR,
    // "*"+Criteria.CRITERIA_VALUE_SEPERATOR)+"*)");
    // @date: 2012-04-11
    return criteria;
  }

  private static String filterSpecialCharactersForSearch(String value) {
    return RESERVED_CHARS_PATTERN.matcher(value).replaceAll(" ");
  }

  private static String filterSearchValueForFullTextSearch(String searchString) {
    return FULLTEXT_EXCLUSION_PATTERN.matcher(searchString).replaceAll(StringUtils.EMPTY);
  }

}
