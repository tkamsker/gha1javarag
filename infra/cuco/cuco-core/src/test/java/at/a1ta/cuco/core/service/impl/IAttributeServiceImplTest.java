package at.a1ta.cuco.core.service.impl;

import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import at.a1ta.cuco.core.service.AttributeService;
import at.a1ta.cuco.core.shared.dto.AttributeConfig;
import at.a1ta.cuco.core.shared.dto.AttributeConfig.ConfigTypes;

@Ignore
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:testApplicationContext-cuco-core.xml"})
public class IAttributeServiceImplTest {

  @Autowired
  AttributeService attributeService;

  @Test
  public void testInsertConfig() {

    AttributeConfig config = new AttributeConfig();
    config.setAttributeName("Anzahl der Freiminuten (TEST)");
    config.setAttributeType(ConfigTypes.NUMBER);
    config.setOrderNum(4);
    config.setLowerBounds(0);
    config.setUpperBounds(1000);
    config.setActive(true);

    AttributeConfig insertConfig = attributeService.insertConfig(config, 36668);

    Assert.assertNotNull(insertConfig);
    Assert.assertNotNull(insertConfig.getAttributeConfigId());
    Assert.assertNotNull(insertConfig.getCreator());
    Assert.assertNotNull(insertConfig.getCreateDate());
    Assert.assertNotNull(insertConfig.getLastModifier());
    Assert.assertNotNull(insertConfig.getLastUpdate());
    Assert.assertNotNull(insertConfig.getOrderNum());

    Assert.assertEquals(true, insertConfig.getActive());
    Assert.assertEquals(false, insertConfig.getDeleted());

    insertConfig = attributeService.deactivateConfig(insertConfig, 36668);

    Assert.assertEquals(false, insertConfig.getActive());

    insertConfig = attributeService.activateConfig(insertConfig, 36668);

    Assert.assertEquals(true, insertConfig.getActive());
  }
}
