package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.util.ArrayList;

public class GetPartySummaryResponse implements Serializable {
  private static final long serialVersionUID = 1L;
  private boolean errorResponse;
  private String errorText;
  private ArrayList<PartySummaryItem> productSummaryItems = new ArrayList<PartySummaryItem>();
  private ArrayList<PartySummaryItem> subscriptionSummaryItems = new ArrayList<PartySummaryItem>();

  public ArrayList<PartySummaryItem> getProductSummaryItems() {
    return productSummaryItems;
  }

  public void setProductSummaryItems(ArrayList<PartySummaryItem> productSummaryItems) {
    this.productSummaryItems = productSummaryItems;
  }

  public ArrayList<PartySummaryItem> getSubscriptionSummaryItems() {
    return subscriptionSummaryItems;
  }

  public void setSubscriptionSummaryItems(ArrayList<PartySummaryItem> subscriptionSummaryItems) {
    this.subscriptionSummaryItems = subscriptionSummaryItems;
  }

  public boolean isErrorResponse() {
    return errorResponse;
  }

  public void setErrorResponse(boolean errorResponse) {
    this.errorResponse = errorResponse;
  }

  public String getErrorText() {
    return errorText;
  }

  public void setErrorText(String errorText) {
    this.errorText = errorText;
  }

  public boolean containsSubscriptionSummaryItem(String key) {
    if (getSubscriptionSummaryItems() != null && key != null) {
      for (PartySummaryItem itm : getSubscriptionSummaryItems()) {
        if (key.equalsIgnoreCase(itm.getName())) {
          return true;
        }
      }
    }
    return false;
  }

  public PartySummaryItem getSubscriptionSummaryItemByKey(String key) {
    if (getSubscriptionSummaryItems() != null && key != null) {
      for (PartySummaryItem itm : getSubscriptionSummaryItems()) {
        if (key.equalsIgnoreCase(itm.getName())) {
          return itm;
        }
      }
    }
    return null;

  }

}
