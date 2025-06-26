package at.a1ta.cuco.core.dao.esb;

import org.junit.runner.RunWith;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.server.dao.EsbAccessParameterDao;
import at.a1ta.bite.core.server.dto.EsbAccessParameter;
import at.a1ta.bite.core.server.esb.EsbStubFactory;
import at.a1ta.bite.core.server.esb.StubCache;

@RunWith(MockitoJUnitRunner.class)
public abstract class AbstractParametrizedESBDaoTest {

  public static final EsbAccessParameter ESB_A1TA_DEV_PARAMETERS = new EsbAccessParameter("DEV_A1TA", "ems1e.a1telekom.inside:17322", "ems1e.a1telekom.inside:17322", "ta-cuco", "ta", 60000l, "a1ta-dev", "http://esb-e-ar1:8080/si:a1ta-dev");

  public static final EsbAccessParameter ESB_MK_DEV_PARAMETERS = new EsbAccessParameter("DEV_MK", "ems1e.a1telekom.inside:17322", "ems1e.a1telekom.inside:17322", "ta-cuco", "ta", 60000l, "mk", "http://esb-e-ar1:8080/si:mk");

  public static final EsbAccessParameter ESB_A1TA_INT_PARAMETERS = new EsbAccessParameter("INT_A1TA", "ems1i.telekom.inside:17322", "ems2i.telekom.inside:17322", "ta-cuco", "cuco2010", 60000l, "a1ta-int", "http://esb-i.telekom.inside:8080/esb/si:a1ta-int");

  public static final EsbAccessParameter ESB_A1TA_PROD_PARAMETERS = new EsbAccessParameter("PROD_A1TA", "ems1p.telekom.inside:17322", "ems2p.telekom.inside:17322", "ta-cuco", "cuco2412", 60000l, "a1ta-prod", "http://esb-p.telekom.inside:8080/esb/si:a1ta-prod");

  public static final EsbAccessParameter ESB_TA_PROD_PARAMETERS = new EsbAccessParameter("PROD", "ems1p.telekom.inside:17322", "ems2p.telekom.inside:17322", "ta-cuco", "cuco2412", 60000l, "ta-prod", "http://esb-p.telekom.inside:8080/esb/si:ta-prod");

  protected EsbStubFactory esbStubFactory;

  @Mock
  protected EsbAccessParameterDao parameterDaoMock;

  @SuppressWarnings({"unchecked", "rawtypes"})
  public void before() {
    esbStubFactory = new EsbStubFactory();
    esbStubFactory.setEsbAccessParameterDao(parameterDaoMock);
    esbStubFactory.setStubCache(new StubCache());
  }

  protected void use(EsbAccessParameter esbparam) {
    Mockito.when(parameterDaoMock.get(Matchers.anyString())).thenReturn(esbparam);
    before();
  }

}
