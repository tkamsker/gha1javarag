package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.CmDBICTServiceDao;
import at.a1ta.cuco.core.shared.dto.product.PartySummaryItem;

public class CmDBICTServiceDaoImpl extends AbstractDao implements CmDBICTServiceDao {

  @Override
  public List<PartySummaryItem> getICTServicesForPartyId(long partyId) {
    return performListQuery("CmDBICTService.getICTServicesForPartyId", partyId + "");
  }

}
