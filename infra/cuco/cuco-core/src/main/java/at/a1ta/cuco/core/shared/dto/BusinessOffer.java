package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class BusinessOffer implements Serializable {
  private Long customerId;
  private String productDescription;

  public Long getCustomerId() {
    return customerId;
  }

  public void setCustomerId(Long customerId) {
    this.customerId = customerId;
  }

  public String getProductDescription() {
    return productDescription;
  }

  public void setProductDescription(String productDescription) {
    this.productDescription = productDescription;
  }
}