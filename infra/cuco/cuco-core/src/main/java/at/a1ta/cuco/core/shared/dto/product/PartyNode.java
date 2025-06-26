package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class PartyNode extends BaseNode implements Serializable {
  private String name;
  private String address;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getAddress() {
    return address;
  }

  public void setAddress(String address) {
    this.address = address;
  }

  @Override
  public String getText() {
    return name + " (" + getPartyId() + ")";
  }

  public String getDetailedText() {
    return getText() + ", " + address;
  }

}
