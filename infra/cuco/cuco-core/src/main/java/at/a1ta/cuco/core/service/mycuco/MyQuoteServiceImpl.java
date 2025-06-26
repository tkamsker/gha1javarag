package at.a1ta.cuco.core.service.mycuco;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.shared.dto.SearchResult;
import at.a1ta.cuco.core.dao.db.MyQuoteDao;
import at.a1ta.cuco.core.shared.dto.MyOpportunity;
import at.a1ta.cuco.core.shared.dto.OpportunityFilter;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoOverviewRow;

@Service
public class MyQuoteServiceImpl implements MyQuoteService {

  MyQuoteDao quoteDao;

  @Override
  public SearchResult<MyOpportunity> loadMyOpportunities(OpportunityFilter filter, boolean showNonCustomers) {
    return quoteDao.loadMyOpportunities(filter, showNonCustomers);
  }

  @Override
  public SearchResult<SalesInfoOverviewRow> loadMyQuotesForOverview(OpportunityFilter filter, boolean showNonCustomers) {
    return quoteDao.loadMyQuotesForOverview(filter, showNonCustomers);
  }

  @Autowired
  public void setQuoteDao(MyQuoteDao quoteDao) {
    this.quoteDao = quoteDao;
  }

}
