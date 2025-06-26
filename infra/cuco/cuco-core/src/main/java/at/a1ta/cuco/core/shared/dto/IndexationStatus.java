package at.a1ta.cuco.core.shared.dto;

public enum IndexationStatus {
  INDEXED(2, "INDEXED_PRODUCTS"), NOT_INDEXED(3, "EXCLUDED"), INDEXED_NOT_STARTED(1, "INDEXED_PRODUCTS_NOT_USED"), NOT_AVAILABLE(0, "");
  private int relatedValueInCustomerInventory;
  private String relatedDwhValue;

  private IndexationStatus(int relatedValueInCustomerInventory, String relatedDwhValue) {
    this.relatedValueInCustomerInventory = relatedValueInCustomerInventory;
    this.relatedDwhValue = relatedDwhValue;
  }

  public static IndexationStatus getForDWHValue(String relatedDwhValue) {
    if (relatedDwhValue == null || relatedDwhValue.trim().isEmpty()) {
      return NOT_AVAILABLE;
    } else if (relatedDwhValue.trim().equalsIgnoreCase("INDEXED_PRODUCTS")) {
      return INDEXED;
    } else if (relatedDwhValue.trim().equalsIgnoreCase("EXCLUDED")) {
      return NOT_INDEXED;
    } else if (relatedDwhValue.trim().equalsIgnoreCase("INDEXED_PRODUCTS_NOT_USED")) {
      return INDEXED_NOT_STARTED;
    }
    return NOT_AVAILABLE;
  }

  public static IndexationStatus getForCIValue(int relatedValueInCustomerInventory) {
    switch (relatedValueInCustomerInventory) {
      case 1:
        return INDEXED_NOT_STARTED;
      case 2:
        return INDEXED;
      case 3:
        return NOT_INDEXED;
      default:
        // incase of 0 also it will return NOT_AVAILABLE
        return NOT_AVAILABLE;
    }

  }

  public String getRelatedDwhValue() {
    return relatedDwhValue;
  }

  public int getRelatedValueInCustomerInventory() {
    return relatedValueInCustomerInventory;
  }

}
