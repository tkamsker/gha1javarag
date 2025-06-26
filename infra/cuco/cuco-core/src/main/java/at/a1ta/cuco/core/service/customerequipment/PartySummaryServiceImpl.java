package at.a1ta.cuco.core.service.customerequipment;

import java.util.ArrayList;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.server.service.TextService;
import at.a1ta.cuco.core.dao.db.CmDBICTServiceDao;
import at.a1ta.cuco.core.shared.dto.product.GetPartySummaryResponse;
import at.a1ta.cuco.core.shared.dto.product.PartySummaryItem;
import at.a1telekom.eai.customerinventory.GetPartySummaryRequest;
import at.a1telekom.eai.customerinventory.GetPartySummaryRequest.LoadOptions;
import at.a1telekom.eai.customerinventory.GetPartySummaryRequestDocument;
import at.a1telekom.eai.customerinventory.GetPartySummaryResponse.SubscriptionTypes;
import at.a1telekom.eai.customerinventory.GetPartySummaryResponse.SubscriptionTypes.SubscriptionType;
import at.a1telekom.eai.customerinventory.GetPartySummaryResponse.TopLevelProducts;
import at.a1telekom.eai.customerinventory.GetPartySummaryResponse.TopLevelProducts.Product;
import at.a1telekom.eai.customerinventory.GetPartySummaryResponseDocument;

import com.codahale.metrics.annotation.Metered;
import com.telekomaustriagroup.esb.customerinventory.CustomerInventoryStub;

@Service
public class PartySummaryServiceImpl extends BaseEsbClient<CustomerInventoryStub> implements PartySummaryService {

  private static final String UI_TEXT = "_UI_Text";
  private static final String PRODUCT_OVERVIEW_SUB_TYPE = "ProductOverview_SubType_";
  private static final Logger logger = LoggerFactory.getLogger(PartySummaryServiceImpl.class);
  @Autowired
  private SettingService settingService;
  @Autowired
  private TextService textService;
  @Autowired
  private CmDBICTServiceDao cmDBICTServiceDao;

  @Override
  @Metered(name = "PartySummaryService.getPartySummary", absolute = true)
  public GetPartySummaryResponse getPartySummary(Long partyId) {
    GetPartySummaryRequestDocument requestDoc = GetPartySummaryRequestDocument.Factory.newInstance();
    GetPartySummaryRequest req = requestDoc.addNewGetPartySummaryRequest();
    LoadOptions loadOptions = req.addNewLoadOptions();
    loadOptions.setGetProductSummary(true);
    loadOptions.setGetSubscriptionTypeSummary(true);
    loadOptions.setCountChildSubscriptions(true);
    loadOptions.setGroupProductSummaryByBillingAccount(true);
    req.setPartyId(partyId + "");
    requestDoc.setGetPartySummaryRequest(req);
    GetPartySummaryResponseDocument partySummary;
    GetPartySummaryResponse cucoResponse = new GetPartySummaryResponse();
    try {
      if (settingService.getBooleanValue("testModeActiveForDec", false)) {
        cucoResponse.getSubscriptionSummaryItems().add(new PartySummaryItem("Festnetz", 4));
        cucoResponse.getSubscriptionSummaryItems().add(new PartySummaryItem("Mobil", 1));
        cucoResponse.getSubscriptionSummaryItems().add(new PartySummaryItem("Verrechnungskonten", 2));
        cucoResponse.getProductSummaryItems().add(new PartySummaryItem("A1 Enterprise Mobile", 6));
        cucoResponse.getProductSummaryItems().add(new PartySummaryItem("Festnetz Internet Business", 4));
        cucoResponse.getProductSummaryItems().add(new PartySummaryItem("A1 Breitband Pro Business", 2));
        cucoResponse.getProductSummaryItems().add(new PartySummaryItem("A1 Data Corporate", 3));
        cucoResponse.getProductSummaryItems().add(new PartySummaryItem("A1 Breitband Pro Business symmetrisch", 1));

      } else {
        partySummary = stub.getPartySummary(requestDoc, null);
        extractProducts(cucoResponse, partySummary.getGetPartySummaryResponse().getTopLevelProducts());
        extractSubscriptions(cucoResponse, partySummary.getGetPartySummaryResponse().getSubscriptionTypes());
      }
    } catch (Exception ex) {
      cucoResponse.setErrorResponse(true);
      cucoResponse.setErrorText(ex.getMessage() + "\n" + ex.getCause());
      logger.error("Error while calling CI.getPartySummary for Party Id " + partyId, ex);
    }

    return cucoResponse;
  }

  private void extractSubscriptions(GetPartySummaryResponse cucoResponse, SubscriptionTypes subscriptionTypes) {
    for (SubscriptionType sub : subscriptionTypes.getSubscriptionTypeArray()) {
      String key = textService.getByKeyWithDefaultText(PRODUCT_OVERVIEW_SUB_TYPE + sub.getType() + UI_TEXT, sub.getType()).getText();
      if (key != null && cucoResponse.containsSubscriptionSummaryItem(key)) {
        cucoResponse.getSubscriptionSummaryItemByKey(key).setCount(cucoResponse.getSubscriptionSummaryItemByKey(key).getCount() + sub.getCount());
      } else {
        cucoResponse.getSubscriptionSummaryItems().add(new PartySummaryItem(key, sub.getCount()));
      }
    }
  }

  private void extractProducts(GetPartySummaryResponse cucoResponse, TopLevelProducts topLevelProducts) {
    for (Product prod : topLevelProducts.getProductArray()) {
      cucoResponse.getProductSummaryItems().add(new PartySummaryItem(prod.getName(), prod.getCount()));
    }
  }

  @Override
  @Metered(name = "PartySummaryService.getICTServicesForPartyId", absolute = true)
  public ArrayList<PartySummaryItem> getICTServicesForPartyId(Long partyId) {

    ArrayList<PartySummaryItem> result = null;
    try {
      result = (ArrayList<PartySummaryItem>) cmDBICTServiceDao.getICTServicesForPartyId(partyId);
    } catch (Exception ex) {
      logger.error("Error while calling cmdb.getICTServicesForPartyId " + partyId, ex);
    }
    return result;
  }

}
