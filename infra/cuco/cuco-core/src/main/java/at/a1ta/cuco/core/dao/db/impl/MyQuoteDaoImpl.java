package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.dao.db.MyQuoteDao;
import at.a1ta.cuco.core.shared.dto.MyOpportunity;
import at.a1ta.cuco.core.shared.dto.OpportunityFilter;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoOverviewRow;

public class MyQuoteDaoImpl extends AbstractDao implements MyQuoteDao {

  @Autowired
  private SettingService settingService;

  private static final String SEARCH_RESULT_LIMIT_SETTING_KEY = "mycuco.table.searchresult.limit";

  @SuppressWarnings("unchecked")
  @Override
  public SearchResult<MyOpportunity> loadMyOpportunities(OpportunityFilter filter, boolean showNonCustomers) {
    Map<String, Object> params = createParams(filter);
    SearchResult<MyOpportunity> result = (SearchResult<MyOpportunity>) performLimitedListQuery("MyQuote.LoadMyOpportunities", params, settingService.getIntValue(SEARCH_RESULT_LIMIT_SETTING_KEY));
    if (showNonCustomers) {
      SearchResult<MyOpportunity> resultsForNonCustomer = (SearchResult<MyOpportunity>) performLimitedListQuery("MyQuote.LoadMyOpportunitiesForNonCustomers", params,
          settingService.getIntValue(SEARCH_RESULT_LIMIT_SETTING_KEY));
      result.getResults().addAll(resultsForNonCustomer.getResults());
    }
    return result;
  }

  @SuppressWarnings("unchecked")
  @Override
  public SearchResult<SalesInfoOverviewRow> loadMyQuotesForOverview(OpportunityFilter filter, boolean showNonCustomers) {
    Map<String, Object> params = createParams(filter);
    SearchResult<SalesInfoOverviewRow> result = (SearchResult<SalesInfoOverviewRow>) performLimitedListQuery("MyQuote.loadMyQuotesForOverview", params,
        settingService.getIntValue(SEARCH_RESULT_LIMIT_SETTING_KEY));
    if (showNonCustomers) {
      SearchResult<SalesInfoOverviewRow> resultForLeads = (SearchResult<SalesInfoOverviewRow>) performLimitedListQuery("MyQuote.loadMyQuotesForOverviewForLeads", params,
          settingService.getIntValue(SEARCH_RESULT_LIMIT_SETTING_KEY));
      result.getResults().addAll(resultForLeads.getResults());
    }
    return result;
  }

  private Map<String, Object> createParams(OpportunityFilter filter) {
    Map<String, Object> params = new HashMap<String, Object>();
    params.put("userId", filter.getUserId());
    params.put("clearanceUserId", filter.getClearanceUserId());
    params.put("betreuer", filter.getBetreuer() != null ? filter.getBetreuer().toLowerCase() : null);
    params.put("partyId", filter.getPartyId());
    params.put("quoteNumber", filter.getQuoteNumber());
    params.put("firstName", filter.getFirstName());
    params.put("lastName", filter.getLastName());
    params.put("productOfferingName", filter.getProductOfferingName() != null ? filter.getProductOfferingName().getId() : null);
    params.put("status", filter.getStatus());
    params.put("createDate", filter.getCreateDate());
    params.put("validToDate", filter.getValidToDate());
    params.put("creatorName", filter.getCreator());
    params.put("lastModifierName", filter.getLastModifier());
    params.put("title", filter.getTitle());
    params.put("assignee", filter.getAssignee());
    return params;
  }

}
