package at.a1ta.cuco.core.service.impl;

import static org.mockito.Matchers.anyLong;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.when;

import java.net.MalformedURLException;
import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

import org.hamcrest.core.IsInstanceOf;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.service.CustomerEquipmentService;
import at.a1ta.cuco.core.service.PartyService;
import at.a1ta.cuco.core.service.customerequipment.ProductBrowserServiceImpl;
import at.a1ta.cuco.core.shared.dto.IndexationStatus;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentConsignee;
import at.a1ta.cuco.core.shared.dto.product.AccountNode;
import at.a1ta.cuco.core.shared.dto.product.BaseNode;
import at.a1ta.cuco.core.shared.dto.product.Location;
import at.a1ta.cuco.core.shared.dto.product.LocationNode;
import at.a1ta.cuco.core.shared.dto.product.ProductTree;
import at.a1ta.cuco.core.shared.dto.product.SubscriptionNode;
import at.a1telekom.eai.customerinventory.Address;
import at.a1telekom.eai.customerinventory.FormattedAddress;
import at.a1telekom.eai.customerinventory.Subscription;

@RunWith(MockitoJUnitRunner.class)
public class ProductBrowserServiceImplTest {

  public enum Kind {
    SINGLE(1), SAME_ADDR(2), SAME_LOC(3), SIMILAR_ADDR(4), DIFFERENT(5);

    long partyId;

    private Kind(long partyId) {
      this.partyId = partyId;

    }
  }

  @Spy
  ProductBrowserServiceImpl productBrowserServiceImpl;

  @Mock
  PartyService partyServiceImpl;

  @Mock
  SettingService settingService;
  @Mock
  CustomerEquipmentService customerEquipmentService;

  @Before
  public void setup() throws MalformedURLException, RemoteException {
    Party party = new Party();
    doReturn(party).when(partyServiceImpl).get(anyLong());

    productBrowserServiceImpl.setPartyService(partyServiceImpl);

    ArrayList<EquipmentConsignee> consignees = new ArrayList<EquipmentConsignee>();
    doReturn(consignees).when(customerEquipmentService).getEquipmentConsignees(anyLong());
    productBrowserServiceImpl.setCustomerEquipmentService(customerEquipmentService);
    when(settingService.getValue("productBrowser.showMAMInfo")).thenReturn("true");
    productBrowserServiceImpl.setSettingService(settingService);
    doReturn(createMockSubscriptions(Kind.SINGLE)).when(productBrowserServiceImpl).getLocationSubscriptionsMap(Kind.SINGLE.partyId);
    doReturn(createMockSubscriptions(Kind.SAME_ADDR)).when(productBrowserServiceImpl).getLocationSubscriptionsMap(Kind.SAME_ADDR.partyId);
    doReturn(createMockSubscriptions(Kind.SAME_LOC)).when(productBrowserServiceImpl).getLocationSubscriptionsMap(Kind.SAME_LOC.partyId);
    doReturn(createMockSubscriptions(Kind.SIMILAR_ADDR)).when(productBrowserServiceImpl).getLocationSubscriptionsMap(Kind.SIMILAR_ADDR.partyId);
    doReturn(createMockSubscriptions(Kind.DIFFERENT)).when(productBrowserServiceImpl).getLocationSubscriptionsMap(Kind.DIFFERENT.partyId);

  }

  @Test
  public void singleAddresseTest() {
    test(Kind.SINGLE.partyId, 1);
  }

  @Test
  public void differentAddressesTest() {
    test(Kind.DIFFERENT.partyId, 2);
  }

  @Test
  public void sameAddressTest() {
    test(Kind.SAME_ADDR.partyId, 1);
  }

  @Test
  public void sameLocTest() {
    test(Kind.SAME_LOC.partyId, 1);
  }

  @Test
  public void similarAddressTest() {
    test(Kind.SIMILAR_ADDR.partyId, 1);
  }

  @Test
  public void testMapSubscritionTreeToParent() {
    LocationNode parent = new LocationNode();
    Subscription subscription = Subscription.Factory.newInstance();
    subscription.addNewCustomerAccount().setAccountNumber("1234");
    subscription.setPartyId("1");
    productBrowserServiceImpl.mapSubscritionTreeToParent(Arrays.asList(subscription), parent);

    ArrayList<BaseNode> nodes = parent.getChildren();
    Assert.assertThat(nodes.get(0), IsInstanceOf.instanceOf(AccountNode.class));

    AccountNode banNode = (AccountNode) nodes.iterator().next();

    Assert.assertEquals("1234", banNode.getAccountNumber());
    Assert.assertEquals(parent, banNode.getParent());
    Assert.assertEquals(1, banNode.getChildren().size());
    Assert.assertEquals(banNode, banNode.getChildren().get(0).getParent());
  }

  @Test
  public void testMapSubscritionTreeToParent_IndexedAccount() {
    LocationNode parent = new LocationNode();
    Subscription subscription = Subscription.Factory.newInstance();
    subscription.setPartyId("1");
    subscription.addNewCustomerAccount().setAccountNumber("1234");
    subscription.getCustomerAccount().setIdxExemption(false);
    productBrowserServiceImpl.mapSubscritionTreeToParent(Arrays.asList(subscription), parent);

    ArrayList<BaseNode> nodes = parent.getChildren();
    Assert.assertThat(nodes.get(0), IsInstanceOf.instanceOf(AccountNode.class));

    AccountNode banNode = (AccountNode) nodes.iterator().next();

    Assert.assertEquals(IndexationStatus.INDEXED, banNode.getIdxStatus());
  }

  @Test
  public void testMapSubscritionTreeToParent_NotIndexedAccount() {
    LocationNode parent = new LocationNode();
    Subscription subscription = Subscription.Factory.newInstance();
    subscription.setPartyId("1");
    subscription.addNewCustomerAccount().setAccountNumber("1234");
    subscription.getCustomerAccount().setIdxExemption(true);
    productBrowserServiceImpl.mapSubscritionTreeToParent(Arrays.asList(subscription), parent);

    ArrayList<BaseNode> nodes = parent.getChildren();
    Assert.assertThat(nodes.get(0), IsInstanceOf.instanceOf(AccountNode.class));

    AccountNode banNode = (AccountNode) nodes.iterator().next();

    Assert.assertEquals(IndexationStatus.NOT_INDEXED, banNode.getIdxStatus());
  }

  @Test
  public void testMapSubscritionTreeToParent_NotAvailable() {
    LocationNode parent = new LocationNode();
    Subscription subscription = Subscription.Factory.newInstance();
    subscription.setPartyId("1");
    subscription.addNewCustomerAccount().setAccountNumber("1234");
    productBrowserServiceImpl.mapSubscritionTreeToParent(Arrays.asList(subscription), parent);

    ArrayList<BaseNode> nodes = parent.getChildren();
    Assert.assertThat(nodes.get(0), IsInstanceOf.instanceOf(AccountNode.class));

    AccountNode banNode = (AccountNode) nodes.iterator().next();

    Assert.assertEquals(IndexationStatus.NOT_AVAILABLE, banNode.getIdxStatus());
  }

  @Test
  public void testMapSubscritionTreeToParentNoBanPresent() {
    LocationNode parent = new LocationNode();
    Subscription subscription = Subscription.Factory.newInstance();
    subscription.setPartyId("1");
    productBrowserServiceImpl.mapSubscritionTreeToParent(Arrays.asList(subscription), parent);
    Assert.assertThat(parent.getChildren().get(0), IsInstanceOf.instanceOf(SubscriptionNode.class));
  }

  private void test(long partyId, int expectedNumberOfLocations) {
    ArrayList<Long> partyIds = new ArrayList<Long>();
    partyIds.add(partyId);

    ProductTree tree = productBrowserServiceImpl.getSubscriptionTree(partyIds, "", false);
    HashMap<Long, ArrayList<Location>> locationMap = tree.getLocationMap();
    ArrayList<Location> list = locationMap.get(partyId);
    Assert.assertEquals(expectedNumberOfLocations, list.size());
  }

  private HashMap<String, ArrayList<Subscription>> createMockSubscriptions(Kind kind) {
    HashMap<String, ArrayList<Subscription>> mockSubscriptions = null;

    switch (kind) {
      case SINGLE:
        return createSingleSubscription();
      case DIFFERENT:
        return createDifferentSubscriptions();
      case SAME_ADDR:
        return createSameAddressSubscriptions();
      case SAME_LOC:
        return createSameLocSubscriptions();
      case SIMILAR_ADDR:
        return createSimilarAddressSubscriptions();
      default:
        break;
    }

    return mockSubscriptions;
  }

  private HashMap<String, ArrayList<Subscription>> createSingleSubscription() {
    FormattedAddress formattedAddress = FormattedAddress.Factory.newInstance();
    formattedAddress.setAddressLine1("Seebach 11");
    formattedAddress.setAddressLine2("4560 Kirchdorf");
    formattedAddress.setAddressLine3("");

    Subscription subscription = Subscription.Factory.newInstance();
    subscription.setPartyId("1");
    Address address = Address.Factory.newInstance();
    address.setFormattedAddress(formattedAddress);
    subscription.setAddress(address);

    ArrayList<Subscription> subscriptions = new ArrayList<Subscription>();
    subscriptions.add(subscription);

    HashMap<String, ArrayList<Subscription>> mockSubscriptions = new HashMap<String, ArrayList<Subscription>>();
    mockSubscriptions.put("123", subscriptions);

    return mockSubscriptions;
  }

  private HashMap<String, ArrayList<Subscription>> createDifferentSubscriptions() {
    FormattedAddress formattedAddress = FormattedAddress.Factory.newInstance();
    formattedAddress.setAddressLine1("Seebach 11");
    formattedAddress.setAddressLine2("4560 Kirchdorf");
    formattedAddress.setAddressLine3("");

    Subscription subscription = Subscription.Factory.newInstance();
    subscription.setPartyId("1");
    Address address = Address.Factory.newInstance();
    address.setFormattedAddress(formattedAddress);
    subscription.setAddress(address);
    FormattedAddress formattedAddress1 = FormattedAddress.Factory.newInstance();
    formattedAddress1.setAddressLine1("Steinfeld 58");
    formattedAddress1.setAddressLine2("4563 Micheldorf");
    formattedAddress1.setAddressLine3("");

    Subscription subscription1 = Subscription.Factory.newInstance();
    Address address1 = Address.Factory.newInstance();
    address1.setFormattedAddress(formattedAddress1);
    subscription1.setAddress(address1);
    subscription1.setPartyId("1");
    ArrayList<Subscription> subscriptions = new ArrayList<Subscription>();
    subscriptions.add(subscription);
    ArrayList<Subscription> subscriptions1 = new ArrayList<Subscription>();
    subscriptions1.add(subscription1);

    HashMap<String, ArrayList<Subscription>> mockSubscriptions = new HashMap<String, ArrayList<Subscription>>();
    mockSubscriptions.put("123", subscriptions);
    mockSubscriptions.put("234", subscriptions1);

    return mockSubscriptions;
  }

  private HashMap<String, ArrayList<Subscription>> createSameAddressSubscriptions() {
    FormattedAddress formattedAddress = FormattedAddress.Factory.newInstance();
    formattedAddress.setAddressLine1("Seebach 11");
    formattedAddress.setAddressLine2("4560 Kirchdorf");
    formattedAddress.setAddressLine3("");

    Subscription subscription = Subscription.Factory.newInstance();
    subscription.setPartyId("1");
    Address address = Address.Factory.newInstance();
    address.setFormattedAddress(formattedAddress);
    subscription.setAddress(address);
    FormattedAddress formattedAddress1 = FormattedAddress.Factory.newInstance();
    formattedAddress1.setAddressLine1("Seebach 11");
    formattedAddress1.setAddressLine2("4560 Kirchdorf");
    formattedAddress1.setAddressLine3("");

    Subscription subscription1 = Subscription.Factory.newInstance();
    subscription1.setPartyId("1");
    Address address1 = Address.Factory.newInstance();
    address1.setFormattedAddress(formattedAddress1);
    subscription1.setAddress(address1);
    ArrayList<Subscription> subscriptions = new ArrayList<Subscription>();
    subscriptions.add(subscription);
    ArrayList<Subscription> subscriptions1 = new ArrayList<Subscription>();
    subscriptions1.add(subscription1);

    HashMap<String, ArrayList<Subscription>> mockSubscriptions = new HashMap<String, ArrayList<Subscription>>();
    mockSubscriptions.put("123", subscriptions);
    mockSubscriptions.put("234", subscriptions1);

    return mockSubscriptions;
  }

  private HashMap<String, ArrayList<Subscription>> createSameLocSubscriptions() {
    FormattedAddress formattedAddress = FormattedAddress.Factory.newInstance();
    formattedAddress.setAddressLine1("Seebach 11");
    formattedAddress.setAddressLine2("4560 Kirchdorf");
    formattedAddress.setAddressLine3("");

    Subscription subscription = Subscription.Factory.newInstance();
    subscription.setPartyId("1");
    Address address = Address.Factory.newInstance();
    address.setFormattedAddress(formattedAddress);
    subscription.setAddress(address);
    FormattedAddress formattedAddress1 = FormattedAddress.Factory.newInstance();
    formattedAddress1.setAddressLine1("Seebach 11");
    formattedAddress1.setAddressLine2("4560 Kirchdorf");
    formattedAddress1.setAddressLine3("");

    Subscription subscription1 = Subscription.Factory.newInstance();
    subscription1.setPartyId("1");
    Address address1 = Address.Factory.newInstance();
    address1.setFormattedAddress(formattedAddress1);
    subscription1.setAddress(address1);
    ArrayList<Subscription> subscriptions = new ArrayList<Subscription>();
    subscriptions.add(subscription);
    subscriptions.add(subscription1);

    HashMap<String, ArrayList<Subscription>> mockSubscriptions = new HashMap<String, ArrayList<Subscription>>();
    mockSubscriptions.put("123", subscriptions);

    return mockSubscriptions;
  }

  private HashMap<String, ArrayList<Subscription>> createSimilarAddressSubscriptions() {
    FormattedAddress formattedAddress = FormattedAddress.Factory.newInstance();
    formattedAddress.setAddressLine1("Seebach 11");
    formattedAddress.setAddressLine2("4560 Kirchdorf");
    formattedAddress.setAddressLine3("");

    Subscription subscription = Subscription.Factory.newInstance();
    Address address = Address.Factory.newInstance();
    address.setFormattedAddress(formattedAddress);
    subscription.setAddress(address);
    subscription.setPartyId("1");
    FormattedAddress formattedAddress1 = FormattedAddress.Factory.newInstance();
    formattedAddress1.setAddressLine1("Seebach 11");
    formattedAddress1.setAddressLine2("4560");
    formattedAddress1.setAddressLine3("Kirchdorf");

    Subscription subscription1 = Subscription.Factory.newInstance();
    Address address1 = Address.Factory.newInstance();
    subscription1.setPartyId("1");
    address1.setFormattedAddress(formattedAddress1);
    subscription1.setAddress(address1);
    ArrayList<Subscription> subscriptions = new ArrayList<Subscription>();
    subscriptions.add(subscription);
    ArrayList<Subscription> subscriptions1 = new ArrayList<Subscription>();
    subscriptions1.add(subscription1);

    HashMap<String, ArrayList<Subscription>> mockSubscriptions = new HashMap<String, ArrayList<Subscription>>();
    mockSubscriptions.put("123", subscriptions);
    mockSubscriptions.put("234", subscriptions1);

    return mockSubscriptions;
  }
}
