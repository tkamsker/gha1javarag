package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;

public class BANCollection implements Serializable {
  private long partyId;
  private ArrayList<BillingAccountNumber> bans;

  public BANCollection() {}

  public BANCollection(long partyId) {
    this.partyId = partyId;
  }

  public BANCollection(long partyId, ArrayList<BillingAccountNumber> bans) {
    this.partyId = partyId;
    this.bans = bans;
  }

  public long getPartyId() {
    return partyId;
  }

  public void setPartyId(long partyId) {
    this.partyId = partyId;
  }

  public ArrayList<BillingAccountNumber> getBANs() {
    return bans;
  }

  public void setBANs(ArrayList<BillingAccountNumber> bans) {
    this.bans = bans;
  }
}
