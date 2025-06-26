package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.AttributeDao;
import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.AttributeConfig;
import at.a1ta.cuco.core.shared.dto.AttributeHistory;

public class AttributeDaoImpl extends AbstractDao implements AttributeDao {

  @Override
  public List<AttributeConfig> getAllConfigs() {
    return performListQuery("Attribute.getAllConfigs");
  }

  @Override
  public void insertConfig(AttributeConfig config) {
    executeInsert("Attribute.insertConfig", config);
  }

  @Override
  public void updateConfig(AttributeConfig config) {
    executeUpdate("Attribute.updateConfig", config);
  }

  @Override
  public List<Attribute> getByPartyId(long partyId, String segment) {
    HashMap<String, Object> params = new HashMap<String, Object>();
    params.put("kundeId", partyId);
    params.put("segment", segment);
    return performListQuery("Attribute.getByPartyId", params);
  }

  @Override
  public List<Attribute> getSameExistingAttributes(Attribute attribute) {
    return performListQuery("Attribute.getSameExistingAttributes", attribute);
  }

  @Override
  public void insert(Attribute attribute) {
    executeInsert("Attribute.insert", attribute);
  }

  @Override
  public void delete(Attribute attribute) {
    executeDelete("Attribute.delete", attribute);
  }

  @Override
  public List<AttributeHistory> getHistory(long partyId, long attributeConfigId) {
    HashMap<String, Long> params = new HashMap<String, Long>();
    params.put("partyId", partyId);
    params.put("attributeConfigId", attributeConfigId);
    List<AttributeHistory> result = performListQuery("Attribute.getHistory", params);
    return result;
  }

  @Override
  public void insertHistory(AttributeHistory history) {
    executeInsert("Attribute.insertHistory", history);
  }

  @Override
  public void switchOrderNum(AttributeConfig a, AttributeConfig b) {
    int ordernumA = a.getOrderNum();
    a.setOrderNum(b.getOrderNum());
    b.setOrderNum(ordernumA);

    executeUpdate("Attribute.updateConfig", a);
    executeUpdate("Attribute.updateConfig", b);
  }

}
