package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class SAPSubscriptionNode extends SubscriptionNode implements Serializable {
  public SAPSubscriptionNode() {
    super();
  }

  private String consigneeId;
  private String consigneeName;

  public String getConsigneeId() {
    return consigneeId;
  }

  public void setConsigneeId(String consigneeId) {
    this.consigneeId = consigneeId;
  }

  public String getConsigneeName() {
    return consigneeName;
  }

  public void setConsigneeName(String consigneeName) {
    this.consigneeName = consigneeName;
  }

  @Override
  public String getText() {
    return (consigneeName != null ? consigneeName : "") + " - " + consigneeId;
  }
}
