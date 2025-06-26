package at.a1ta.cuco.core.dao.esb;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map.Entry;

import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.Mockito;

import at.a1ta.bite.core.server.service.TextService;
import at.a1ta.bite.core.shared.dto.Text;
import at.a1ta.cuco.core.service.customerequipment.ProductBrowserServiceImpl;
import at.a1ta.cuco.core.shared.dto.product.CallNumber;
import at.a1ta.cuco.core.shared.dto.product.DefaultSubscriptionNode;
import at.a1ta.cuco.core.shared.dto.product.SubscriptionTree;
import at.a1telekom.eai.customerinventory.Subscription;

@Ignore("This are integration Tests and not Unittests")
public class ITestProductBrowser extends AbstractParametrizedESBDaoTest {
  private ProductBrowserServiceImpl productBrowserServiceImpl = new ProductBrowserServiceImpl();

  @Mock
  private TextService textService;

  @Before
  public void setUp() {
    use(ESB_A1TA_PROD_PARAMETERS);
    // productBrowserServiceImpl.setPartyService(partyService);
    // productBrowserServiceImpl.setCustomerEquipmentService(customerEquipmentService);
    productBrowserServiceImpl.setTextService(textService);

    Text text = new Text();
    text.setText("asdf");
    Mockito.when(textService.getByKeyWithDefaultText(Matchers.anyString(), Matchers.anyString())).thenReturn(text);
  }

  @Test
  public void testGetLocationSubscriptionsMap() {
    long partyId = 100126287;
    String sessionId = "123456";
    HashMap<String, ArrayList<Subscription>> map = productBrowserServiceImpl.getLocationSubscriptionsMap(partyId);
    System.out.println("getLocationSubscriptionsMap: " + map);

    for (Entry<String, ArrayList<Subscription>> entry : map.entrySet()) {
      String key = entry.getKey();
      ArrayList<Subscription> subscriptions = entry.getValue();

      for (Subscription subscription : subscriptions) {
        DefaultSubscriptionNode subscriptionNode = new DefaultSubscriptionNode();
        subscriptionNode.setId(subscription.getId());
        if (subscription.getCallNumber() != null) {
          subscriptionNode.setCallNumber(new CallNumber(subscription.getCallNumber().getCC(), subscription.getCallNumber().getNDC(), subscription.getCallNumber().getSN()));

          SubscriptionTree tree = productBrowserServiceImpl.getDefaultProductNodes(subscriptionNode, sessionId, false);
          System.out.println("getDefaultProductNodes: " + tree);
        }
      }
    }
  }
}
