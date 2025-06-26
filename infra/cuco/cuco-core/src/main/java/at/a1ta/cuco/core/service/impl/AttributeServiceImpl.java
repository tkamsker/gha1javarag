package at.a1ta.cuco.core.service.impl;

import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.dao.db.AttributeDao;
import at.a1ta.cuco.core.service.AttributeService;
import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.AttributeConfig;
import at.a1ta.cuco.core.shared.dto.AttributeHistory;

@Service
public class AttributeServiceImpl implements AttributeService {

  @Autowired
  AttributeDao attributeDao;

  @Override
  public List<AttributeConfig> getAllConfigs() {
    return attributeDao.getAllConfigs();
  }

  @Override
  public AttributeConfig insertConfig(AttributeConfig config, long user) {
    Date date = new Date();
    BiteUser BiteUser = createUser(user);
    config.setCreator(BiteUser);
    config.setCreateDate(date);
    config.setLastModifier(BiteUser);
    config.setLastUpdate(date);
    config.setDeleted(false);
    attributeDao.insertConfig(config);
    return config;
  }

  private BiteUser createUser(long userId) {
    BiteUser user = new BiteUser();
    user.setId(userId);
    return user;
  }

  @Override
  public AttributeConfig updateConfig(AttributeConfig config, long user) {
    config.setLastModifier(createUser(user));
    config.setLastUpdate(new Date());
    attributeDao.updateConfig(config);
    return config;
  }

  @Override
  public AttributeConfig deleteConfig(AttributeConfig config, long user) {
    config.setDeleted(true);
    config.setLastModifier(createUser(user));
    config.setLastUpdate(new Date());
    attributeDao.updateConfig(config);
    return config;
  }

  @Override
  public AttributeConfig activateConfig(AttributeConfig config, long user) {
    config.setActive(true);
    config.setLastModifier(createUser(user));
    config.setLastUpdate(new Date());
    attributeDao.updateConfig(config);
    return config;
  }

  @Override
  public AttributeConfig deactivateConfig(AttributeConfig config, long user) {
    config.setActive(false);
    config.setLastModifier(createUser(user));
    config.setLastUpdate(new Date());
    attributeDao.updateConfig(config);
    return config;
  }

  @Override
  public List<Attribute> getByPartyId(long partyId, String segment) {
    return attributeDao.getByPartyId(partyId, segment);
  }

  @Override
  public Attribute addAttributeAndArchive(Attribute attribute, long user) {
    attribute.setLastModifier(createUser(user));
    attribute.setLastUpdate(new Date());

    archiveExisting(attribute);

    attributeDao.insert(attribute);
    return attribute;
  }

  private void archiveExisting(Attribute attribute) {
    List<Attribute> existingAttributes = attributeDao.getSameExistingAttributes(attribute);
    if (existingAttributes != null && existingAttributes.size() > 0) {
      attribute.setHasHistory(true);
      for (Attribute attr : existingAttributes) {
        AttributeHistory history = createHistory(attr);
        attributeDao.insertHistory(history);
        attributeDao.delete(attr);
      }
    }
  }

  private AttributeHistory createHistory(Attribute attr) {
    AttributeConfig attributeConfig = createConfig(attr);
    AttributeHistory history = new AttributeHistory();
    if (attr != null) {
      history.setAttributeId(attr.getAttributeId());
      history.setAttributeConfig(attributeConfig);
      history.setKundeId(attr.getKundeId());
      history.setBooleanValue(attr.getBooleanValue());
      history.setNumberValue(attr.getNumberValue());
      history.setCreateDate(attr.getLastUpdate());
      history.setCreator(createUser(attr.getLastModifier().getId()));
      history.setTextValue(attr.getTextValue());
    }
    return history;
  }

  private AttributeConfig createConfig(Attribute attr) {
    AttributeConfig attributeConfig = new AttributeConfig();
    if (attr != null && attr.getAttributeConfig() != null) {
      attributeConfig.setAttributeConfigId(attr.getAttributeConfig().getAttributeConfigId());
    }
    return attributeConfig;
  }

  @Override
  public List<AttributeHistory> getHistory(long partyId, long attributeConfigId) {
    List<AttributeHistory> history = attributeDao.getHistory(partyId, attributeConfigId);
    return history;
  }

}
