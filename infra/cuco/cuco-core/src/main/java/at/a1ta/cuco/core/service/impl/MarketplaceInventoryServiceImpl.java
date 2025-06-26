package at.a1ta.cuco.core.service.impl;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.server.service.TextService;
import at.a1ta.bite.core.shared.util.CommonUtils;
import at.a1ta.cuco.core.service.MarketplaceInventoryService;
import at.a1ta.cuco.core.shared.dto.product.AccountNode;
import at.a1ta.cuco.core.shared.dto.product.DefaultProductNode;
import at.a1ta.cuco.core.shared.dto.product.DefaultSubscriptionNode;
import at.a1ta.cuco.core.shared.dto.product.DefaultSubscriptionType;
import at.a1ta.cuco.core.shared.dto.product.Location;
import at.a1ta.cuco.core.shared.dto.product.Location.LocationType;
import at.a1ta.cuco.core.shared.dto.product.LocationNode;
import at.a1ta.cuco.core.shared.dto.product.MetaData;
import at.a1ta.cuco.core.shared.dto.product.MetaDataEntry;
import at.a1ta.cuco.core.shared.dto.product.MetaDataEntryType;
import at.a1telekom.eai.marketplaceinventory.GetMarketplaceSubscriptionsForPartyRequestDocument;
import at.a1telekom.eai.marketplaceinventory.GetMarketplaceSubscriptionsForPartyResType.Account;
import at.a1telekom.eai.marketplaceinventory.GetMarketplaceSubscriptionsForPartyResType.Account.Subscription;
import at.a1telekom.eai.marketplaceinventory.GetMarketplaceSubscriptionsForPartyResponseDocument;
import at.a1telekom.eai.marketplaceinventory.RequestType;

import com.telekomaustriagroup.esb.marketplaceinventory.MarketplaceInventoryStub;

@Service
public class MarketplaceInventoryServiceImpl extends BaseEsbClient<MarketplaceInventoryStub> implements MarketplaceInventoryService {

  private static final Logger LOGGER = LoggerFactory.getLogger(MarketplaceInventoryServiceImpl.class);
  @Autowired
  private SettingService settingService;

  @Autowired
  private TextService textService;

  private static SimpleDateFormat dateFormat = new SimpleDateFormat("dd.MM.yyyy");

  private static final HashMap<String, String> DATE_FORMAT_REGEXPS = new HashMap<String, String>() {
    {
      put("^\\d{4}-\\d{1,2}-\\d{1,2}$", "yyyy-MM-dd");
    }
  };

  @Override
  public LocationNode getMarketplaceAccountsWithSubscriptionsForParty(long partyId) {
    LocationNode locationNode = new LocationNode();
    if (!settingService.getBooleanValue("productBrowser.showMarketPlaceSubscriptions", false)) {
      return locationNode;
    }

    try {
      GetMarketplaceSubscriptionsForPartyRequestDocument reqDoc = GetMarketplaceSubscriptionsForPartyRequestDocument.Factory.newInstance();
      RequestType addNewGetMarketplaceSubscriptionsForPartyRequest = reqDoc.addNewGetMarketplaceSubscriptionsForPartyRequest();
      addNewGetMarketplaceSubscriptionsForPartyRequest.setPartyId(partyId + "");
      reqDoc.setGetMarketplaceSubscriptionsForPartyRequest(addNewGetMarketplaceSubscriptionsForPartyRequest);

      GetMarketplaceSubscriptionsForPartyResponseDocument response = stub.getMarketplaceSubscriptionsForParty(reqDoc, null);
      final String statusLabel = textService.getByKeyWithDefaultText("productbrowser.marketplace.statusLabel", "Status:").getText();
      final String serviceStatusLabel = textService.getByKeyWithDefaultText("productbrowser.marketplace.serviceStatusLabel", "Service Status:").getText();
      final String periodLabel = textService.getByKeyWithDefaultText("productbrowser.marketplace.periodLabel", "Periode:").getText();
      if (response != null && response.getGetMarketplaceSubscriptionsForPartyResponse() != null && response.getGetMarketplaceSubscriptionsForPartyResponse().getAccountArray() != null
          && response.getGetMarketplaceSubscriptionsForPartyResponse().getAccountArray().length > 0) {

        Location location = new Location();
        location.setAddress("Keine Adresse");
        location.setLocationId("unknown");
        location.setPartyId(partyId);
        location.setLocationType(LocationType.HYBRID);
        locationNode = new LocationNode();
        locationNode.setId("unknown");
        locationNode.setLocation(location);
        locationNode.getLocation().setLocationId("MarketplaceLocation");
        locationNode.getLocation().setPartyId(partyId);
        locationNode.setDepth(0);
        locationNode.setDisplayA1CoachLink(false);
        locationNode.setFeasibilityCheckAvailable(false);
        for (Account account : response.getGetMarketplaceSubscriptionsForPartyResponse().getAccountArray()) {
          AccountNode accountNode = AccountNode.builder().accountNumber(account.getID()).parent(locationNode).build();
          accountNode.setPartyId(partyId);
          accountNode.setId(account.getID());
          accountNode.setParent(locationNode);
          accountNode.setCustomerName(account.getCustomerName());
          accountNode.setDepth(1);
          accountNode.setDisplayA1CoachLink(false);
          accountNode.setFeasibilityCheckAvailable(false);
          locationNode.addChild(accountNode);
          DefaultSubscriptionNode subNode = new DefaultSubscriptionNode();
          subNode.setAccountNumber(account.getID());
          subNode.setDepth(2);
          subNode.setSubscriptionId(account.getID());
          subNode.setId(account.getID());
          subNode.setType(DefaultSubscriptionType.Marketplace);
          subNode.setTypeText(DefaultSubscriptionType.Marketplace.name());
          subNode.setTopLevelProducts(textService.getByKeyWithDefaultText("productbrowser.marketplace.topLevelProductLabel", "A1 Marketplace").getText());
          subNode.setDisplayA1CoachLink(false);
          subNode.setEffectiveDepthForView(0);
          subNode.setPartyId(partyId);
          subNode.setFeasibilityCheckAvailable(false);
          subNode.setParent(accountNode);
          subNode.setExpanded(false);
          subNode.setChildDetailsLoaded(true);
          accountNode.addChild(subNode);
          for (Subscription sub : account.getSubscriptionArray()) {
            DefaultProductNode prodNode = new DefaultProductNode();
            prodNode.setId(sub.getID());
            prodNode.setDepth(3);
            prodNode.setEffectiveDepthForView(1);
            prodNode.setPartyId(partyId);
            prodNode.setProductName(sub.getName());
            prodNode.setValidForStart(getDateInCuCoFormat(sub.getStartDate()));
            prodNode.setCommitmentStartDate(getDateInCuCoFormat(sub.getStartDate()));
            prodNode.setValidForEnd(getDateInCuCoFormat(sub.getExpirationDate()));
            prodNode.setCommitmentEndDate(getDateInCuCoFormat(sub.getExpirationDate()));
            prodNode.setProductStatus(sub.getStatus());
            prodNode.setAutoVVLDuration("");
            prodNode.setAutoVVLEndDate("");
            prodNode.setAutoVVLStartDate("");
            prodNode.setText(sub.getName());
            prodNode.setMatchingCallNumberWithRootSubscription(true);
            MetaData metaData = new MetaData();
            ArrayList<MetaDataEntry> entries = new ArrayList<MetaDataEntry>();
            entries.add(new MetaDataEntry(periodLabel, periodLabel, sub.getPeriod(), MetaDataEntryType.STRING));
            entries.add(new MetaDataEntry(statusLabel, statusLabel, sub.getStatus(), MetaDataEntryType.STRING));
            entries.add(new MetaDataEntry(serviceStatusLabel, serviceStatusLabel, sub.getServiceStatus(), MetaDataEntryType.STRING));
            metaData.put(entries);
            prodNode.setMetaData(metaData);
            prodNode.setProductCharacteristicValuesAsMetaData(new MetaData());
            prodNode.getProductCharacteristicValuesAsMetaData().put(entries);
            String productCharacteristicValues = "";
            for (MetaDataEntry entry : prodNode.getProductCharacteristicValuesAsMetaData().getAll()) {
              productCharacteristicValues += "<pre-wrap style='font-family: Verdana;'>" + entry.getName() + " " + entry.getValue() + "</pre-wrap>" + "<br/>";
            }
            prodNode.setProductCharacteristicValuesAsString(productCharacteristicValues);
            accountNode.setDisplayA1CoachLink(false);
            accountNode.setFeasibilityCheckAvailable(false);
            prodNode.setParent(subNode);
            subNode.addChild(prodNode);
          }
        }

      }
    } catch (Exception ex) {
      LOGGER.error("Error while retrieving Marketplace subscriptions for party " + partyId, ex);
    }
    return locationNode;
  }

  private String getDateInCuCoFormat(String inputDate) {
    if (CommonUtils.cleanString(inputDate) == null) {
      return inputDate;
    }
    try {
      SimpleDateFormat orig = new SimpleDateFormat(determineDateFormat(inputDate));
      Date date = orig.parse(inputDate);
      return dateFormat.format(date);
    } catch (Exception e) {
      return inputDate;
    }

  }

  private String determineDateFormat(String dateString) {
    for (String regexp : DATE_FORMAT_REGEXPS.keySet()) {
      if (dateString.toLowerCase().matches(regexp)) {
        return DATE_FORMAT_REGEXPS.get(regexp);
      }
    }
    return "yyyy-mm-dd";
  }
}
