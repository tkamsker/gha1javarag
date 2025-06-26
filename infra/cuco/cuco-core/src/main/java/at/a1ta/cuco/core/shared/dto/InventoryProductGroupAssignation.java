package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class InventoryProductGroupAssignation implements Serializable {
  private long inventoryProductGroupId;
  private long levelId;
  private String productId;

  public long getInventoryProductGroupId() {
    return inventoryProductGroupId;
  }

  public void setInventoryProductGroupId(long inventoryProductGroupId) {
    this.inventoryProductGroupId = inventoryProductGroupId;
  }

  public long getLevelId() {
    return levelId;
  }

  public void setLevelId(long levelId) {
    this.levelId = levelId;
  }

  public String getProductId() {
    return productId;
  }

  public void setProductId(String productId) {
    this.productId = productId;
  }
}
