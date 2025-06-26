package at.a1ta.cuco.core.shared.dto.product;

import java.util.ArrayList;

import at.a1ta.bite.core.shared.util.SharedStringUtils;

public class SubscriptionNode extends BaseNode implements AccountAware {

  private String accountNumber;

  private String vertragNoForDisplay;

  private String subscriptionId;

  private String topLevelProducts;

  private ArrayList<BaseNode> childrenWithMatchinCallNumbers = new ArrayList<BaseNode>();

  public SubscriptionNode(String accountNumber, String subscriptionId) {
    super();
    setId(subscriptionId);
    this.accountNumber = accountNumber;
    this.subscriptionId = subscriptionId;
  }

  public SubscriptionNode() {
    super();
  }

  @Override
  public String getAccountNumber() {
    return this.accountNumber;
  }

  public void setAccountNumber(String ban) {
    this.accountNumber = ban;
  }

  public boolean hasBan() {
    return !SharedStringUtils.isBlank(this.accountNumber);
  }

  public String getSubscriptionId() {
    return subscriptionId;
  }

  public void setSubscriptionId(String subscriptionId) {
    this.subscriptionId = subscriptionId;
    setId(subscriptionId);
  }

  public String getVertragNoForDisplay() {
    return vertragNoForDisplay;
  }

  public void setVertragNoForDisplay(String vertragNoForDisplay) {
    this.vertragNoForDisplay = vertragNoForDisplay;
  }

  public ArrayList<BaseNode> getChildrenWithMatchingCallNumbers() {
    return childrenWithMatchinCallNumbers;
  }

  public void setChildrenWithMatchinCallNumbers(ArrayList<BaseNode> childrenWithMatchinCallNumbers) {
    this.childrenWithMatchinCallNumbers = childrenWithMatchinCallNumbers;
  }

  public String getTopLevelProducts() {
    return topLevelProducts;
  }

  public void setTopLevelProducts(String topLevelProducts) {
    this.topLevelProducts = topLevelProducts;
  }

}
