package at.a1ta.cuco.core.shared.dto;

public enum CustomerInteractionAttributes {
  PRODUCT, REASON1, REASON2, REASON3, RESULT, NOTE;

  public static CustomerInteractionAttributes find(String string) {
    for (CustomerInteractionAttributes attribute : values()) {
      if (attribute.name().equals(string)) {
        return attribute;
      }
    }
    return null;
  }
}
