package at.a1ta.cuco.core.dao.db;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.product.PartySummaryItem;

public interface CmDBICTServiceDao {

  List<PartySummaryItem> getICTServicesForPartyId(long partyId);

}
