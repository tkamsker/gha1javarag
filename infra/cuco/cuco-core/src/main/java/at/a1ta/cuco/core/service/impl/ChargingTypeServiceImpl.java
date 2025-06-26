package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.ChargingTypeDao;
import at.a1ta.cuco.core.service.ChargingTypeService;
import at.a1ta.cuco.core.shared.dto.ChargingType;

@Service
public class ChargingTypeServiceImpl implements ChargingTypeService {

  private ChargingTypeDao chargingTypeDao;

  @Override
  public List<ChargingType> getAllChargingTypes() {
    return chargingTypeDao.getAllChargingTypes();
  }

  @Autowired
  public void setChargingTypeDao(ChargingTypeDao chargingTypeDao) {
    this.chargingTypeDao = chargingTypeDao;
  }
}
