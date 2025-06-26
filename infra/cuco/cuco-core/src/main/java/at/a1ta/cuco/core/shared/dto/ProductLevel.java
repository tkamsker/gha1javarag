package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class ProductLevel implements Serializable, InventoryProductGroupAssignable {
  private Long productLevelId;
  private String productLevelDescription;
  private List<ProductLevel> subProductLevels;
  private List<Product> products;
  private InventoryProductGroup inventoryProductGroup;
  private ProductLevel parent;

  public ProductLevel() {}

  public ProductLevel(Long productLevelId, String productLevelDescription) {
    this.productLevelId = productLevelId;
    this.productLevelDescription = productLevelDescription;
  }

  public Long getProductLevelId() {
    return productLevelId;
  }

  public void setProductLevelId(Long productLevelId) {
    this.productLevelId = productLevelId;
  }

  public String getProductLevelDescription() {
    return productLevelDescription;
  }

  public void setProductLevelDescription(String productLevelDescription) {
    this.productLevelDescription = productLevelDescription;
  }

  public List<ProductLevel> getSubProductLevels() {
    return subProductLevels;
  }

  public void setSubProductLevels(List<ProductLevel> subProductLevels) {
    this.subProductLevels = subProductLevels;
  }

  public void addSubProductLevel(ProductLevel subProductLevel) {
    if (subProductLevels == null) {
      subProductLevels = new ArrayList<ProductLevel>();
    }
    subProductLevels.add(subProductLevel);
  }

  public List<Product> getProducts() {
    return products;
  }

  public void setProducts(List<Product> products) {
    this.products = products;
  }

  public void addProduct(Product product) {
    if (products == null) {
      products = new ArrayList<Product>();
    }
    products.add(product);
  }

  @Override
  public String getDescription() {
    return getProductLevelDescription();
  }

  @Override
  public boolean equals(Object o) {
    if (!(o instanceof ProductLevel)) {
      return false;
    }
    ProductLevel productLevel = (ProductLevel) o;
    return productLevelId.equals(productLevel.getProductLevelId());
  }

  @Override
  public ProductLevel getParent() {
    return parent;
  }

  public void setParent(ProductLevel parent) {
    this.parent = parent;
  }

  @Override
  public int hashCode() {
    return productLevelId.hashCode();
  }

  @Override
  public InventoryProductGroup getInventoryProductGroup() {
    return inventoryProductGroup;
  }

  @Override
  public void setInventoryProductGroup(InventoryProductGroup inventoryProductGroup) {
    this.inventoryProductGroup = inventoryProductGroup;
  }
}
