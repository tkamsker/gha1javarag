package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.CreditTypeDao;
import at.a1ta.cuco.core.shared.dto.CreditType;

public class CreditTypeDaoImpl extends AbstractDao implements CreditTypeDao {

  @Override
  public void deleteCreditType(Long id) {
    executeDelete("CreditType.delete", id);
  }

  @Override
  public List<CreditType> getAllCreditTypes() {
    return performListQuery("CreditType.get");
  }

  @Override
  public CreditType getCreditTypeById(Long id) {
    return performObjectQuery("CreditType.get", id);
  }

  @Override
  public void insertCreditType(CreditType ct) {
    executeInsert("CreditType.insert", ct);
  }

  @Override
  public void updateCreditType(CreditType ct) {
    executeInsert("CreditType.update", ct);
  }

}
