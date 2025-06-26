package at.a1ta.cuco.core.shared.dto.nbo;

import java.io.Serializable;

public class VBMProductDetails implements Serializable {
  private String productId;
  private String productName;
  private Long maxScoring;
  private String clarifyProductId;
  private String partWebProductId;
  private String description;

  public static final VBMProductDetails ALL_PROD = new VBMProductDetails("Alle", "Alle");
  public static final VBMProductDetails NO_PROD_FILTER = new VBMProductDetails("Kein Filter", "Kein Filter");

  public VBMProductDetails(String productId, String productName) {
    super();
    this.productId = productId;
    this.productName = productName;
  }

  public VBMProductDetails() {
    super();
  }

  private String productDetailsURL;

  public String getProductName() {
    return productName;
  }

  public void setProductName(String productName) {
    this.productName = productName;
  }

  public String getClarifyProductId() {
    return clarifyProductId;
  }

  public void setClarifyProductId(String clarifyProductId) {
    this.clarifyProductId = clarifyProductId;
  }

  public String getPartWebProductId() {
    return partWebProductId;
  }

  public void setPartWebProductId(String partWebProductId) {
    this.partWebProductId = partWebProductId;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public String getProductDetailsURL() {
    return productDetailsURL;
  }

  public void setProductDetailsURL(String productDetailsURL) {
    this.productDetailsURL = productDetailsURL;
  }

  public boolean isAvailable() {
    // for later implementation
    return true;
  }

  public String getProductId() {
    return productId;
  }

  public void setProductId(String productId) {
    this.productId = productId;
  }

  public Long getMaxScoring() {
    return maxScoring;
  }

  public void setMaxScoring(Long maxScoring) {
    this.maxScoring = maxScoring;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((productId == null) ? 0 : productId.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) return true;
    if (obj == null) return false;
    if (getClass() != obj.getClass()) return false;
    VBMProductDetails other = (VBMProductDetails) obj;
    if (productId == null) {
      if (other.productId != null) return false;
    } else if (!productId.equals(other.productId)) return false;
    return true;
  }

}
