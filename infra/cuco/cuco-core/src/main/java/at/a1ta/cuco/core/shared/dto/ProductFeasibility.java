package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class ProductFeasibility implements Serializable {
  private String productId;
  private String displayName;
  private ProductFeasibilityStatus status;

  public ProductFeasibility() {}

  public ProductFeasibility(String productId, String displayName, ProductFeasibilityStatus status) {
    this.productId = productId;
    this.displayName = displayName;
    this.status = status;
  }

  public String getProductId() {
    return productId;
  }

  public void setProductId(String productId) {
    this.productId = productId;
  }

  public String getDisplayName() {
    return displayName;
  }

  public void setDisplayName(String displayName) {
    this.displayName = displayName;
  }

  public ProductFeasibilityStatus getStatus() {
    return status;
  }

  public void setStatus(ProductFeasibilityStatus status) {
    this.status = status;
  }

  @Override
  public String toString() {
    return getClass() + ": productId=" + productId + "; displayName=" + displayName + "; status=" + status;
  }
}
