package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;

public class ProductTree implements Serializable {
  private HashMap<Long, ArrayList<Location>> locationMap;
  private ArrayList<BaseNode> partyNodes;

  public HashMap<Long, ArrayList<Location>> getLocationMap() {
    return locationMap;
  }

  public void setLocationMap(HashMap<Long, ArrayList<Location>> locations) {
    this.locationMap = locations;
  }

  public ArrayList<BaseNode> getPartyNodes() {
    return partyNodes;
  }

  public void setPartyNodes(ArrayList<BaseNode> partyNodes) {
    this.partyNodes = partyNodes;
  }
}
