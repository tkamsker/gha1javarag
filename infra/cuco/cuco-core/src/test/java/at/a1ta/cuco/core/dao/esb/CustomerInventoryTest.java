package at.a1ta.cuco.core.dao.esb;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Matchers.any;
import static org.mockito.Mockito.when;

import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.apache.xmlbeans.XmlException;
import org.junit.Before;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.runners.MockitoJUnitRunner;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;

import at.a1ta.cuco.core.service.customerequipment.ProductBrowserServiceImpl;
import at.a1telekom.eai.customerinventory.GetProductsForSubscriptionRequestDocument;
import at.a1telekom.eai.customerinventory.GetProductsForSubscriptionResponseDocument;
import at.a1telekom.eai.customerinventory.GetProductsResponseType;
import at.a1telekom.eai.customerinventory.GetSubscriptionsForPartyRequestDocument;
import at.a1telekom.eai.customerinventory.GetSubscriptionsForPartyResponseDocument;
import at.a1telekom.eai.customerinventory.GetSubscriptionsForPartyResponseType;
import at.a1telekom.eai.customerinventory.Product;
import at.a1telekom.eai.customerinventory.ProductBundle;
import at.a1telekom.eai.customerinventory.Subscription;
import at.a1telekom.eai.customerinventory.impl.GetProductsForSubscriptionRequestDocumentImpl;
import at.a1telekom.eai.customerinventory.impl.GetSubscriptionsForPartyRequestDocumentImpl;
import at.mobilkom.eai.esb.EsbParam;

import com.telekomaustriagroup.esb.customerinventory.CustomerInventoryStub;
import com.telekomaustriagroup.esb.customerinventory.Error;

@RunWith(MockitoJUnitRunner.class)
public class CustomerInventoryTest {

  private static final String FILE_RESOURCE_RESPONSE_SUBSCRIPTIONS_FOR_PARTY = "GetSubscriptionsForPartyResponse.xml";
  private static final String FILE_RESOURCE_RESPONSE_PRODUCTS_FOR_SUBSCRIPTION = "GetProductsForSubscriptionResponse.xml";
  private static final String FILE_RESOURCE_RESPONSE_PRODUCTS_FOR_SUBSCRIPTION_PRODUCT_CATALOG_DETAILS = "GetProductsForSubscriptionResponse_ProductCatalogDetails.xml";

  @Mock
  private CustomerInventoryStub customerInventoryStub;

  @Spy
  private ProductBrowserServiceImpl productBrowserServiceImpl;

  @Before
  public void setUp() {}

  @Test
  public void testGetSubscriptionsForParty() throws XmlException, IOException, Error {

    when(customerInventoryStub.getSubscriptionsForParty(any(GetSubscriptionsForPartyRequestDocument.class), any(EsbParam.class))).thenReturn(fromFileSource(FILE_RESOURCE_RESPONSE_SUBSCRIPTIONS_FOR_PARTY));

    GetSubscriptionsForPartyResponseDocument responseDoc = customerInventoryStub.getSubscriptionsForParty(new GetSubscriptionsForPartyRequestDocumentImpl(null), null);
    assertNotNull(responseDoc);
    GetSubscriptionsForPartyResponseType resp = responseDoc.getGetSubscriptionsForPartyResponse();
    assertNotNull(resp);
    resp.getSubscriptions();
    assertEquals(2, resp.getSubscriptions().getSubscriptionArray().length);
    Subscription subscription = resp.getSubscriptions().getSubscriptionArray(0);
    assertEquals("899999997212761", subscription.getId());
    assertEquals("200007874513", subscription.getCustomerAccount().getAccountNumber());
    assertEquals("43", subscription.getCallNumber().getCC());
    assertEquals("7229", subscription.getCallNumber().getNDC());
    assertEquals("63651", subscription.getCallNumber().getSN());
    assertEquals("Gewerbepark-Wagram 7", subscription.getAddress().getFormattedAddress().getAddressLine1());
    assertEquals("4061 Pasching", subscription.getAddress().getFormattedAddress().getAddressLine2());
    assertEquals("Wireline", subscription.getType());
  }

  @Test
  public void testGetProductsForSubscription() throws XmlException, IOException, Error {

    when(customerInventoryStub.getProductsForSubscription(any(GetProductsForSubscriptionRequestDocument.class), any(EsbParam.class))).thenReturn(fromFileSource2(FILE_RESOURCE_RESPONSE_PRODUCTS_FOR_SUBSCRIPTION));

    GetProductsForSubscriptionResponseDocument responseDoc = customerInventoryStub.getProductsForSubscription(new GetProductsForSubscriptionRequestDocumentImpl(null), null);
    assertNotNull(responseDoc);
    GetProductsResponseType resp = responseDoc.getGetProductsForSubscriptionResponse();
    assertNotNull(resp);
    Subscription subscription = resp.getSubscription();
    assertEquals("899999997212761", subscription.getId());
    assertEquals("200007874513", subscription.getCustomerAccount().getAccountNumber());
    assertEquals(1, resp.getSubscription().getProducts().sizeOfProductArray());
    ProductBundle bundle = (ProductBundle) resp.getSubscription().getProducts().getProductArray(0);
    assertNotNull(bundle);
    assertEquals("alte POTS Produkte", bundle.getName());
    assertEquals("A1", bundle.getBrand());
    assertEquals("43", subscription.getCallNumber().getCC());
    assertEquals("7229", subscription.getCallNumber().getNDC());
    assertEquals("63651", subscription.getCallNumber().getSN());
    assertEquals("Gewerbepark-Wagram 7", subscription.getAddress().getFormattedAddress().getAddressLine1());
    assertEquals("4061 Pasching", subscription.getAddress().getFormattedAddress().getAddressLine2());
    assertEquals("Wireline", subscription.getType());
  }

  @Test
  @Ignore
  // reactivate when getProductsForSubscriptions delivers ProductCatalogDetails
  public void testGetProductsForSubscriptionProductCatalogDetails() throws XmlException, IOException, Error {

    when(customerInventoryStub.getProductsForSubscription(any(GetProductsForSubscriptionRequestDocument.class), any(EsbParam.class))).thenReturn(fromFileSource2(FILE_RESOURCE_RESPONSE_PRODUCTS_FOR_SUBSCRIPTION_PRODUCT_CATALOG_DETAILS));

    GetProductsForSubscriptionResponseDocument responseDoc = customerInventoryStub.getProductsForSubscription(new GetProductsForSubscriptionRequestDocumentImpl(null), null);
    assertNotNull(responseDoc);
    GetProductsResponseType resp = responseDoc.getGetProductsForSubscriptionResponse();
    assertNotNull(resp);

    for (Product product : resp.getSubscription().getProducts().getProductArray()) {
      if (product instanceof ProductBundle) {
        ProductBundle productBundle = (ProductBundle) product;
        assertTrue(productBrowserServiceImpl.isTv(productBundle));
      }
    }
  }

  private GetSubscriptionsForPartyResponseDocument fromFileSource(String file) throws IOException, XmlException {
    return GetSubscriptionsForPartyResponseDocument.Factory.parse(FileUtils.readFileToString(getClasspathResource(file).getFile()));
  }

  private GetProductsForSubscriptionResponseDocument fromFileSource2(String file) throws IOException, XmlException {
    return GetProductsForSubscriptionResponseDocument.Factory.parse(FileUtils.readFileToString(getClasspathResource(file).getFile()));
  }

  private Resource getClasspathResource(String file) {
    return new ClassPathResource("at/a1ta/cuco/core/dao/esb/" + file);
  }
}
