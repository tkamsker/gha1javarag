package at.a1ta.cuco.core.dao.esb;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.cuco.core.shared.dto.AccessToken;
import at.a1ta.cuco.core.shared.dto.PartnerCenterAccessTokenRequest;

@RunWith(MockitoJUnitRunner.class)
@Ignore("This are integration Tests and not Unittests")
public class ITestDefaultPartnerCenterLandingPageDao extends AbstractParametrizedESBDaoTest {

  private PartnerCenterLandingPageDaoImpl dao;

  @Before
  public void setUp() {
    use(ESB_A1TA_INT_PARAMETERS);

    dao = new PartnerCenterLandingPageDaoImpl();
  }

  @Test
  public void test() {
    PartnerCenterAccessTokenRequest request = createPartnerCenterAccessTokenRequest("43 664 88603737", "CuCo", "Next");
    AccessToken result = dao.getAccessToken(request);
    Assert.assertNotNull(result);
    Assert.assertNotNull(result.getToken());
    Assert.assertEquals(request.getTargetSystem(), result.getTargetSystem());
  }

  private PartnerCenterAccessTokenRequest createPartnerCenterAccessTokenRequest(String phone, String sourceSystem, String processId) {
    PartnerCenterAccessTokenRequest request = new PartnerCenterAccessTokenRequest();

    request.setTargetSystem("Black");
    request.setSourceSystem(sourceSystem);

    String[] msisdnParts = phone.split(" ");
    request.setCountryCode(msisdnParts[0]);
    request.setNationalDestinationCode(msisdnParts[1]);
    request.setSubscriberNumber(msisdnParts[0]);
    request.setProcessId(processId);

    return request;
  }

}
