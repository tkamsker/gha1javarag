package at.a1ta.cuco.core.shared.dto;

import java.util.ArrayList;
import java.util.List;

public class AggregatedInventoryProductGroupUsage extends InventoryProductGroupUsage {
  private List<Party> parties;

  public List<Party> getParties() {
    return parties;
  }

  public void setParties(List<Party> parties) {
    this.parties = parties;
  }

  public void addParty(Party party) {
    if (parties == null) {
      parties = new ArrayList<Party>();
    }
    parties.add(party);
  }
}
