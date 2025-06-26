package at.a1ta.cuco.core.service;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.AttributeConfig;
import at.a1ta.cuco.core.shared.dto.AttributeHistory;

public interface AttributeService {

  List<AttributeConfig> getAllConfigs();

  AttributeConfig insertConfig(AttributeConfig config, long user);

  AttributeConfig updateConfig(AttributeConfig config, long user);

  AttributeConfig deleteConfig(AttributeConfig config, long user);

  AttributeConfig activateConfig(AttributeConfig config, long user);

  AttributeConfig deactivateConfig(AttributeConfig config, long user);

  List<Attribute> getByPartyId(long partyId, String segment);

  Attribute addAttributeAndArchive(Attribute attribute, long user);

  List<AttributeHistory> getHistory(long partyId, long attributeConfigId);

}
