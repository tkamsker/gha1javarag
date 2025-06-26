package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.UnknownAreaCodeDao;
import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;

public class UnknownAreaCodeDaoImpl extends AbstractDao implements UnknownAreaCodeDao {

  @Override
  public void deleteUnknownAreaCode(Long id) {
    executeDelete("UnknownAreaCode.delete", id);
  }

  @Override
  public List<UnknownAreaCode> getAllUnknownAreaCodes() {
    return performListQuery("UnknownAreaCode.get");
  }

  @Override
  public UnknownAreaCode getUnknownAreaCodeById(Long id) {
    return performObjectQuery("UnknownAreaCode.get", id);
  }

  @Override
  public void insertUnknownAreaCode(UnknownAreaCode ct) {
    executeInsert("UnknownAreaCode.insert", ct);
  }

  @Override
  public void updateUnknownAreaCode(UnknownAreaCode ct) {
    executeInsert("UnknownAreaCode.update", ct);
  }

}
