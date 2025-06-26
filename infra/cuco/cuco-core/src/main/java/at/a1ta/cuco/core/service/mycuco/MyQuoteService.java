package at.a1ta.cuco.core.service.mycuco;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.shared.dto.MyOpportunity;
import at.a1ta.cuco.core.shared.dto.OpportunityFilter;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoOverviewRow;

public interface MyQuoteService {

  SearchResult<MyOpportunity> loadMyOpportunities(OpportunityFilter filter, boolean showNonCustomers);

  SearchResult<SalesInfoOverviewRow> loadMyQuotesForOverview(OpportunityFilter filter, boolean showNonCustomers);
}
