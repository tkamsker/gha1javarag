package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class Product implements Serializable, InventoryProductGroupAssignable {
  private String productId;
  private String productDescription;
  private InventoryProductGroup inventoryProductGroup;
  private ProductLevel parent;

  public Product() {}

  public Product(String productId, String productDescription) {
    this.productId = productId;
    this.productDescription = productDescription;
  }

  public String getProductId() {
    return productId;
  }

  public void setProductId(String productId) {
    this.productId = productId;
  }

  public String getProductDescription() {
    return productDescription;
  }

  public void setProductDescription(String productDescription) {
    this.productDescription = productDescription;
  }

  @Override
  public String getDescription() {
    return getProductDescription();
  }

  @Override
  public InventoryProductGroup getInventoryProductGroup() {
    return inventoryProductGroup;
  }

  @Override
  public void setInventoryProductGroup(InventoryProductGroup inventoryProductGroup) {
    this.inventoryProductGroup = inventoryProductGroup;
  }

  @Override
  public ProductLevel getParent() {
    return parent;
  }

  public void setParent(ProductLevel parent) {
    this.parent = parent;
  }

  @Override
  public boolean equals(Object o) {
    if (!(o instanceof Product)) {
      return false;
    }
    Product product = (Product) o;
    return productId.equals(product.getProductId());
  }

  @Override
  public int hashCode() {
    return productId.hashCode();
  }

}
