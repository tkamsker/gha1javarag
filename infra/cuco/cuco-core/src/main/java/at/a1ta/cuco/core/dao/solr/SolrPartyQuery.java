package at.a1ta.cuco.core.dao.solr;

import at.a1ta.bite.data.solr.core.query.BasicQuery;
import at.a1ta.bite.data.solr.core.query.Field;

public class SolrPartyQuery extends BasicQuery {

  public enum SearchField implements Field {
    //@formatter:off
    TITLE("title_ci"),
    FIRSTNAME("firstname_ci"),
    LASTNAME("lastname_ci"),
    STREET("street_ci"),
    POSTCODE("postcode"),
    HOUSENUMBER("housenumber_ci"),
    CITY("city_ci"),
    VILLAGE("village_ci"),
    CUSTOMER_NUMBER("customernumber"),
    BAN("billingaccountnumber"),
    EMAIL("email_ci"),
    PHONE_SUBSCRIBER_NUMBER("subscribernumber"),
    PHONE_DESTINATION_CODE("destinationcode"),
    PHONE_COUNTRY_CODE("countrycode"),
    COMMERCIAL_REGISTER_NUMBER("commercialregister"),
    CENTRAL_ASSOCIATION_NUMBER("centralassociation"),
    FULLTEXT("fulltext");
		//@formatter:on

    private String fieldName;

    SearchField(String name) {
      this.fieldName = name;
    }

    @Override
    public String getName() {
      return this.fieldName;
    }
  }

}
