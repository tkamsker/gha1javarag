package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;

public class MetaData implements Serializable {
  private ArrayList<MetaDataEntry> list = new ArrayList<MetaDataEntry>();
  private HashMap<String, MetaDataEntry> map = new HashMap<String, MetaDataEntry>();

  public void put(ArrayList<MetaDataEntry> entries) {
    for (MetaDataEntry entry : entries) {
      put(entry);

    }
  }

  public void put(MetaDataEntry entry) {
    list.add(entry);
    map.put(entry.getId() != null ? entry.getId().toLowerCase() : "", entry);
  }

  public ArrayList<MetaDataEntry> getAll() {
    return list;
  }

  public boolean hasMetaData() {
    return !list.isEmpty();
  }

  public boolean hasMetaDataEntryWithName(String name) {
    for (MetaDataEntry entry : getAll()) {
      if (entry != null && entry.getName() != null && entry.getName().equalsIgnoreCase(name)) {
        return true;
      }
    }
    return false;
  }

  public boolean hasMetaDataEntryWithID(String id) {
    for (String key : map.keySet()) {
      if (key != null && key.equalsIgnoreCase(id)) {
        return true;
      }
    }
    return false;
  }

  @Override
  public String toString() {
    StringBuilder sb = new StringBuilder();
    for (MetaDataEntry entry : list) {
      sb.append(entry).append("\r\n");
    }
    return sb.toString();
  }
}
