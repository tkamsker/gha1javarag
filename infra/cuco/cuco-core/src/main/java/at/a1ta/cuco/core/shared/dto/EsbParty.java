package at.a1ta.cuco.core.shared.dto;

public class EsbParty {

  long partyId;
  String shortName;
  StandardAddress address;

  public long getPartyId() {
    return partyId;
  }

  public void setPartyId(long partyId) {
    this.partyId = partyId;
  }

  public String getShortName() {
    return shortName;
  }

  public void setShortName(String shortName) {
    this.shortName = shortName;
  }

  public StandardAddress getAddress() {
    return address;
  }

  public void setAddress(StandardAddress address) {
    this.address = address;
  }

}
