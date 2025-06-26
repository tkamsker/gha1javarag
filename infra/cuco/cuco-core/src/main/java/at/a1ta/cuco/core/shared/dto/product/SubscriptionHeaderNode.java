package at.a1ta.cuco.core.shared.dto.product;

public class SubscriptionHeaderNode extends SubscriptionNode {
  private static final long serialVersionUID = 1L;
  private String subscriptionIdHeader;
  private String custAccountNoHeader;
  private String callNumberHeader;
  private String addressLine1Header;
  private String addressLine2Header;
  private String addressLine3Header;
  private String typeHeader;

  public String getSubscriptionIdHeader() {
    return subscriptionIdHeader;
  }

  public void setSubscriptionIdHeader(String subscriptionIdHeader) {
    this.subscriptionIdHeader = subscriptionIdHeader;
  }

  public String getCustAccountNoHeader() {
    return custAccountNoHeader;
  }

  public void setCustAccountNoHeader(String custAccountNoHeader) {
    this.custAccountNoHeader = custAccountNoHeader;
  }

  public String getCallNumberHeader() {
    return callNumberHeader;
  }

  public void setCallNumberHeader(String callNumberHeader) {
    this.callNumberHeader = callNumberHeader;
  }

  public String getAddressLine1Header() {
    return addressLine1Header;
  }

  public void setAddressLine1Header(String addressLine1Header) {
    this.addressLine1Header = addressLine1Header;
  }

  public String getAddressLine2Header() {
    return addressLine2Header;
  }

  public void setAddressLine2Header(String addressLine2Header) {
    this.addressLine2Header = addressLine2Header;
  }

  public String getAddressLine3Header() {
    return addressLine3Header;
  }

  public void setAddressLine3Header(String addressLine3Header) {
    this.addressLine3Header = addressLine3Header;
  }

  public String getTypeHeader() {
    return typeHeader;
  }

  public void setTypeHeader(String typeHeader) {
    this.typeHeader = typeHeader;
  }
}
