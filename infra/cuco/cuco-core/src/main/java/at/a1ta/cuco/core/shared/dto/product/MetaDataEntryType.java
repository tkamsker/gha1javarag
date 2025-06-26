package at.a1ta.cuco.core.shared.dto.product;

public enum MetaDataEntryType {
  STRING(1), LONG(2), BOOLEAN(3), DATE_TIME(4), DECIMAL(5), LKMS_ID(6), MBIT(7), KBIT(8), MB(9);

  private int value;

  MetaDataEntryType(int value) {
    this.value = value;
  }

  public int getValue() {
    return value;
  }
}
