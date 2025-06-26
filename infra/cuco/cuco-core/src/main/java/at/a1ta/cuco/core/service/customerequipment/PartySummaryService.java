package at.a1ta.cuco.core.service.customerequipment;

import java.util.ArrayList;

import at.a1ta.cuco.core.shared.dto.product.GetPartySummaryResponse;
import at.a1ta.cuco.core.shared.dto.product.PartySummaryItem;

public interface PartySummaryService {

  GetPartySummaryResponse getPartySummary(Long partyId);

  ArrayList<PartySummaryItem> getICTServicesForPartyId(Long partyId);

}
