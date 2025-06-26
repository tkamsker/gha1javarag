package at.a1ta.cuco.core.service.customerequipment;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.Serializable;
import java.math.BigDecimal;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Collections;
import java.util.Comparator;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;

import org.apache.commons.io.FileUtils;
import org.apache.commons.lang.StringUtils;
import org.apache.commons.lang.time.FastDateFormat;
import org.apache.commons.lang3.SerializationUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.codahale.metrics.annotation.Metered;
import com.telekomaustriagroup.esb.customerinventory.CustomerInventoryStub;

import at.a1ta.bite.core.server.dao.EsbAccessParameterDao;
import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.LocalSettingService;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.server.service.TextService;
import at.a1ta.bite.core.shared.Separator;
import at.a1ta.bite.core.shared.dto.Text;
import at.a1ta.cuco.core.dao.esb.BrianCeeQueryOrderDao;
import at.a1ta.cuco.core.service.CustomerEquipmentService;
import at.a1ta.cuco.core.service.MarketplaceInventoryService;
import at.a1ta.cuco.core.service.PartyService;
import at.a1ta.cuco.core.service.ProductBrowserService;
import at.a1ta.cuco.core.shared.dto.IndexationStatus;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.customerequipment.Equipment;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentConsignee;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentTree;
import at.a1ta.cuco.core.shared.dto.product.AccountNode;
import at.a1ta.cuco.core.shared.dto.product.AsyncPlaceholderNode;
import at.a1ta.cuco.core.shared.dto.product.BaseNode;
import at.a1ta.cuco.core.shared.dto.product.BaseNode.DISPLAY;
import at.a1ta.cuco.core.shared.dto.product.BillableUser;
import at.a1ta.cuco.core.shared.dto.product.CallNumber;
import at.a1ta.cuco.core.shared.dto.product.CuCoComponentProductPrice;
import at.a1ta.cuco.core.shared.dto.product.CuCoPrice;
import at.a1ta.cuco.core.shared.dto.product.CuCoProdPriceAlterations;
import at.a1ta.cuco.core.shared.dto.product.CuCoProdPriceAlterations.ProdPriceAlterationType;
import at.a1ta.cuco.core.shared.dto.product.CuCoProdPriceCharge;
import at.a1ta.cuco.core.shared.dto.product.CuCoProdPriceCharge.ProdPriceChargeType;
import at.a1ta.cuco.core.shared.dto.product.DefaultProductNode;
import at.a1ta.cuco.core.shared.dto.product.DefaultProductNode.DefaultProductNodeType;
import at.a1ta.cuco.core.shared.dto.product.DefaultProductNode.ProductPromotionStatus;
import at.a1ta.cuco.core.shared.dto.product.DefaultProductNode.ProductType;
import at.a1ta.cuco.core.shared.dto.product.DefaultSubscriptionNode;
import at.a1ta.cuco.core.shared.dto.product.DefaultSubscriptionType;
import at.a1ta.cuco.core.shared.dto.product.EmptyProductNode;
import at.a1ta.cuco.core.shared.dto.product.GeoCallNumber;
import at.a1ta.cuco.core.shared.dto.product.LastMileId;
import at.a1ta.cuco.core.shared.dto.product.Location;
import at.a1ta.cuco.core.shared.dto.product.Location.LocationType;
import at.a1ta.cuco.core.shared.dto.product.LocationNode;
import at.a1ta.cuco.core.shared.dto.product.MetaData;
import at.a1ta.cuco.core.shared.dto.product.MetaDataEntry;
import at.a1ta.cuco.core.shared.dto.product.MetaDataEntryType;
import at.a1ta.cuco.core.shared.dto.product.Node;
import at.a1ta.cuco.core.shared.dto.product.NodeHelper;
import at.a1ta.cuco.core.shared.dto.product.PartyNode;
import at.a1ta.cuco.core.shared.dto.product.PhysicalResourceNode;
import at.a1ta.cuco.core.shared.dto.product.ProductTree;
import at.a1ta.cuco.core.shared.dto.product.SAPPhysicalResourceNode;
import at.a1ta.cuco.core.shared.dto.product.SAPProductNode;
import at.a1ta.cuco.core.shared.dto.product.SAPSubscriptionNode;
import at.a1ta.cuco.core.shared.dto.product.SubscriptionNode;
import at.a1ta.cuco.core.shared.dto.product.SubscriptionTree;
import at.a1telekom.cdm.common.Money;
import at.a1telekom.eai.customerinventory.AllowanceProdPriceAlteration;
import at.a1telekom.eai.customerinventory.ComponentProdPrice;
import at.a1telekom.eai.customerinventory.GetProductsForSubscriptionRequestDocument;
import at.a1telekom.eai.customerinventory.GetProductsForSubscriptionRequestType;
import at.a1telekom.eai.customerinventory.GetProductsForSubscriptionResponseDocument;
import at.a1telekom.eai.customerinventory.GetProductsResponseType;
import at.a1telekom.eai.customerinventory.GetSubscriptionsForPartyRequestDocument;
import at.a1telekom.eai.customerinventory.GetSubscriptionsForPartyRequestType;
import at.a1telekom.eai.customerinventory.GetSubscriptionsForPartyRequestType.LoadOptions;
import at.a1telekom.eai.customerinventory.GetSubscriptionsForPartyResponseDocument;
import at.a1telekom.eai.customerinventory.GetSubscriptionsForPartyResponseType;
import at.a1telekom.eai.customerinventory.OneTimeChargeProdPriceCharge;
import at.a1telekom.eai.customerinventory.OneTimeDiscountProdPriceAlteration;
import at.a1telekom.eai.customerinventory.PhysicalResource;
import at.a1telekom.eai.customerinventory.ProdPriceAlteration;
import at.a1telekom.eai.customerinventory.ProdPriceCharge;
import at.a1telekom.eai.customerinventory.Product;
import at.a1telekom.eai.customerinventory.Product.BundledProductList;
import at.a1telekom.eai.customerinventory.Product.BundledProductList.BundledProduct;
import at.a1telekom.eai.customerinventory.ProductBundle;
import at.a1telekom.eai.customerinventory.ProductCharacteristicValue;
import at.a1telekom.eai.customerinventory.ProductCommitment;
import at.a1telekom.eai.customerinventory.ProductComponent;
import at.a1telekom.eai.customerinventory.ProductPrice;
import at.a1telekom.eai.customerinventory.ProductTermValue;
import at.a1telekom.eai.customerinventory.RecurringChargeProdPriceCharge;
import at.a1telekom.eai.customerinventory.RecurringDiscountProdPriceAlteration;
import at.a1telekom.eai.customerinventory.RequestPagination;
import at.a1telekom.eai.customerinventory.SubRelatedCallNumber;
import at.a1telekom.eai.customerinventory.Subscription;
import at.a1telekom.eai.customerinventory.TechnicalSubscription;
import at.a1telekom.eai.customerinventory.impl.ProductBundleImpl;
import at.a1telekom.eai.customerinventory.impl.ProductCommitmentImpl;
import at.mobilkom.brian.wsdl.AttributeRec;
import at.mobilkom.brian.wsdl.BrianCeeQueryOrderResponse;
import at.mobilkom.brian.wsdl.BrianCeeQueryOrderResponseDocument;
import at.mobilkom.brian.wsdl.CeeOrderRec;
import at.mobilkom.brian.wsdl.CeeQOrderResponseRec;

@Service
public class ProductBrowserServiceImpl extends BaseEsbClient<CustomerInventoryStub> implements ProductBrowserService {
  private static final String DD_MM_YYYY = "dd.MM.yyyy";

  private static final Logger logger = LoggerFactory.getLogger(ProductBrowserServiceImpl.class);

  private static final boolean GET_SAP_EQUIPMENT = false;

  private CustomerEquipmentService customerEquipmentService;
  private PartyService partyService;
  private TextService textService;
  private SettingService settingService;
  private String getSubscriptionForPartyRequestPartyId = "";
  private String getSubscriptionForPartyRequestXml = "";
  private String getSubscriptionForPartyResponseXml = "";
  private String getSubscriptionForPartyRequestResponseXml = "";
  private String getProductsForSubscriptionRequestCallNumber = "";
  private String getProductsForSubscriptionRequestXml = "";
  private String getProductsForSubscriptionResponseXml = "";
  private String getProductsForSubscriptionRequestResponseXml = "";
  private EsbAccessParameterDao esbAccessParameterDao;
  private String esbServiceEndPointUrl = "";

  private LinkedHashSet<String> filesToZipList = new LinkedHashSet<String>();

  @Autowired
  private BrianCeeQueryOrderDao brianCeeQueryOrderDao;

  @Autowired
  private LocalSettingService localSettingService;

  @Autowired
  private MarketplaceInventoryService marketplaceInventoryService;

  @Override
  @Metered(name = "ProductBrowser.getSubscriptionTree", absolute = true)
  public ProductTree getSubscriptionTree(ArrayList<Long> partyIds, String sessionId, boolean hasAuthorityToSeeCustomerInventoryXMLs) {
    HashMap<Long, ArrayList<Location>> locations = new HashMap<Long, ArrayList<Location>>();

    ArrayList<BaseNode> partyNodes = new ArrayList<BaseNode>();

    for (Long partyId : partyIds) {
      final PartyNode partyNode = createPartyNode(locations, partyId);
      partyNodes.add(partyNode);
    }

    ProductTree result = new ProductTree();
    result.setLocationMap(locations);
    result.setPartyNodes(partyNodes);
    return result;
  }

  private PartyNode createPartyNode(HashMap<Long, ArrayList<Location>> locations, Long partyId) {
    PartyNode partyNode = new PartyNode();
    partyNode.setPartyId(partyId);

    Party party = partyService.get(partyId);
    partyNode.setId(partyId + "");
    partyNode.setName(party.getName());
    partyNode.setAddress(party.getFullAddress());
    partyNode.setIdxStatus(party.getIdxStatus());
    HashMap<String, ArrayList<Subscription>> locationSubscriptionsMap = getLocationSubscriptionsMap(partyId);

    for (Entry<String, ArrayList<Subscription>> locationSubscriptionEntry : locationSubscriptionsMap.entrySet()) {
      String locationId = locationSubscriptionEntry.getKey();
      ArrayList<Subscription> subscriptions = locationSubscriptionEntry.getValue();

      Subscription firstSubscription = subscriptions.get(0);

      String address = "Keine Adresse";

      if (firstSubscription.getAddress() != null && firstSubscription.getAddress().getFormattedAddress() != null) {
        address = StringUtils.defaultIfBlank(firstSubscription.getAddress().getFormattedAddress().getAddressLine1(), "").trim();
        address += ", " + StringUtils.defaultIfBlank(firstSubscription.getAddress().getFormattedAddress().getAddressLine2(), "").trim();
        address += (StringUtils.isNotBlank(firstSubscription.getAddress().getFormattedAddress().getAddressLine3()) ? " " : "")
            + firstSubscription.getAddress().getFormattedAddress().getAddressLine3().trim();
      }

      LocationNode locationNode;
      Location location = getLocationForParty(locations, partyId, locationId, address);
      if (location != null) {
        locationNode = getLocationNodeByLocation(partyNode, location);
      } else {
        location = new Location();
        location.setAddress(address);

        parseAddressDetails(address, location);

        location.setLocationId(locationId);
        location.setPartyId(partyId);

        locationNode = new LocationNode();
        locationNode.setId(locationId);
        locationNode.setParent(partyNode);
        partyNode.addChild(locationNode);
        locationNode.setLocation(location);

        if (!locations.containsKey(partyId)) {
          locations.put(partyId, new ArrayList<Location>());
        }
        locations.get(partyId).add(location);
      }

      mapSubscritionTreeToParent(subscriptions, locationNode);
    }

    try {
      ArrayList<EquipmentConsignee> consignees = new ArrayList<EquipmentConsignee>();
      if (GET_SAP_EQUIPMENT) {
        consignees = customerEquipmentService.getEquipmentConsignees(partyId);
      }

      for (EquipmentConsignee consignee : consignees) {
        String address = StringUtils.defaultIfBlank(consignee.getStreet(), "").trim();
        address += StringUtils.isEmpty(consignee.getHouseNumber()) ? "" : " " + StringUtils.defaultIfBlank(consignee.getHouseNumber(), "").trim();
        address += ", " + StringUtils.defaultIfBlank(consignee.getPlz(), "").trim();
        address += StringUtils.isEmpty(consignee.getCity()) ? "" : " " + StringUtils.defaultIfBlank(consignee.getCity(), "").trim();
        address = address.trim();

        String name = StringUtils.defaultIfBlank(consignee.getName1(), "").trim();
        name += " " + StringUtils.defaultIfBlank(consignee.getName2(), "").trim();
        name = name.trim();

        LocationNode locationNode = new LocationNode();
        Location location = getLocationForPartyByAddress(locations, partyId, address);
        if (location != null) {
          locationNode = getLocationNodeByLocation(partyNode, location);
        } else {

          location = new Location();
          location.setAddress(address);
          location.setLocationId(consignee.getConsignee());
          location.setPartyId(partyId);

          locationNode = new LocationNode();
          locationNode.setId(location.getLocationId());
          locationNode.setLocation(location);
          partyNode.addChild(locationNode);
          locationNode.setParent(partyNode);

          if (!locations.containsKey(partyId)) {
            locations.put(partyId, new ArrayList<Location>());
          }
          locations.get(partyId).add(location);

        }

        SAPSubscriptionNode subscriptionNode = new SAPSubscriptionNode();
        subscriptionNode.setId(consignee.getId());
        subscriptionNode.setConsigneeId(consignee.getConsignee());
        subscriptionNode.setConsigneeName(name);

        subscriptionNode.setParent(locationNode);
        locationNode.addChild(subscriptionNode);

        AsyncPlaceholderNode placeholderNode = new AsyncPlaceholderNode();
        placeholderNode.setId("0");
        placeholderNode.setParent(subscriptionNode);
        subscriptionNode.addChild(placeholderNode);
      }
    } catch (Exception e) {
      logger.error(e.getMessage(), e);
      throw new RuntimeException("An error occurred during the getEquipmentConsignees call: " + e.getMessage(), e);
    }

    if (settingService.getBooleanValue("productBrowser.showMarketPlaceSubscriptions", false)) {
      LocationNode locationNode = marketplaceInventoryService.getMarketplaceAccountsWithSubscriptionsForParty(partyId);

      if (locationNode != null && locationNode.getChildren() != null && locationNode.getChildren().size() > 0 && locationNode.getChildren().get(0).getChildren() != null
          && locationNode.getChildren().get(0).getChildren().size() > 0) {

        locationNode.setParent(partyNode);
        boolean unknownLocationFound = false;
        if (partyNode.getChildren() != null && !partyNode.getChildren().isEmpty()) {

          for (BaseNode node : partyNode.getChildren()) {
            if (node instanceof LocationNode && "unknown".equalsIgnoreCase(node.getId())) {
              unknownLocationFound = true;
              node.getChildren().addAll(locationNode.getChildren());
              break;
            }
          }

        }
        if (!unknownLocationFound) {
          partyNode.addChild(locationNode);
        }
      }
    }
    return partyNode;
  }

  private void parseAddressDetails(String address, Location location) {
    if (address != null) {
      String[] split = address.split(", ");
      if (split.length == 2) {
        location.setStreet(split[0].trim());
        location.setPoBox(split[1].substring(0, 4));
        location.setCity(split[1].substring(4).trim());
      }
    }
  }

  private LocationType translateLocationType(LocationType oldLocationType, DefaultSubscriptionNode subscriptionNode) {
    LocationType locationType = oldLocationType;

    if (subscriptionNode.getType() != null) {
      if (subscriptionNode.getType().equals(DefaultSubscriptionType.Mixed) || subscriptionNode.getType().equals(DefaultSubscriptionType.Unknown)) {
        locationType = LocationType.HYBRID;
      } else if (subscriptionNode.getType().equals(DefaultSubscriptionType.Mobile)) {
        if (locationType == null) {
          locationType = LocationType.MOBILE;
        } else if (locationType != LocationType.MOBILE) {
          locationType = LocationType.HYBRID;
        }
      } else if (subscriptionNode.getType().equals(DefaultSubscriptionType.Wireline)) {
        if (locationType == null) {
          locationType = LocationType.FIXED;
        } else if (locationType != LocationType.FIXED) {
          locationType = LocationType.HYBRID;
        }
      }
    }
    return locationType;
  }

  public void mapSubscritionTreeToParent(Iterable<Subscription> subscriptions, LocationNode parent) {
    LinkedHashMap<String, AccountNode> accounts = new LinkedHashMap<String, AccountNode>();

    LocationType locationType = parent.getLocationTypeFormLocation();

    for (Subscription subscription : subscriptions) {
      BaseNode parentNodeForSubscription = parent;
      String accountNumber = null;
      if (subscription.getCustomerAccount() != null) {

        accountNumber = StringUtils.defaultIfBlank(subscription.getCustomerAccount().getAccountNumber(), "");
        if (accountNumber.startsWith("A") || accountNumber.startsWith("a")) {
          accountNumber = accountNumber.replaceFirst("A", "").replaceFirst("a", "");
        }
        AccountNode accountNode = accounts.get(accountNumber);
        if (null == accountNode) {
          accountNode = AccountNode.builder().accountNumber(accountNumber).parent(parent).build();
          if (subscription.isSetPartyId() && subscription.getPartyId() != null && !subscription.getPartyId().isEmpty()) {
            accountNode.setPartyId(Long.parseLong(subscription.getPartyId()));
          }
          parent.addChild(accountNode);
          accounts.put(accountNumber, accountNode);
        }
        accountNode.setIdxStatus(subscription.getCustomerAccount().isSetIdxExemption() ? subscription.getCustomerAccount().getIdxExemption() ? IndexationStatus.NOT_INDEXED : IndexationStatus.INDEXED
            : IndexationStatus.NOT_AVAILABLE);

        if ("true".equalsIgnoreCase(settingService.getValue("productBrowser.showMAMInfo"))) {
          accountNode.setContractSegment(subscription.getCustomerAccount().getAccountType());
        } else {
          accountNode.setContractSegment("DISABLED");
        }
        parentNodeForSubscription = accountNode;
      }

      DefaultSubscriptionNode subscriptionNode = prepareSubscriptionNode(subscription, parentNodeForSubscription, accountNumber);
      locationType = translateLocationType(locationType, subscriptionNode);
    }

    if (null != parent.getLocation()) {
      parent.getLocation().setLocationType(locationType);
    }
  }

  private DefaultSubscriptionNode prepareSubscriptionNode(Subscription subscription, BaseNode parentNodeForSubscription, String accountNumber) {
    DefaultSubscriptionNode subscriptionNode = new DefaultSubscriptionNode();
    subscriptionNode.setLinkedSubscriptionId(subscription.getId());
    subscriptionNode.setParent(parentNodeForSubscription);
    if (subscription.isSetPartyId() && subscription.getPartyId() != null && !subscription.getPartyId().isEmpty()) {
      subscriptionNode.setPartyId(Long.parseLong(subscription.getPartyId()));
    }
    if (parentNodeForSubscription != null) {
      parentNodeForSubscription.addChild(subscriptionNode);
      subscriptionNode.setIntendedUIDisplay(DISPLAY.BROWSER);
    } else {
      subscriptionNode.setIntendedUIDisplay(DISPLAY.TABLE);
    }
    if (accountNumber == null && subscription.getCustomerAccount() != null) {
      accountNumber = StringUtils.defaultIfBlank(subscription.getCustomerAccount().getAccountNumber(), "");
      if (accountNumber.startsWith("A") || accountNumber.startsWith("a")) {
        accountNumber = accountNumber.replaceFirst("A", "").replaceFirst("a", "");
      }
    }

    subscriptionNode.setId(subscription.getId());
    subscriptionNode.setSubscriptionId(subscription.getId());
    subscriptionNode.setAccountNumber(accountNumber);
    subscriptionNode.setVertragNoForDisplay(formatBEN(subscription));

    subscriptionNode.setIdxStatus(subscription.isSetIdxExemption() ? subscription.getIdxExemption() ? IndexationStatus.NOT_INDEXED : IndexationStatus.INDEXED : IndexationStatus.NOT_AVAILABLE);
    at.a1telekom.cdm.common.CallNumber phoneNumber = null;

    if (subscription.getRelatedCallNumbers() != null && subscription.getRelatedCallNumbers().getSubRelatedCallNumberArray() != null) {
      for (SubRelatedCallNumber subRelatedCallNumber : subscription.getRelatedCallNumbers().getSubRelatedCallNumberArray()) {
        if (subRelatedCallNumber.getType().equalsIgnoreCase(textService.getByKeyWithDefaultText("newProductOverviewGeoCallNumberTypeMatchString", "GeoNumber").getText())) {
          phoneNumber = subRelatedCallNumber.getCallNumber();
          if (phoneNumber != null) {
            subscriptionNode.setGeoCallNumber(new GeoCallNumber(phoneNumber.getCC(), phoneNumber.getNDC(), phoneNumber.getSN()));
          }
          break;
        }
      }
    }

    if (subscription.getCallNumber() != null) {
      subscriptionNode.setCallNumber(getCallNumber(subscription));
      if (subscription.getType().equalsIgnoreCase(textService.getByKeyWithDefaultText("newProductOverviewLastMileIdCallNumberTypeMatchString", "LastMile").getText())) {
        subscriptionNode.setLastMileId(new LastMileId(subscription.getCallNumber().getCC(), subscription.getCallNumber().getNDC(), subscription.getCallNumber().getSN()));
      }
    }
    if (subscription.getCallNumber() == null && subscriptionNode.getLastMileId() == null) {
      if (subscription.getBillableUser() != null && settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false)) {
        subscriptionNode.setBillableUser(new BillableUser(subscription.getBillableUser().getUsername()));
      } else {
        subscriptionNode.setCallNumber(new CallNumber("Keine LastMileId/Rufnummer", "", ""));
        if (settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false)) {
          subscriptionNode.setBillableUser(new BillableUser("Keine BillableUser"));
        }
      }
    }
    subscriptionNode.setType(translateSubscriptionType(subscription.getType()));
    subscriptionNode.setTypeText(subscription.getType());

    setProductBrowserAdditionalInfoIconsAccessibility(subscription, subscriptionNode);

    if (subscription.getAddress() != null && subscription.getAddress().getFormattedAddress() != null) {
      subscriptionNode.setAddress1(StringUtils.defaultIfBlank(subscription.getAddress().getFormattedAddress().getAddressLine1(), "").trim());
      subscriptionNode.setAddress2(StringUtils.defaultIfBlank(subscription.getAddress().getFormattedAddress().getAddressLine2(), "").trim());
      subscriptionNode.setAddress3(StringUtils.defaultIfBlank(subscription.getAddress().getFormattedAddress().getAddressLine3(), "").trim());
    }

    AsyncPlaceholderNode placeholderNode = new AsyncPlaceholderNode();
    placeholderNode.setId("0");

    if (subscriptionNode.getIntendedUIDisplay() != DISPLAY.TABLE) {
      placeholderNode.setParent(subscriptionNode);
      subscriptionNode.addChild(placeholderNode);
    }
    return subscriptionNode;
  }

  private void setProductBrowserAdditionalInfoIconsAccessibility(Subscription subscription, DefaultSubscriptionNode subscriptionNode) {
    String allowedTypesForFeasibilityCheck = settingService.getValue("tableViewFeasibilityCheckAllowedTypes");
    String allowedTypesForA1CoachLink = settingService.getValue("tableViewA1CoachLinkAllowedTypes");
    subscriptionNode.setFeasibilityCheckAvailable(!(subscription.getType() != null
        && Arrays.asList((allowedTypesForFeasibilityCheck == null ? "" : allowedTypesForFeasibilityCheck).split(Separator.SEMICOLON)).contains(subscription.getType())));
    subscriptionNode.setDisplayA1CoachLink(
        (subscription.getType() != null && Arrays.asList((allowedTypesForA1CoachLink == null ? "" : allowedTypesForA1CoachLink).split(Separator.SEMICOLON)).contains(subscription.getType())));
  }

  private String formatBEN(Subscription subscription) {
    String billingArrangementNumber = subscription.getBillingArrangement() != null ? subscription.getBillingArrangement().getBillingArrangementNumber().trim() : "";
    if (billingArrangementNumber.toUpperCase().startsWith("A")) {
      billingArrangementNumber = billingArrangementNumber.toUpperCase().replaceFirst("A", "");
    }
    if (billingArrangementNumber.contains(",")) {
      String[] split = billingArrangementNumber.split(",");
      billingArrangementNumber = split[0] + "/" + split[1].replaceAll("^0+", "");
    }

    return billingArrangementNumber;
  }

  private Location getLocationForParty(HashMap<Long, ArrayList<Location>> locations, Long partyId, String locationId, String address) {
    Location location = null;
    location = getLocationForPartyByLocationId(locations, partyId, locationId);
    if (location == null) {
      location = getLocationForPartyByAddress(locations, partyId, address);
    }
    if (location != null && location.getLocationId() == null) {
      location.setLocationId(locationId);
    }
    return location;
  }

  private Location getLocationForPartyByLocationId(HashMap<Long, ArrayList<Location>> locations, Long partyId, String locationId) {
    if (locationId != null) {
      if (!locations.containsKey(partyId)) {
        return null;
      }
      for (Location loc : locations.get(partyId)) {
        if (locationId.equals(loc.getLocationId())) {
          return loc;
        }
      }
    }
    return null;
  }

  private Location getLocationForPartyByAddress(HashMap<Long, ArrayList<Location>> locations, Long partyId, String address) {
    if (address != null) {
      if (!locations.containsKey(partyId)) {
        return null;
      }
      for (Location loc : locations.get(partyId)) {
        if (loc.getAddress().equals(address)) {
          return loc;
        }
      }
    }
    return null;
  }

  private LocationNode getLocationNodeByLocation(PartyNode partyNode, Location location) {
    for (Node node : partyNode.getChildren()) {
      if (node instanceof LocationNode) {
        if (((LocationNode) node).getLocation().equals(location)) {
          return (LocationNode) node;
        }
      }
    }
    return null;
  }

  private DefaultSubscriptionType translateSubscriptionType(String type) {
    try {
      return DefaultSubscriptionType.valueOf(type);
    } catch (Exception e) {
      return DefaultSubscriptionType.Unknown;
    }
  }

  public HashMap<String, ArrayList<Subscription>> getLocationSubscriptionsMap(long partyId) {
    try {

      HashMap<String, ArrayList<Subscription>> locationSubscriptionMap = new HashMap<String, ArrayList<Subscription>>();
      GetSubscriptionsForPartyResponseType resp;
      String mockResponseFileName = System.getProperty("catalina.base") + "//mocks//CI_getSubscriptionsForParty_CMSYS3218.xml";
      if (settingService.getBooleanValue("testModeActive", false) && settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false)
          && new File(mockResponseFileName).exists()) {
        resp = GetSubscriptionsForPartyResponseDocument.Factory.parse(FileUtils.readFileToString(new File(mockResponseFileName))).getGetSubscriptionsForPartyResponse();
      } else {
        GetSubscriptionsForPartyResponseDocument respDoc = stub.getSubscriptionsForParty(prepareRequestForGetSubsForParty(partyId, true, true, false, true,
            (settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false) ? true : false), true, 1), null);
        resp = respDoc.getGetSubscriptionsForPartyResponse();
      }

      if (resp.getSubscriptions() == null || resp.getSubscriptions().getSubscriptionArray() == null) {
        return locationSubscriptionMap;
      }
      for (Subscription subscription : resp.getSubscriptions().getSubscriptionArray()) {
        String locationId = (subscription.getAddress() == null || !subscription.getAddress().isSetLkmsId() || subscription.getAddress().getLkmsId() == null) ? "unknown"
            : subscription.getAddress().getLkmsId();

        if (!locationSubscriptionMap.containsKey(locationId)) {
          locationSubscriptionMap.put(locationId, new ArrayList<Subscription>());
        }

        ArrayList<Subscription> currSubscriptions = locationSubscriptionMap.get(locationId);
        currSubscriptions.add(subscription);
      }

      return locationSubscriptionMap;
    } catch (Exception e) {
      logger.error(e.getMessage(), e);
      throw new RuntimeException("An error occurred during the getSubscriptionsForParty call: " + e.getMessage(), e);
    }
  }

  private GetSubscriptionsForPartyRequestDocument prepareRequestForGetSubsForParty(Long partyId, boolean getFixedNet, boolean getMobileNet, boolean getProducts, boolean getLocation,
      boolean getBillableUser, boolean getTopLevelProductsOnly, int pageNumber) {
    GetSubscriptionsForPartyRequestDocument reqDoc = GetSubscriptionsForPartyRequestDocument.Factory.newInstance();
    GetSubscriptionsForPartyRequestType req = GetSubscriptionsForPartyRequestType.Factory.newInstance();
    req.setPartyId(partyId + "");
    req.setLoadOptions(getLoadOptionsForGetSubsForParty(getFixedNet, getMobileNet, getProducts, getLocation, getBillableUser, getTopLevelProductsOnly, pageNumber));

    reqDoc.setGetSubscriptionsForPartyRequest(req);
    getSubscriptionForPartyRequestPartyId = partyId + "";
    getSubscriptionForPartyRequestXml = "<request>" + "\n" + reqDoc.toString() + "\n" + "</request>";
    return reqDoc;
  }

  // This method is called from CalcTool to load prices for a ban
  @Override
  public Product[] getProductsForCustomerAccount(String ban, String partyId) {
    try {
      if (ban == null || ban.toString().isEmpty() || partyId == null || partyId.isEmpty()) {
        logger.error("Invalid Request for getProductsForCustomerAccount , BAN is not sent with request : BAN=" + ban);
        throw new RuntimeException("Invalid Request for getProductsForCustomerAccount , BAN is not sent with request : BAN=" + ban);
      }

      // addiing prefix for amdocs accounts as requested by customer inventory
      if (!ban.startsWith("A") && !ban.startsWith("a")) {
        ban = "A" + ban.trim();
      }
      GetSubscriptionsForPartyResponseType resp;
      GetSubscriptionsForPartyRequestDocument request = prepareRequestForGetSubsForParty(Long.parseLong(partyId), false, true, true, false,
          (settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false) ? true : false), false, 1);
      request.getGetSubscriptionsForPartyRequest().setCustomerAccountNumber(ban);
      String mockResponseFileName = System.getProperty("catalina.base") + "//mocks//CI_getSubscriptionsForParty_CMSYS3218.xml";
      if (settingService.getBooleanValue("testModeActive", false) && settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false)
          && new File(mockResponseFileName).exists()) {
        resp = GetSubscriptionsForPartyResponseDocument.Factory.parse(FileUtils.readFileToString(new File(mockResponseFileName))).getGetSubscriptionsForPartyResponse();
      } else {
        GetSubscriptionsForPartyResponseDocument respDoc = stub.getSubscriptionsForParty(request, null);
        resp = respDoc.getGetSubscriptionsForPartyResponse();
      }

      if (resp == null || !resp.isSetSubscriptions()) {
        return null;
      }
      List<Product> productLists = new ArrayList<Product>();

      for (Subscription subscription : resp.getSubscriptions().getSubscriptionArray()) {
        if (subscription.isSetProducts()) {
          Collections.addAll(productLists, subscription.getProducts().getProductArray());
        }
      }

      while (!resp.getPagination().getIsLastPage()) {
        request = prepareRequestForGetSubsForParty(Long.parseLong(partyId), false, true, true, false,
            (settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false) ? true : false), false, resp.getPagination().getPageNumber() + 1);
        request.getGetSubscriptionsForPartyRequest().setCustomerAccountNumber(ban);

        GetSubscriptionsForPartyResponseDocument respDoc = stub.getSubscriptionsForParty(request, null);
        resp = respDoc.getGetSubscriptionsForPartyResponse();

        if (resp == null || !resp.isSetSubscriptions()) {
          return productLists.toArray(new Product[productLists.size()]);
        }

        for (Subscription subscription : resp.getSubscriptions().getSubscriptionArray()) {
          if (subscription.isSetProducts()) {
            Collections.addAll(productLists, subscription.getProducts().getProductArray());
          }
        }
      }

      return productLists.toArray(new Product[productLists.size()]);
    } catch (Exception e) {
      logger.error(e.getMessage(), e);
      throw new RuntimeException("An error occurred during the getProductsForCustomerAccount call: " + e.getMessage(), e);
    }
  }

  private LoadOptions getLoadOptionsForGetSubsForParty(boolean getFixedNet, boolean getMobileNet, boolean getProducts, boolean getLocation, boolean getBillableUser, boolean getTopLevelProductsOnly,
      int pageNumber) {
    LoadOptions loadOptions = LoadOptions.Factory.newInstance();
    loadOptions.setGetFixedNet(getFixedNet);
    loadOptions.setGetMobileNet(getMobileNet);
    loadOptions.setGetProducts(getProducts);
    loadOptions.setGetLocation(getLocation);
    loadOptions.setGetBillableUser(getBillableUser);
    loadOptions.setGetTopLevelProductsOnly(getTopLevelProductsOnly);
    loadOptions.setPagination(RequestPagination.Factory.newInstance());
    loadOptions.getPagination().setPageNumber(pageNumber);
    loadOptions.getPagination().setPageSize(settingService.getIntValue("productBrowser.loadOptions.getSubscriptionsForPartyPageSize", 500));
    loadOptions.setGetAccountDiscounts(true);
    loadOptions.setGetNonCDM(true);
    return loadOptions;
  }

  @Override
  public SubscriptionTree getSubscriptionTree(SubscriptionNode node, String sessionId, boolean hasAuthorityToSeeCustomerInventoryXMLs) {
    if (node instanceof DefaultSubscriptionNode) {
      return getDefaultProductNodes((DefaultSubscriptionNode) node, sessionId, hasAuthorityToSeeCustomerInventoryXMLs);
    }
    if (node instanceof SAPSubscriptionNode) {
      return getSAPProductNodes((SAPSubscriptionNode) node);
    }
    return getEmptyProductNodes();
  }

  private SubscriptionTree getSAPProductNodes(SAPSubscriptionNode node) {

    try {
      EquipmentTree equipmentTree = customerEquipmentService.getEquipmentTree(node.getConsigneeId(), NodeHelper.getPartyNode(node).getPartyId());

      SubscriptionTree tree = new SubscriptionTree();
      ArrayList<BaseNode> productNodes = new ArrayList<BaseNode>();
      tree.setProductNodes(productNodes);

      for (Equipment child : equipmentTree.getChildren()) {
        BaseNode buildSapEquipmentNode = buildSapEquipmentNode(child, null);
        buildSapEquipmentNode.setPartyId(NodeHelper.getPartyNode(node).getPartyId());
        tree.getProductNodes().add(buildSapEquipmentNode);
      }

      return tree;
    } catch (Exception e) {
      logger.error(e.getMessage(), e);
      throw new RuntimeException("An error occurred during the getEquipmentTree call: " + e.getMessage());
    }
  }

  private BaseNode buildSapEquipmentNode(Equipment equipment, BaseNode parentNode) {
    BaseNode childNode = createNode(equipment);

    if (parentNode != null) {
      childNode.setParent(parentNode);
      parentNode.addChild(childNode);
    }

    if (equipment.hasChildren()) {
      for (Equipment childEquipment : equipment.getChildren()) {
        buildSapEquipmentNode(childEquipment, childNode);
      }
    }

    return childNode;
  }

  private BaseNode createNode(Equipment equipment) {
    String name = StringUtils.defaultIfBlank(equipment.getTypBezeichnung(), "");
    name = name.isEmpty() ? "" : name + " - ";
    name += StringUtils.defaultIfBlank(equipment.getName(), equipment.getId());

    if (equipment.isMaterial()) {
      SAPPhysicalResourceNode node = new SAPPhysicalResourceNode();
      node.setId(equipment.getId());
      node.setText(name);
      node.setMetaData(MetaDataHelper.createMetaData(equipment));
      node.setEquipmentAttributes(MetaDataHelper.createMetaDataEquipmentAttributes(equipment));
      return node;
    }

    SAPProductNode node = new SAPProductNode();
    node.setText(name);
    mapEquipmentTyp(equipment);

    node.setMetaData(MetaDataHelper.createMetaData(equipment));
    node.setEquipmentAttributes(MetaDataHelper.createMetaDataEquipmentAttributes(equipment));
    return node;
  }

  private void mapEquipmentTyp(Equipment equipment) {
    if (equipment.getEquipmentTyp() != null) {
      Text text = textService.getByKeyWithDefaultText(equipment.getEquipmentTyp(), equipment.getEquipmentTyp());
      equipment.setEquipmentTyp(text.getText());
    }
  }

  private SubscriptionTree getEmptyProductNodes() {
    SubscriptionTree tree = new SubscriptionTree();
    ArrayList<BaseNode> productNodes = new ArrayList<BaseNode>();
    productNodes.add(new EmptyProductNode());
    tree.setProductNodes(productNodes);
    return tree;
  }

  // // this method is designed to be called for Product browser View
  public SubscriptionTree getDefaultProductNodes(DefaultSubscriptionNode subscriptionNode, String sessionId, boolean hasAuthorityToSeeCustomerInventoryXMLs) {
    try {
      subscriptionNode.setChildDetailsLoaded(true);
      at.a1telekom.eai.customerinventory.GetProductsRequestType.LoadOptions loadOptions = at.a1telekom.eai.customerinventory.GetProductsRequestType.LoadOptions.Factory.newInstance();
      loadOptions.setGetResources(true);
      loadOptions.setGetTerminatedProducts(false);
      loadOptions.setGetPrices(true);
      loadOptions.setGetOrderingStack(true);
      loadOptions.setGetNonCDM(true);
      loadOptions.setGetAccountDiscounts(true);
      // loadOptions.setGetProductCatalogDetails(true); // deactivated until CustomerInventoryStub really delivers data

      GetProductsForSubscriptionRequestType request = GetProductsForSubscriptionRequestType.Factory.newInstance();
      request.setLoadOptions(loadOptions);
      if (subscriptionNode.getBillableUser() == null) {
        at.a1telekom.cdm.common.CallNumber cn = request.addNewCallNumber();
        if (subscriptionNode.getLastMileId() != null) {
          cn.setCC(subscriptionNode.getLastMileId().getCountryCode());
          cn.setNDC(subscriptionNode.getLastMileId().getOnkz());
          cn.setSN(subscriptionNode.getLastMileId().getTnum());
          getProductsForSubscriptionRequestCallNumber = subscriptionNode.getLastMileId().getCountryCode() + subscriptionNode.getLastMileId().getOnkz() + subscriptionNode.getLastMileId().getTnum();
        } else if (subscriptionNode.getCallNumber() != null) {
          cn.setCC(subscriptionNode.getCallNumber().getCountryCode());
          cn.setNDC(subscriptionNode.getCallNumber().getOnkz());
          cn.setSN(subscriptionNode.getCallNumber().getTnum());
          getProductsForSubscriptionRequestCallNumber = subscriptionNode.getCallNumber().getCountryCode() + subscriptionNode.getCallNumber().getOnkz() + subscriptionNode.getCallNumber().getTnum();
        }
        request.setCallNumber(cn);
      } else if (settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false)) {
        request.setBillableUserName(subscriptionNode.getBillableUser().getUserName());
      }

      GetProductsForSubscriptionRequestDocument reqDoc = GetProductsForSubscriptionRequestDocument.Factory.newInstance();
      reqDoc.setGetProductsForSubscriptionRequest(request);
      getProductsForSubscriptionRequestXml = "<request>" + "\n" + reqDoc.toString() + "\n" + "</request>";
      GetProductsResponseType response;
      GetProductsForSubscriptionResponseDocument respDoc;
      String mockResponseFileNameForCmsys2294 = System.getProperty("catalina.base") + "//mocks//CI_getProductsForSubscription_CMSYS2294.xml";
      String mockResponseFileNameForCmsys3218 = System.getProperty("catalina.base") + "//mocks//CI_getProductsForSubscription_CMSYS3218.xml";
      if (settingService.getBooleanValue("testModeActive", false) && subscriptionNode.getId().equalsIgnoreCase("L10287438") && new File(mockResponseFileNameForCmsys2294).exists()) {
        response = GetProductsForSubscriptionResponseDocument.Factory.parse(FileUtils.readFileToString(new File(mockResponseFileNameForCmsys2294))).getGetProductsForSubscriptionResponse();
      } else if (settingService.getBooleanValue("testModeActive", false) && new File(mockResponseFileNameForCmsys3218).exists()
          && settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false)) {
        response = GetProductsForSubscriptionResponseDocument.Factory.parse(FileUtils.readFileToString(new File(mockResponseFileNameForCmsys3218))).getGetProductsForSubscriptionResponse();
        getProductsForSubscriptionResponseXml = "<response>" + "\n" + response.toString() + "\n" + "</response>";
      } else {
        respDoc = stub.getProductsForSubscription(reqDoc, null);

        response = respDoc.getGetProductsForSubscriptionResponse();
        getProductsForSubscriptionResponseXml = "<response>" + "\n" + respDoc.toString() + "\n" + "</response>";
      }
      if (!(settingService.getBooleanValue("productBrowser.createZipWithInitialPreLoadLogic", false)) && hasAuthorityToSeeCustomerInventoryXMLs
          && settingService.getBooleanValue("productBrowser.a1OneTvPart2Active", true)) {
        File createFolderForUploading = new File(getUploadPathForCustomerInventoryFolder());

        File createFolderAsPerSession = new File(createFolderForUploading + File.separator + sessionId);

        File defaultZipPathWithPartyId = new File(createFolderAsPerSession + File.separator
            + textService.getByKeyWithDefaultText("newProductOverviewCustomerInventoryDotAsPrefix", "CustomerInventory.").getText() + getSubscriptionForPartyRequestPartyId);

        getProductsForSubscriptionRequestResponseXml = "<esbWebServiceCall>" + "\n" + "<esbEndpoint> " + esbServiceEndPointUrl + " </esbEndpoint>" + "\n" + getProductsForSubscriptionRequestXml + "\n"
            + getProductsForSubscriptionResponseXml + "\n" + "</esbWebServiceCall>";
        createGetProductsForSubscriptionRequestResponseFiles(defaultZipPathWithPartyId);
        File getZipFile = new File(defaultZipPathWithPartyId + File.separator + textService.getByKeyWithDefaultText("newProductOverviewCustomerInventoryDotAsPrefix", "CustomerInventory.").getText()
            + getSubscriptionForPartyRequestPartyId + textService.getByKeyWithDefaultText("newProductOverviewReqRespZipSuffix", ".zip").getText());
        if (getZipFile.exists()) {
          getZipFile.delete();
        }
        filesToZipList.clear();
        getAllCiRequestResponseFileListToZip(defaultZipPathWithPartyId);
        createCiRequestResponseFolderZip(getZipFile.toString(), defaultZipPathWithPartyId.toString());
      }
      SubscriptionTree tree = new SubscriptionTree();
      ArrayList<BaseNode> productNodes = new ArrayList<BaseNode>();
      tree.setProductNodes(productNodes);
      tree.setSubscriptionNode(subscriptionNode);
      if (DISPLAY.TABLE == subscriptionNode.getIntendedUIDisplay()) {
        subscriptionNode.setChildren(productNodes);
      }
      if (response.getSubscription() != null && response.getSubscription().getProducts() != null && response.getSubscription().getProducts().getProductArray() != null) {
        boolean searchForChildrenWithMatchingCallNumber = settingService.getBooleanValue("productBrowser.filterBundlesWithSubscriptionID", false)
            && !subscriptionNode.getSubscriptionId().equalsIgnoreCase(response.getSubscription().getId());
        for (Product product : response.getSubscription().getProducts().getProductArray()) {
          if (DISPLAY.TABLE != subscriptionNode.getIntendedUIDisplay() || shouldAddProduct(product.getName())) {
            DefaultProductNode node = createNode(product, subscriptionNode, subscriptionNode, searchForChildrenWithMatchingCallNumber);
            node.setMatchingCallNumberWithRootSubscription(!searchForChildrenWithMatchingCallNumber);
            if (!node.hasOANProductInChildNodes()) {
              node.setHasOANProductInHiddenNodes(hasHiddenOANProducts(product));
            }
            node.setParent(subscriptionNode);
            productNodes.add(node);
            if (response.getSubscription().isSetCallNumber()) {
              node.setRootCallNumberForBundleProduct(getCallNumber(response.getSubscription()));
            } else {
              node.setRootCallNumberForBundleProduct(subscriptionNode.getCallNumber());
            }
            subscriptionNode.setRootCallNumberForBundleProduct(node.getRootCallNumberForBundleProduct());
          } else {
            productNodes.add(new EmptyProductNode());
          }
        }
        if (searchForChildrenWithMatchingCallNumber && !subscriptionNode.getChildrenWithMatchingCallNumbers().isEmpty()) {
          tree.getProductNodes().addAll(subscriptionNode.getChildrenWithMatchingCallNumbers());
          subscriptionNode.setChildrenWithMatchingCallNumbersArraySize(subscriptionNode.getChildrenWithMatchingCallNumbers().size());
        }
      } else {
        productNodes.add(new EmptyProductNode());
      }

      return tree;
    } catch (Exception e) {
      logger.error("An error occurred during the getProductsForSubscription call: " + e.getMessage(), e);
      throw new RuntimeException(e.getMessage(), e);
    }
  }

  private boolean hasHiddenOANProducts(Product product) {
    MetaData metaData = new MetaData();
    if (product instanceof ProductBundle && !isVoiceProduct(product)) {
      final ProductBundleImpl productBundle = (ProductBundleImpl) product;
      BundledProductList bundledProductList = productBundle.getBundledProductList();
      if (bundledProductList != null) {
        for (BundledProduct childProduct : bundledProductList.getBundledProductArray()) {
          metaData.put(MetaDataHelper.createMetaData(childProduct.getProduct(), new ArrayList<String>()));
          if (getOANIdentifier(metaData)) {
            return true;
          }
          if (hasHiddenOANProducts(childProduct.getProduct())) {
            return true;
          }
        }
      }
    }

    return false;
  }

  private PhysicalResourceNode createNode(PhysicalResource res) {
    PhysicalResourceNode node = new PhysicalResourceNode();
    node.setText(res.getName());
    node.setId(res.getSerialNumber());
    node.setMetaData(new MetaData());
    node.getMetaData().put(MetaDataHelper.createMetaData(res));
    return node;
  }

  private void setXploreTvUsernameProductCharacteristic(Product product, DefaultProductNode node) {

    for (TechnicalSubscription technicalSubscription : product.getTechnicalSubscriptionArray()) {
      String zappwareTypeIdentifier = "Zappware";
      String zappwareType = technicalSubscription.getType();

      if (zappwareType.equals(zappwareTypeIdentifier)) {

        try {
          BrianCeeQueryOrderResponseDocument brianCeeQueryOrderResponseDocument = brianCeeQueryOrderDao.getCeeQueryOrderResponse(technicalSubscription.getTechnicalSubscriptionId());
          BrianCeeQueryOrderResponse brianCeeQueryOrderResponse = brianCeeQueryOrderResponseDocument.getBrianCeeQueryOrderResponse();
          CeeQOrderResponseRec ceeQOrderResponseRec = brianCeeQueryOrderResponse.getCeeQueryOrderResponse();
          CeeOrderRec[] ceeOrderRecArray = ceeQOrderResponseRec.getCeeOrderArray();

          for (CeeOrderRec ceeOrderRec : ceeOrderRecArray) {
            for (AttributeRec attributeRec : ceeOrderRec.getAttributeArray()) {
              String xploreTVAttributeName = "InitHouseholdMailUser";
              if (attributeRec.getAttrName().equals(xploreTVAttributeName)) {
                MetaDataEntry dataEntry = new MetaDataEntry("A1 Xplore TV Benutzername", "getXploreTvUsername", attributeRec.getAttrValue(), MetaDataEntryType.STRING);
                node.getProductCharacteristicValuesAsMetaData().getAll().add(dataEntry);
              }
            }
          }
        } catch (Exception e) {
          logger.error("Error while retrieving xplore tv username for technicalSubscriptionId" + technicalSubscription.getTechnicalSubscriptionId(), e);
        }
      }
    }
  }

  private DefaultProductNode createNode(Product product, BaseNode parent, SubscriptionNode rootSubscriptionNode, boolean searchForChildrenWithMatchingCallNumber) {

    DefaultProductNode node = new DefaultProductNode();

    node.setDepth(parent != null ? parent.getDepth() + 1 : 0);
    node.setId(product.getProductId());
    node.setText(product.getName());
    node.setIntendedUIDisplay(parent != null ? parent.getIntendedUIDisplay() : DISPLAY.BROWSER);
    node.setMetaData(new MetaData());
    node.setPartyId(parent != null ? parent.getPartyId() : null);
    if (product.isSetSubscription()) {
      node.setLinkedSubscriptionId(product.getSubscription().getId());
    }

    if (product.isSetCallNumber()) {
      node.setCallNumber(getCallNumber(product));
      if (searchForChildrenWithMatchingCallNumber && node.getCallNumber() != null && node.getCallNumber().equals(rootSubscriptionNode.getCallNumber())) {
        node.setLinkedSubscriptionId(rootSubscriptionNode.getSubscriptionId());
      }
    }
    mapProductStatus(product);

    mapTarifs(product);
    final String autoVVLProductOfferingTermID = settingService.getValue("productBrowser.metaData.autoVVLproductOfferingTermID");
    final String blacklistValue = settingService.getValue("productBrowser.metaData.BlacklistedProductSpecCharacteristicIds");
    final String promotionAvailableProductOfferingTermValueId = settingService.getValue("productBrowser.metaData.promotionAvailableProductOfferingTermValueId");
    final String promotionNotAvailableProductOfferingTermValueId = settingService.getValue("productBrowser.metaData.promotionNotAvailableProductOfferingTermValueId");
    final String promotionAvalabilityStatusProductOfferingTermId = settingService.getValue("productBrowser.metaData.promotionAvalabilityStatusProductOfferingTermId");
    final String blacklistValuesForNewProductViewStr = textService.getByKeyWithDefaultText("admin_productBrowserTableViewBlacklist", "").getText();
    final String whitelistValuesForNewProductViewStr = textService.getByKeyWithDefaultText("admin_productBrowserTableViewWhitelist", "").getText();
    final String filterMode = settingService.getValue("productBrowser.tableView.productCharacteristic.mode");
    List<String> blacklistValuesForNewProductView = Arrays.asList((blacklistValuesForNewProductViewStr == null ? "" : blacklistValuesForNewProductViewStr).split(Separator.SEMICOLON));
    List<String> whitelistValuesForNewProductView = Arrays.asList((whitelistValuesForNewProductViewStr == null ? "" : whitelistValuesForNewProductViewStr).split(Separator.SEMICOLON));

    List<String> blacklistedProductSpecCharacteristicIdsList = Arrays.asList((blacklistValue == null ? "" : blacklistValue).split(Separator.SEMICOLON));
    ArrayList<MetaDataEntry> metaDatas = MetaDataHelper.createMetaData(product, blacklistedProductSpecCharacteristicIdsList);
    node.getMetaData().put(metaDatas);
    node.setProductCharacteristicValuesAsMetaData(new MetaData());
    node.getProductCharacteristicValuesAsMetaData()
        .put(MetaDataHelper.getProductCharacteristicValuesMetaDataEntries(product.getProductCharacteristicValues(), filterMode, blacklistValuesForNewProductView, whitelistValuesForNewProductView));

    setXploreTvUsernameProductCharacteristic(product, node);

    String productCharacteristicValues = "";
    for (MetaDataEntry entry : node.getProductCharacteristicValuesAsMetaData().getAll()) {
      productCharacteristicValues += "<pre-wrap style='font-family: Verdana;'>" + entry.getName() + ": " + entry.getValue() + "</pre-wrap>" + "<br/>";
    }
    node.setProductCharacteristicValuesAsString(productCharacteristicValues);
    node.setVoiceProductType(ProductType.UNDEFINED);
    node.setValidForStart(MetaDataHelper.getValidForStart(product.getValidFor()) != null ? FastDateFormat.getInstance(DD_MM_YYYY).format(MetaDataHelper.getValidForStart(product.getValidFor())) : "-");
    node.setValidForEnd(MetaDataHelper.getValidForEnd(product.getValidFor()) != null ? FastDateFormat.getInstance(DD_MM_YYYY).format(MetaDataHelper.getValidForEnd(product.getValidFor())) : "-");
    node.setProductName(product.getName());
    node.setProductBrand(product.getBrand());
    node.setProductStatus(product.getProductStatus());
    if (product.getProductTermValues() != null && product.getProductTermValues().getProductTermValueArray() != null) {
      for (ProductTermValue res : product.getProductTermValues().getProductTermValueArray()) {
        if (res != null && res.getProductOfferingTermValue() != null && res.getProductOfferingTermValue().getProductOfferingTerm() != null) {
          final String currentProductOfferingTermId = res.getProductOfferingTermValue().getProductOfferingTerm().getProductOfferingTermId();
          final String currentProductOfferingTermVal = res.getProductOfferingTermValue().getProductOfferingTermValueId();
          if (autoVVLProductOfferingTermID.equals(currentProductOfferingTermId)) {
            node.setProductOfferingTermId(currentProductOfferingTermId);
            node.setAutoVVLDuration(res.getProductOfferingTermValue().getValue());
          }

          if (currentProductOfferingTermId.equals(promotionAvalabilityStatusProductOfferingTermId) && promotionAvailableProductOfferingTermValueId.equals(currentProductOfferingTermVal)) {
            node.setPromotionStatus(ProductPromotionStatus.AVAILABLE);
          }
          if (currentProductOfferingTermId.equals(promotionAvalabilityStatusProductOfferingTermId) && promotionNotAvailableProductOfferingTermValueId.equals(currentProductOfferingTermVal)) {
            node.setPromotionStatus(ProductPromotionStatus.NOT_AVAILABLE);
          }

        }

        if (res instanceof ProductCommitment) {
          final ProductCommitmentImpl productCommitment = (ProductCommitmentImpl) res;
          node.setCommitmentStartDate(productCommitment.getCommitmentStart() != null ? FastDateFormat.getInstance(DD_MM_YYYY).format(productCommitment.getCommitmentStart().getTime()) : "");
          node.setCommitmentEndDate(productCommitment.getCommitmentEnd() != null ? FastDateFormat.getInstance(DD_MM_YYYY).format(productCommitment.getCommitmentEnd().getTime()) : "");
          node.setCommitmentDuration(productCommitment.getDurationMonth());
        }
      }
      if (node.getCommitmentEndDate() != null) {
        try {
          node.setAutoVVLStartDate(FastDateFormat.getInstance(DD_MM_YYYY).format(addOneDay(new SimpleDateFormat(DD_MM_YYYY).parse(node.getCommitmentEndDate()))));
        } catch (Exception e) {
          logger.error("Error While calculating autovvl end date with value " + node.getCommitmentEndDate(), e);
        }

        try {
          node.setAutoVVLEndDate(FastDateFormat.getInstance(DD_MM_YYYY)
              .format(addMonth(addOneDay(new SimpleDateFormat(DD_MM_YYYY).parse(node.getCommitmentEndDate())), node.getAutoVVLDuration() != null ? Integer.parseInt(node.getAutoVVLDuration()) : 0)));
        } catch (Exception e) {
          logger.error("Error While calculating autovvl end date with value " + node.getCommitmentEndDate() + " and autovvl duration " + node.getAutoVVLDuration(), e);
        }
      }
    }

    if (product.isSetProductPrices() && product.getProductPrices() != null && product.getProductPrices().sizeOfProductPriceArray() > 0) {

      if (settingService.getBooleanValue("idxMay2017.ProductBrowser.priceTable", false)) {
        ArrayList<CuCoProdPriceAlterations> alterations = new ArrayList<CuCoProdPriceAlterations>();
        Map<String, CuCoProdPriceCharge> charges = new HashMap<String, CuCoProdPriceCharge>();
        // extracting charges and alterations
        for (ProductPrice current : product.getProductPrices().getProductPriceArray()) {
          if (current instanceof ProdPriceCharge && ((ProdPriceCharge) current).getPrice() != null && ((ProdPriceCharge) current).getPrice().getAmount().compareTo(BigDecimal.ZERO) == 1) {
            if (current instanceof RecurringChargeProdPriceCharge) {
              CuCoComponentProductPrice extractedRecurringChargePrice = extractRecurringChargePrice((RecurringChargeProdPriceCharge) current);
              node.addToAllPrices(extractedRecurringChargePrice);
              node.addToPriceTree((CuCoProdPriceCharge) extractedRecurringChargePrice);
              charges.put(extractedRecurringChargePrice.getProductPriceId(), (CuCoProdPriceCharge) extractedRecurringChargePrice);
            } else if (current instanceof OneTimeChargeProdPriceCharge) {
              CuCoComponentProductPrice extractedOnetimeChargePrice = extractOnetimeChargePrice((OneTimeChargeProdPriceCharge) current);
              node.addToAllPrices(extractedOnetimeChargePrice);
              node.addToPriceTree((CuCoProdPriceCharge) extractedOnetimeChargePrice);
              charges.put(extractedOnetimeChargePrice.getProductPriceId(), (CuCoProdPriceCharge) extractedOnetimeChargePrice);
            }
          } else if (current instanceof ProdPriceAlteration) {
            if (current instanceof RecurringDiscountProdPriceAlteration) {
              CuCoComponentProductPrice extractedRecurringDiscountAlteration = extractRecurringDiscountAlteration((RecurringDiscountProdPriceAlteration) current);
              node.addToAllPrices(extractedRecurringDiscountAlteration);
              alterations.add((CuCoProdPriceAlterations) extractedRecurringDiscountAlteration);
              if ("POPC_ACCOUNT_LEVEL_DISCOUNT".equals(current.getProductOfferingPriceCategoryId())) {
                  CuCoProdPriceAlterations currentAlteration = (CuCoProdPriceAlterations) extractedRecurringDiscountAlteration;
                  CuCoProdPriceCharge result = new CuCoProdPriceCharge(ProdPriceChargeType.ACCOUNT_DISCOUNT);

                  result.setName(currentAlteration.getName());
                  result.setFrequency(currentAlteration.getFrequency());
                  result.setIdxStatus(currentAlteration.getIdxStatus());
                  result.setIdxStartDate(currentAlteration.getDiscountStartDate());
                  node.addToPriceTree(result);                 
              }
            } else if (current instanceof OneTimeDiscountProdPriceAlteration) {
              CuCoComponentProductPrice extractedOnetimeDiscountAlteration = extractOnetimeDiscountAlteration((OneTimeDiscountProdPriceAlteration) current);
              node.addToAllPrices(extractedOnetimeDiscountAlteration);
              alterations.add((CuCoProdPriceAlterations) extractedOnetimeDiscountAlteration);
            } else if (current instanceof AllowanceProdPriceAlteration) {
              CuCoComponentProductPrice extractedAllowance = extractAllowance((AllowanceProdPriceAlteration) current);
              node.addToAllPrices(extractedAllowance);
              alterations.add((CuCoProdPriceAlterations) extractedAllowance);
            }
          }
        }
        // Forming a tree of charges and alterations
        for (CuCoProdPriceAlterations currentAlteration : alterations) {
          String parentPriceId = currentAlteration.getParentPriceId();
          if (charges.containsKey(parentPriceId)) {
            charges.get(parentPriceId).addToAlterations(currentAlteration);
          }
        }
      }
      ProductPrice price = getProductPriceChargeForIdxValue(product);
      if (price != null && ((ComponentProdPrice) price).isSetIdxStatus()) {
        node.setIdxStatus(IndexationStatus.getForCIValue(((ComponentProdPrice) price).getIdxStatus().intValue()));
      }
    }
    if (product instanceof ProductBundle && !isVoiceProduct(product)) {
      final ProductBundleImpl productBundle = (ProductBundleImpl) product;

      node.setVoiceProductType(isTv(productBundle) ? ProductType.TV : ProductType.UNDEFINED);

      if (product.getName() == null || product.getName().isEmpty()) {
        if (productBundle.getBundledProductOffering() != null) {
          node.setText(productBundle.getBundledProductOffering().getProductOfferingId());
        } else {
          node.setText("Unbekannt");
        }
      }

      BundledProductList bundledProductList = productBundle.getBundledProductList();
      if (bundledProductList != null) {
        boolean linkedParentNodeAlreadyFound = searchForChildrenWithMatchingCallNumber && node.getLinkedSubscriptionId() != null
            && node.getLinkedSubscriptionId().equalsIgnoreCase(rootSubscriptionNode.getLinkedSubscriptionId());
        for (BundledProduct childProduct : bundledProductList.getBundledProductArray()) {
          if (DISPLAY.TABLE != node.getIntendedUIDisplay() || shouldAddProduct(childProduct.getProduct().getName())) {
            DefaultProductNode childNode = createNode(childProduct.getProduct(), node, rootSubscriptionNode, searchForChildrenWithMatchingCallNumber && !linkedParentNodeAlreadyFound);
            childNode.setIntendedUIDisplay(node.getIntendedUIDisplay());
            childNode.setParent(node);
            node.addChild(childNode);
          }
        }
      }
      node.getMetaData().put(MetaDataHelper.createMetaData(productBundle));
      node.setProductType(DefaultProductNodeType.BUNDLE);

    } else if (product instanceof ProductComponent && !isVoiceProduct(product)) {
      final ProductComponent productComponent = (ProductComponent) product;
      node.getMetaData().put(MetaDataHelper.createMetaData(productComponent));
      node.setProductType(DefaultProductNodeType.COMPONENT);
      node.setVoiceProductType(ProductType.INET);

    } else if (product instanceof ProductComponent && isVoiceProduct(product)) {
      node.setVoiceProductType(translateProductType(product));

      node.getMetaData().put(MetaDataHelper.createVoiceMetaData((ProductComponent) product));
      node.setProductType(DefaultProductNodeType.VOICE);

    }

    if (product.getPhysicalResources() != null && product.getPhysicalResources().getPhysicalResourceArray() != null) {
      for (PhysicalResource res : product.getPhysicalResources().getPhysicalResourceArray()) {
        PhysicalResourceNode childNode = createNode(res);
        childNode.setParent(node);
        node.addChild(childNode);
      }
    }
    node.setHasOANProduct(getOANIdentifier(node.getMetaData()));

    boolean linkedToParentNode = (node.getCallNumber() != null && node.getCallNumber().equals(rootSubscriptionNode.getCallNumber()))
        || (node.getLinkedSubscriptionId() != null && node.getLinkedSubscriptionId().equalsIgnoreCase(rootSubscriptionNode.getLinkedSubscriptionId()));
    node.setMatchingCallNumberWithRootSubscription(!searchForChildrenWithMatchingCallNumber || linkedToParentNode);
    if (searchForChildrenWithMatchingCallNumber && linkedToParentNode) {
      DefaultProductNode clone = SerializationUtils.clone(node);
      clone.setParent(rootSubscriptionNode);
      clone.setEffectiveDepthForView(rootSubscriptionNode.getDepth() + 1);
      clone.setHasIndirectParent(true);
      rootSubscriptionNode.getChildrenWithMatchingCallNumbers().add(clone);
    }
    return node;
  }

  private boolean getOANIdentifier(MetaData metaData) {
    String oanIdentifiers = settingService.getValueOrDefault("productBrowser.oanProductIdentiers", "PSC_OAN_NETWORK_PROVIDER");
    if (oanIdentifiers.contains(";")) {
      for (String identifier : oanIdentifiers.split(";")) {
        if (metaData.hasMetaDataEntryWithID(identifier)) {
          return true;
        }
      }
      return false;
    }
    return metaData.hasMetaDataEntryWithName(oanIdentifiers);
  }

  private ProductPrice getProductPriceChargeForIdxValue(Product product) {
    for (ProductPrice price : product.getProductPrices().getProductPriceArray()) {
      if (price instanceof RecurringChargeProdPriceCharge) {
        return price;
      }
    }
    return product.getProductPrices().getProductPriceArray(0);
  }

  private CuCoComponentProductPrice extractAllowance(AllowanceProdPriceAlteration current) {
    CuCoProdPriceAlterations result = new CuCoProdPriceAlterations(ProdPriceAlterationType.ALLOWANCE);
    setCommonPriceFields(current, result);
    result.setParentPriceId(current.isSetAlteratesCharges() ? current.getAlteratesCharges().getProductPriceId() : null);
    result.setUnitOfMeasure(current.getUnitOfMeasure());
    result.setAllowanceValue(current.getValue());
    result.setFrequency(
        current.getFrequency() != null ? textService.getByKeyWithDefaultText("productPrice_Frequency_".concat(current.getFrequency().toLowerCase()), current.getFrequency()).getText() : "-");
    return result;
  }

  private CuCoComponentProductPrice extractOnetimeChargePrice(OneTimeChargeProdPriceCharge current) {
    CuCoProdPriceCharge result = new CuCoProdPriceCharge(ProdPriceChargeType.ONE_TIME);
    setCommonPriceFields(current, result);
    result.setFrequency(textService.getByKeyWithDefaultText("productPrice_Frequency_onetime", "einmalig").getText());
    return result;
  }

  private CuCoComponentProductPrice extractOnetimeDiscountAlteration(OneTimeDiscountProdPriceAlteration current) {
    CuCoProdPriceAlterations result = new CuCoProdPriceAlterations(ProdPriceAlterationType.ONETIME_DISCOUNT);
    setCommonPriceFields(current, result);
    result.setAlteredPriceAfterDiscount(convertToCuCoPrice(current.getAlteredPrice()));
    result.setParentPriceId(current.isSetAlteratesCharges() ? current.getAlteratesCharges().getProductPriceId() : null);
    result.setFrequency(textService.getByKeyWithDefaultText("productPrice_Frequency_onetime", "einmalig").getText());
    return result;
  }

  private CuCoComponentProductPrice extractRecurringDiscountAlteration(RecurringDiscountProdPriceAlteration current) {
    CuCoProdPriceAlterations result = new CuCoProdPriceAlterations(ProdPriceAlterationType.RECURRING_DISCOUNT);
    setCommonPriceFields(current, result);
    result.setAlteredPriceAfterDiscount(current.isSetAlteredPrice() ? convertToCuCoPrice(current.getAlteredPrice()) : null);
    result.setParentPriceId(current.isSetAlteratesCharges() ? current.getAlteratesCharges().getProductPriceId() : null);
    result.setFrequency(
        current.getFrequency() != null ? textService.getByKeyWithDefaultText("productPrice_Frequency_".concat(current.getFrequency().toLowerCase()), current.getFrequency()).getText() : "-");
    result.setDiscountStartDate(current.getDiscountStartDate() != null ? current.getDiscountStartDate().getTime() : null);
    result.setDiscountEndDate(current.isSetDiscountEndDate() ? current.getDiscountEndDate().getTime() : null);
    return result;
  }

  private CuCoComponentProductPrice extractRecurringChargePrice(RecurringChargeProdPriceCharge current) {
    CuCoProdPriceCharge result = new CuCoProdPriceCharge(ProdPriceChargeType.RECURRING);
    setCommonPriceFields(current, result);
    result
        .setFrequency(current.isSetFrequency() ? textService.getByKeyWithDefaultText("productPrice_Frequency_".concat(current.getFrequency().toLowerCase()), current.getFrequency()).getText() : null);
    return result;
  }

  private void setCommonPriceFields(ComponentProdPrice current, CuCoComponentProductPrice result) {
    result.setName(current.getName());
    result.setBasePrice(current.isSetBasePrice() ? convertToCuCoPrice(current.getBasePrice()) : null);
    result.setIdxStatus(current.isSetIdxStatus() ? IndexationStatus.getForCIValue(current.getIdxStatus().intValue()) : IndexationStatus.NOT_AVAILABLE);
    result.setIdxStartDate(current.isSetIdxStartDate() ? current.getIdxStartDate().getTime() : null);
    result.setPrice(current.isSetPrice() ? convertToCuCoPrice(current.getPrice()) : null);
    result.setProductOfferingPriceId(current.getProductOfferingPriceId());
    result.setProductPriceId(current.isSetProductPriceId() ? current.getProductPriceId() : null);
    result.setTaxRate(current.isSetTaxRate() ? current.getTaxRate() : null);
  }

  private CuCoPrice convertToCuCoPrice(Money basePrice) {
    CuCoPrice result = new CuCoPrice();
    result.setAmount(basePrice.getAmount());
    result.setUnits(basePrice.getUnits());
    return result;
  }

  private boolean isVoiceProduct(Product product) {
    return product.getCallNumber() != null;
  }

  private Date addOneDay(Date date) {
    return calcDate(date, Calendar.DAY_OF_YEAR, +1);
  }

  private Date addMonth(Date date, int duration) {
    return calcDate(date, Calendar.MONTH, +duration);
  }

  private Date calcDate(Date date, int unit, int amount) {
    if (date != null) {
      Calendar calendar = Calendar.getInstance();
      calendar.setTime(date);
      calendar.add(unit, amount);
      return calendar.getTime();
    }
    return null;
  }

  public boolean isTv(ProductBundle productBundle) {
    return productBundle.getName().contains("TV");
  }

  private void mapProductStatus(Product product) {
    if (product.getProductStatus() != null) {
      Text text = textService.getByKeyWithDefaultText(product.getProductStatus(), product.getProductStatus());
      product.setProductStatus(text.getText());
    } else {
      product.setProductStatus("Unbekannt");
    }
  }

  private void mapTarifs(Product product) {
    if (product.getProductCharacteristicValues() != null) {
      for (ProductCharacteristicValue value : product.getProductCharacteristicValues().getProductCharacteristicValueArray()) {
        if (value.getProductSpecCharacteristic().getName().equals("Tarif")) {
          Text text = textService.getByKeyWithDefaultText(value.getValue(), value.getValue());
          value.setValue(text.getText());
        }
      }
    }
  }

  private CallNumber getCallNumber(Product voiceProduct) {
    CallNumber callNumber = new CallNumber();
    callNumber.setCountryCode(voiceProduct.getCallNumber().getCC());
    callNumber.setOnkz(voiceProduct.getCallNumber().getNDC());
    callNumber.setTnum(voiceProduct.getCallNumber().getSN());
    return callNumber;
  }

  private CallNumber getCallNumber(Subscription subscription) {
    CallNumber callNumber = new CallNumber();
    callNumber.setCountryCode(subscription.getCallNumber().getCC());
    callNumber.setOnkz(subscription.getCallNumber().getNDC());
    callNumber.setTnum(subscription.getCallNumber().getSN());
    return callNumber;
  }

  private ProductType translateProductType(Product voiceProduct) {
    String ndc = voiceProduct.getCallNumber().getNDC();
    final String[] mobileType = settingService.getValuesIgnoreMissing("productBrowserMobileTypeArrayList");
    List<String> mobileTypes = Arrays.asList(mobileType);
    if (mobileTypes.contains(ndc)) {
      return ProductType.MOBILE;
    }
    return ProductType.FIXED;
  }

  @Autowired
  public void setCustomerEquipmentService(CustomerEquipmentService customerEquipmentService) {
    this.customerEquipmentService = customerEquipmentService;
  }

  @Autowired
  public void setPartyService(PartyService partyService) {
    this.partyService = partyService;
  }

  @Autowired
  public void setTextService(TextService textService) {
    this.textService = textService;
  }

  // CMSYS703
  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }

  @Override
  public void loadInventoryPricesForBAN(String ban, String partyId, Map<String, ProductPrice> socPriceMap) {
    Product[] productsForBAN = getProductsForCustomerAccount(ban, partyId);
    if (productsForBAN == null || productsForBAN.length == 0) {
      return;
    }
    for (Product product : productsForBAN) {
      if (!product.isSetProductPrices()) {
        continue;
      }
      for (ProductPrice price : product.getProductPrices().getProductPriceArray()) {
        if (socPriceMap.containsKey(price.getProductOfferingPriceId())) {
          socPriceMap.put(price.getProductOfferingPriceId(), price);
        }
      }
    }
  }

  @Override
  public ArrayList<BaseNode> getSubscriptionsDataForCustomer(ArrayList<Long> partyIds, String sessionId, boolean hasAuthorityToSeeCustomerInventoryXMLs) {
    ArrayList<BaseNode> result = new ArrayList<BaseNode>();
    for (long partyId : partyIds) {
      result.addAll(getSubscriptionsForParty(partyId, sessionId, hasAuthorityToSeeCustomerInventoryXMLs));
    }
    return result;
  }

  @SuppressWarnings("serial")
  private static class SubscriptionNodeComparator implements Comparator<SubscriptionNode>, Serializable {

    @Override
    public int compare(SubscriptionNode n1, SubscriptionNode n2) {
      return n1.getSubscriptionId().compareTo(n2.getSubscriptionId());
    }
  }

  public ArrayList<DefaultSubscriptionNode> getSubscriptionsForParty(long partyId, String sessionId, boolean hasAuthorityToSeeCustomerInventoryXMLs) {
    ArrayList<DefaultSubscriptionNode> subscriptionsList = new ArrayList<DefaultSubscriptionNode>();
    GetSubscriptionsForPartyResponseType resp = null;
    GetSubscriptionsForPartyResponseDocument respDoc;

    String mockResponseFileName = System.getProperty("catalina.base") + "//mocks//CI_getSubscriptionsForParty_CMSYS3218.xml";
    try {

      if (settingService.getBooleanValue("testModeActive", false) && new File(mockResponseFileName).exists()
          && settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false)) {
        resp = GetSubscriptionsForPartyResponseDocument.Factory.parse(FileUtils.readFileToString(new File(mockResponseFileName))).getGetSubscriptionsForPartyResponse();
        getSubscriptionForPartyResponseXml = "<response>" + "\n" + resp.toString() + "\n" + "</response>";
      } else {
        respDoc = stub.getSubscriptionsForParty(prepareRequestForGetSubsForParty(partyId, true, true, false, true,
            (settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false) ? true : false), true, 1), null);
        resp = respDoc.getGetSubscriptionsForPartyResponse();
        getSubscriptionForPartyResponseXml = "<response>" + "\n" + respDoc.toString() + "\n" + "</response>";
      }
      esbServiceEndPointUrl = esbAccessParameterDao.getURLByInstanceName(stub.getInstanceName());
      getSubscriptionForPartyRequestResponseXml = "<esbWebServiceCall>" + "\n" + "<esbEndpoint> " + esbServiceEndPointUrl + " </esbEndpoint>" + "\n" + getSubscriptionForPartyRequestXml + "\n"
          + getSubscriptionForPartyResponseXml + "\n" + "</esbWebServiceCall>";
      if (settingService.getBooleanValue("productBrowser.a1OneTvPart2Active", true) && hasAuthorityToSeeCustomerInventoryXMLs) {
        File createFolderForUploading = new File(getUploadPathForCustomerInventoryFolder());
        if (!createFolderForUploading.exists()) {
          createFolderForUploading.mkdirs();
        }

        File createFolderAsPerSession = new File(createFolderForUploading + File.separator + sessionId);
        if (!createFolderAsPerSession.exists()) {
          createFolderAsPerSession.mkdir();
        }

        FileUtils.cleanDirectory(createFolderAsPerSession);
        File defaultZipPathWithPartyId = new File(createFolderAsPerSession + File.separator
            + textService.getByKeyWithDefaultText("newProductOverviewCustomerInventoryDotAsPrefix", "CustomerInventory.").getText() + getSubscriptionForPartyRequestPartyId);
        if (defaultZipPathWithPartyId.exists()) {
          deleteDirectory(defaultZipPathWithPartyId);
        }
        defaultZipPathWithPartyId.mkdir();
      }

      if (resp != null && resp.getSubscriptions() != null && resp.getSubscriptions().sizeOfSubscriptionArray() > 0) {
        boolean topLevelProductDisplayEnabled = settingService.getBooleanValue("productBrowser.topLevelProductsEnabled", false);
        for (Subscription subs : resp.getSubscriptions().getSubscriptionArray()) {
          DefaultSubscriptionNode preparedSubscriptionNode = prepareSubscriptionNode(subs, null, null);
          preparedSubscriptionNode.setIntendedUIDisplay(DISPLAY.TABLE);
          preparedSubscriptionNode.setPartyId(partyId);
          preparedSubscriptionNode.setDepth(0);
          subscriptionsList.add(preparedSubscriptionNode);

          if (subs.isSetProducts() && subs.getProducts().sizeOfProductArray() > 0 && topLevelProductDisplayEnabled) {
            String topLevelProduct = "";
            for (Product product : subs.getProducts().getProductArray()) {
              if (!topLevelProduct.isEmpty()) {
                topLevelProduct += "; ";
              }
              topLevelProduct += product.getName();
            }
            preparedSubscriptionNode.setTopLevelProducts(topLevelProduct);
          }
        }

        while (!resp.getPagination().getIsLastPage()) {
          respDoc = stub.getSubscriptionsForParty(prepareRequestForGetSubsForParty(partyId, true, true, false, true,
              (settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false) ? true : false), true, resp.getPagination().getPageNumber() + 1), null);
          resp = respDoc.getGetSubscriptionsForPartyResponse();

          if (resp != null && resp.getSubscriptions() != null && resp.getSubscriptions().sizeOfSubscriptionArray() > 0) {
            for (Subscription subs : resp.getSubscriptions().getSubscriptionArray()) {
              DefaultSubscriptionNode preparedSubscriptionNode = prepareSubscriptionNode(subs, null, null);
              preparedSubscriptionNode.setIntendedUIDisplay(DISPLAY.TABLE);
              preparedSubscriptionNode.setPartyId(partyId);
              preparedSubscriptionNode.setDepth(0);
              subscriptionsList.add(preparedSubscriptionNode);

              if (subs.isSetProducts() && subs.getProducts().sizeOfProductArray() > 0 && topLevelProductDisplayEnabled) {
                String topLevelProduct = "";
                for (Product product : subs.getProducts().getProductArray()) {
                  if (!topLevelProduct.isEmpty()) {
                    topLevelProduct += "; ";
                  }
                  topLevelProduct += product.getName();
                }
                preparedSubscriptionNode.setTopLevelProducts(topLevelProduct);
              }
            }
          }
        }

        ArrayList<DefaultSubscriptionNode> result = subscriptionsList;
        Collections.sort(result, new SubscriptionNodeComparator());

        for (int num = 0; num < Integer.valueOf(settingService.getValueOrDefault("productBrowser.tableView.productCharacteristic.amountOfSubscriptionToPreload", "5")); num++) {
          if (num > (result.size() - 1)) {
            break;
          }
          DefaultSubscriptionNode subscriptionNode = result.get(num);
          try {
            getDefaultProductNodes(subscriptionNode, sessionId, hasAuthorityToSeeCustomerInventoryXMLs);
            subscriptionNode.setChildDetailsLoaded(true);
            if (hasAuthorityToSeeCustomerInventoryXMLs && settingService.getBooleanValue("productBrowser.a1OneTvPart2Active", true)
                && settingService.getBooleanValue("productBrowser.createZipWithInitialPreLoadLogic", false)) {
              File createFolderForUploading = new File(getUploadPathForCustomerInventoryFolder());

              File createFolderAsPerSession = new File(createFolderForUploading + File.separator + sessionId);

              File defaultZipPathWithPartyId = new File(createFolderAsPerSession + File.separator
                  + textService.getByKeyWithDefaultText("newProductOverviewCustomerInventoryDotAsPrefix", "CustomerInventory.").getText() + getSubscriptionForPartyRequestPartyId);

              getProductsForSubscriptionRequestResponseXml = "<esbWebServiceCall>" + "\n" + "<esbEndpoint> " + esbServiceEndPointUrl + " </esbEndpoint>" + "\n" + getProductsForSubscriptionRequestXml
                  + "\n" + getProductsForSubscriptionResponseXml + "\n" + "</esbWebServiceCall>";
              if (settingService.getBooleanValue("productBrowser.a1OneTvPart2Active", true) && hasAuthorityToSeeCustomerInventoryXMLs) {
                createGetProductsForSubscriptionRequestResponseFiles(defaultZipPathWithPartyId);
              }
            }
          } catch (Exception ex) {
            logger.error("Error while retrieving products for subscriptions" + (subscriptionNode.getCallNumber() != null ? subscriptionNode.getCallNumber()
                : (subscriptionNode.getBillableUser() != null && settingService.getBooleanValue("productBrowserBvkBillableUserSubscriptionAndProductsActive", false)
                    ? subscriptionNode.getBillableUser().getUserName()
                    : ""))
                + " for Party " + partyId, ex);
          }
        }
      } else {
        logger.error("No subscriptions found for Party " + partyId);
      }
      if (settingService.getBooleanValue("productBrowser.a1OneTvPart2Active", true) && hasAuthorityToSeeCustomerInventoryXMLs) {
        File createFolderForUploading = new File(getUploadPathForCustomerInventoryFolder());

        File createFolderAsPerSession = new File(createFolderForUploading + File.separator + sessionId);

        File defaultZipPathWithPartyId = new File(createFolderAsPerSession + File.separator
            + textService.getByKeyWithDefaultText("newProductOverviewCustomerInventoryDotAsPrefix", "CustomerInventory.").getText() + getSubscriptionForPartyRequestPartyId);

        createGetSubscriptionForPartyRequestResponseFile(defaultZipPathWithPartyId);
        filesToZipList.clear();
        getAllCiRequestResponseFileListToZip(defaultZipPathWithPartyId);
        createCiRequestResponseFolderZip(
            defaultZipPathWithPartyId + File.separator + textService.getByKeyWithDefaultText("newProductOverviewCustomerInventoryDotAsPrefix", "CustomerInventory.").getText()
                + getSubscriptionForPartyRequestPartyId + textService.getByKeyWithDefaultText("newProductOverviewReqRespZipSuffix", ".zip").getText(),
            defaultZipPathWithPartyId.toString());
      }
    } catch (Exception e) {
      logger.error("Error while retrieving subscriptions for Party " + partyId, e);
    }

    if (settingService.getBooleanValue("productBrowser.showMarketPlaceSubscriptions", false)) {
      appendMarketplaceSubscriptionsTotheList(partyId, subscriptionsList);
    }
    return subscriptionsList;
  }

  private void appendMarketplaceSubscriptionsTotheList(long partyId, ArrayList<DefaultSubscriptionNode> subscriptionsList) {
    LocationNode locationNode = marketplaceInventoryService.getMarketplaceAccountsWithSubscriptionsForParty(partyId);

    if (locationNode == null || locationNode.getChildren() == null || locationNode.getChildren().size() == 0) {
      return;
    }
    for (BaseNode node : locationNode.getChildren()) {
      if (!(node instanceof AccountNode) || node.getChildren() == null || node.getChildren().size() == 0) {
        continue;
      }
      for (BaseNode childSubNote : node.getChildren()) {
        if (childSubNote instanceof DefaultSubscriptionNode) {
          childSubNote.setDepth(0);
          subscriptionsList.add((DefaultSubscriptionNode) childSubNote);
        }
      }

    }

  }

  private String getUploadPathForCustomerInventoryFolder() {
    String path = localSettingService.getValue("productBrowser_CIReqRes_filePath");
    if (!path.endsWith(File.separator)) {
      path += File.separator;
    }
    return path;
  }

  private boolean deleteDirectory(File path) {
    if (path.exists()) {
      File[] files = path.listFiles();
      for (int i = 0; i < files.length; i++) {
        if (files[i].isDirectory()) {
          deleteDirectory(files[i]);
        } else {
          files[i].delete();
        }
      }
    }
    return (path.delete());
  }

  private void createGetSubscriptionForPartyRequestResponseFile(File defaultZipPathWithPartyId) {
    try {
      File getSubscriptionForPartyXmlFile = new File(defaultZipPathWithPartyId + File.separator
          + textService.getByKeyWithDefaultText("newProductOverviewGetSubscriptionForPartyReqRespXmlFilePrefix", "CustomerInventory.getSubscriptionForParty.").getText()
          + getSubscriptionForPartyRequestPartyId + textService.getByKeyWithDefaultText("newProductOverviewAllFileReqRespXmlSuffix", ".xml").getText());
      if (!getSubscriptionForPartyXmlFile.exists()) {
        getSubscriptionForPartyXmlFile.createNewFile();
      }
      FileUtils.writeStringToFile(getSubscriptionForPartyXmlFile, getSubscriptionForPartyRequestResponseXml, "UTF-8");
    } catch (IOException e) {
      logger.error(e.getMessage(), e);
    }
  }

  private void createGetProductsForSubscriptionRequestResponseFiles(File defaultZipPathWithPartyId) {
    try {
      File getPartyForSubscriptionXmlFile = new File(defaultZipPathWithPartyId + File.separator
          + textService.getByKeyWithDefaultText("newProductOverviewGetProductsForSubscriptionReqRespXmlPrefix", "CustomerInventory.getProductsForSubscription.").getText()
          + getProductsForSubscriptionRequestCallNumber + textService.getByKeyWithDefaultText("newProductOverviewAllFileReqRespXmlSuffix", ".xml").getText());
      if (!getPartyForSubscriptionXmlFile.exists()) {
        getPartyForSubscriptionXmlFile.createNewFile();
      }
      if (getProductsForSubscriptionRequestResponseXml != null) {
        FileUtils.writeStringToFile(getPartyForSubscriptionXmlFile, getProductsForSubscriptionRequestResponseXml, "UTF-8");
      }
    } catch (IOException e) {
      logger.error(e.getMessage(), e);
    }
  }

  private void getAllCiRequestResponseFileListToZip(File node) {
    if (node.isFile()) {
      filesToZipList.add(new File(node.toString()).getName());
    }

    if (node.isDirectory()) {
      String[] subNote = node.list();
      for (String filename : subNote) {
        getAllCiRequestResponseFileListToZip(new File(node, filename));
      }
    }
  }

  private void createCiRequestResponseFolderZip(String zipFile, String sourceFolder) {

    byte[] buffer = new byte[1024];
    String source = new File(sourceFolder).getName();
    FileOutputStream fos = null;
    ZipOutputStream zos = null;
    try {
      fos = new FileOutputStream(zipFile);
      zos = new ZipOutputStream(fos);
      FileInputStream in = null;

      for (String file : filesToZipList) {
        ZipEntry ze = new ZipEntry(source + File.separator + file);
        zos.putNextEntry(ze);
        try {
          in = new FileInputStream(sourceFolder + File.separator + file);
          int len;
          while ((len = in.read(buffer)) > 0) {
            zos.write(buffer, 0, len);
          }
        } finally {
          if (in != null) {
            in.close();
          }
        }
      }

      zos.closeEntry();

    } catch (IOException e) {
      logger.error(e.getMessage(), e);
    } finally {
      try {
        if (zos != null) {
          zos.close();
        }
      } catch (IOException e) {
        logger.error(e.getMessage(), e);
      }
    }
  }

  private boolean shouldAddProduct(String productName) {
    final String blacklistValuesForNewProductViewStr = textService.getByKeyWithDefaultText("admin_productBrowserTableViewBlacklist", "").getText();
    final String whitelistValuesForNewProductViewStr = textService.getByKeyWithDefaultText("admin_productBrowserTableViewWhitelist", "").getText();
    final String filterMode = settingService.getValue("productBrowser.tableView.productCharacteristic.mode");
    List<String> blacklistValuesForNewProductView = Arrays.asList((blacklistValuesForNewProductViewStr == null ? "" : blacklistValuesForNewProductViewStr).split(Separator.SEMICOLON));
    List<String> whitelistValuesForNewProductView = Arrays.asList((whitelistValuesForNewProductViewStr == null ? "" : whitelistValuesForNewProductViewStr).split(Separator.SEMICOLON));

    if (filterMode.equalsIgnoreCase("Blacklist") && !isBlacklisted(productName, blacklistValuesForNewProductView)) {
      return true;
    }
    if (filterMode.equalsIgnoreCase("Whitelist") && isWhitelisted(productName, whitelistValuesForNewProductView)) {
      return true;
    }
    return false;
  }

  private static boolean isBlacklisted(String productSpecCharacteristicId, List<String> blacklist) {
    return blacklist.contains(productSpecCharacteristicId);
  }

  private static boolean isWhitelisted(String productSpecCharacteristicId, List<String> whitelist) {
    return whitelist.contains(productSpecCharacteristicId);
  }

  @Autowired
  public void setEsbAccessParameterDao(EsbAccessParameterDao esbAccessParameterDao) {
    this.esbAccessParameterDao = esbAccessParameterDao;
  }
}
