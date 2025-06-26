package at.a1ta.cuco.core.dao.esb;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.ExpectedException;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.data.clarify.dao.ClarifyInteractionAndWorkflowDao;
import at.a1ta.cuco.core.service.impl.LocationServiceImpl;
import at.a1telekom.eai.lkmslocation.AddressDetail;
import at.a1telekom.eai.lkmslocation.Coordinates;

@RunWith(MockitoJUnitRunner.class)
@Ignore("This are integration Tests and not Unittests")
public class ITestESBLocationService extends AbstractParametrizedESBDaoTest {

  @Mock
  private ClarifyInteractionAndWorkflowDao clarifyInteractionAndWorkflowDaoMock;

  private LocationServiceImpl locationService;
  @Rule
  public ExpectedException expectedEx = ExpectedException.none();

  @Before
  public void setUp() {
    use(ESB_A1TA_INT_PARAMETERS);

    locationService = new LocationServiceImpl();
    locationService.setClarifyInteractionAndWorkflowDao(clarifyInteractionAndWorkflowDaoMock);
  }

  @Test
  public void testGetLkmsLocation() {
    AddressDetail addressDetailForLocation = locationService.getAddressDetailForLocation("10089398");
    Coordinates coordinates = addressDetailForLocation.getCoordinates();
    Assert.assertEquals("48.184490", coordinates.getXWorld());
    Assert.assertEquals("15.257159", coordinates.getYWorld());
  }

  @Test
  public void testGetInvalidLkmsLocation() {
    expectedEx.expect(RuntimeException.class);
    expectedEx.expectMessage("Zu der angegeben Lokations-ID wurde kein LKMS-Objekt (Adresse, Grundstück) gefunden.");
    locationService.getAddressDetailForLocation("INVALID");
  }

  @Test
  public void testLkmsLocationIdIsNull() {
    AddressDetail addressDetailForLocation = locationService.getAddressDetailForLocation(null);
    Assert.assertNull(addressDetailForLocation);
  }

}
