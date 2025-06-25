# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/dao/solr/SolrPartyQuery.java

SolrPartyQuery.java
1. Purpose: Defines search query fields for party/customer data in Solr search engine
2. User Interactions: None directly - used by search services
3. Data Handling:
   - Defines searchable fields like title, firstname, lastname, address details
   - Extends BasicQuery for Solr functionality
4. Business Rules:
   - Standardizes field naming conventions with _ci suffix (likely case-insensitive)
   - Maps business fields to Solr index fields
5. Dependencies:
   - Depends on bite.data.solr.core.query components
   - Used by search services needing party/customer lookups