package at.a1ta.cuco.core.dao.db;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.AttributeConfig;
import at.a1ta.cuco.core.shared.dto.AttributeHistory;

public interface AttributeDao {

  List<AttributeConfig> getAllConfigs();

  void insertConfig(AttributeConfig config);

  void updateConfig(AttributeConfig config);

  void switchOrderNum(AttributeConfig a, AttributeConfig b);

  List<Attribute> getByPartyId(long partyId, String segment);

  List<Attribute> getSameExistingAttributes(Attribute attribute);

  void insert(Attribute attribute);

  void delete(Attribute attribute);

  List<AttributeHistory> getHistory(long partyId, long attributeConfigId);

  void insertHistory(AttributeHistory history);
}
