package at.a1ta.cuco.core.shared.dto;

public interface InventoryProductGroupAssignable {
  public String getDescription();

  public InventoryProductGroup getInventoryProductGroup();

  public void setInventoryProductGroup(InventoryProductGroup inventoryProductGroup);

  public ProductLevel getParent();
}
