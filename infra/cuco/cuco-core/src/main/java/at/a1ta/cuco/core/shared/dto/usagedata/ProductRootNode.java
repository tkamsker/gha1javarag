package at.a1ta.cuco.core.shared.dto.usagedata;

import java.io.Serializable;

public class ProductRootNode implements Serializable {
  private ProductNode rootProduct;

  public ProductNode getRootProduct() {
    return rootProduct;
  }

  public void setRootProduct(ProductNode rootProduct) {
    this.rootProduct = rootProduct;
  }
}
