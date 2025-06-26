package at.a1ta.cuco.core.dao.esb;

import org.junit.Assert;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import at.a1ta.cuco.core.service.impl.EsbPartyServiceImpl;
import at.a1ta.cuco.core.shared.dto.EsbParty;
import at.a1ta.cuco.core.shared.dto.StandardAddress;

@Ignore("Integration Test")
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:testApplicationContext-cuco-core.xml"})
public class ITestESBPartyService extends AbstractParametrizedESBDaoTest {

  @Autowired
  private EsbPartyServiceImpl esbPartyService;

  // @Before
  // public void setUp() {
  //
  // EsbPartyDaoImpl esbPartyDao = new EsbPartyDaoImpl();
  // esbPartyDao.setEsbStubFactory(esbStubFactory);
  //
  // esbPartyService = new EsbPartyServiceImpl();
  // esbPartyService.setEsbPartyDao(esbPartyDao);
  // }

  @Test
  public void testGetEsbParty() {
    EsbParty party = esbPartyService.getESBParty(103303208l);
    Assert.assertNotNull(party);
    StandardAddress address = party.getAddress();
    Assert.assertNotNull(address);
    Assert.assertEquals("3142205", address.getLkmsId());
    Assert.assertEquals("Götschka", address.getStreet());
    Assert.assertEquals("37", address.getHouseNumber());
    Assert.assertEquals(null, address.getBlock());
    Assert.assertEquals(null, address.getStaircase());
    Assert.assertEquals(null, address.getFloorNumber());
    Assert.assertEquals(null, address.getDoorNumber());
    Assert.assertEquals(null, address.getAdditional());
    Assert.assertEquals("4212", address.getPostcode());
    Assert.assertEquals("Neumarkt im Mühlkreis", address.getCity());
    Assert.assertEquals("Götschka", address.getVillage());
    Assert.assertEquals("", address.getCountry());

  }

}
