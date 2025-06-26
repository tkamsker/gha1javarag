package at.a1ta.cuco.core.shared.dto.usagedata;

public enum NetworkProvider {
  A1("T", "A1"), ANB("A", "ANB"), COMBINED("C", "Combined");

  private String value;
  private String label;

  private NetworkProvider(String value, String label) {
    this.value = value;
    this.label = label;
  }

  public String getValue() {
    return value;
  }

  public String getLabel() {
    return label;
  }

}
