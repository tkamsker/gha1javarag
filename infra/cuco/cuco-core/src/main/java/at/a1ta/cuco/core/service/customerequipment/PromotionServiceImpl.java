package at.a1ta.cuco.core.service.customerequipment;

import java.util.ArrayList;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.telekomaustriagroup.esb.odsrawdatainventory.ODSRawDataInventoryStub;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.cuco.core.service.PromotionService;
import at.a1ta.cuco.core.shared.dto.product.CallNumber;
import at.a1ta.cuco.core.shared.dto.product.Promotion;
import at.a1telekom.eai.odsrawdatainventory.AdxDiscount;
import at.a1telekom.eai.odsrawdatainventory.AdxService;
import at.a1telekom.eai.odsrawdatainventory.AdxSubscriber;
import at.a1telekom.eai.odsrawdatainventory.AdxSubscriber.Services;
import at.a1telekom.eai.odsrawdatainventory.GetAdxSubscriberRequest;
import at.a1telekom.eai.odsrawdatainventory.GetAdxSubscriberRequest.LoadOptions;
import at.a1telekom.eai.odsrawdatainventory.GetAdxSubscriberRequestDocument;
import at.a1telekom.eai.odsrawdatainventory.GetAdxSubscriberResponseDocument;

@Service
public class PromotionServiceImpl extends BaseEsbClient<ODSRawDataInventoryStub> implements PromotionService {

  private static final Logger LOGGER = LoggerFactory.getLogger(PromotionServiceImpl.class);

  private static final boolean SHOULD_GET_SERVICES = true;
  private static final boolean SHOULD_GET_FEATURES = false;

  @Override
  public ArrayList<Promotion> getSubscriptions(final CallNumber callNumber) {
    final GetAdxSubscriberRequestDocument request = GetAdxSubscriberRequestDocument.Factory.newInstance();
    final GetAdxSubscriberRequest subscriberRequest = request.addNewGetAdxSubscriberRequest();
    final LoadOptions loadOptions = subscriberRequest.addNewLoadOptions();
    loadOptions.setGetServices(SHOULD_GET_SERVICES);
    loadOptions.setGetFeatures(SHOULD_GET_FEATURES);
    final at.a1telekom.cdm.common.CallNumber cn = subscriberRequest.addNewCallNumber();
    cn.setCC(callNumber.getCountryCode());
    cn.setNDC(callNumber.getOnkz());
    cn.setSN(callNumber.getTnum());

    ArrayList<Promotion> promotions = new ArrayList<Promotion>();
    final GetAdxSubscriberResponseDocument response;
    try {
      response = this.stub.getAdxSubscriber(request, null);
      final AdxSubscriber subscriber = response.getGetAdxSubscriberResponse().getSubscriber();
      final Services services = subscriber.getServices();
      if (services != null) {
        for (int i = 0; i < services.sizeOfServiceArray(); i++) {
          final AdxService service = services.getServiceArray(i);
          Promotion promotion = new Promotion();
          promotion.setSoc(service.getSOC());

          if (service.getDiscounts() == null || service.getDiscounts().getDiscountArray() == null) {
            continue;
          }
          for (AdxDiscount discount : service.getDiscounts().getDiscountArray()) {
            promotion.setReasonCode(discount.getReasonCode());
            promotion.setReasonDescription(discount.getReasonDescription());
            promotion.setEffectiveDate(discount.getEffectiveDate() != null ? discount.getEffectiveDate().getTime() : null);
            promotion.setExpirationDate(discount.getExpirationDate() != null ? discount.getExpirationDate().getTime() : null);
            promotion.setDiscountPercent(discount.getDiscountPercent() != null ? discount.getDiscountPercent().doubleValue() : null);
            promotions.add(promotion);
          }
        }
      }
    } catch (Exception ex) {
      LOGGER.error("Error while calling getAdxSubscriber", ex);
    }
    return promotions;
  }
}
