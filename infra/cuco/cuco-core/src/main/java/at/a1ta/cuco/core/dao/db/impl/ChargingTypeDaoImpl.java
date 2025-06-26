package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.ChargingTypeDao;
import at.a1ta.cuco.core.shared.dto.ChargingType;

public class ChargingTypeDaoImpl extends AbstractDao implements ChargingTypeDao {
  @Override
  public List<ChargingType> getAllChargingTypes() {
    return performListQuery("ChargingType.get");
  }
}
