package at.a1ta.cuco.core.shared.dto.customerequipment;

import java.util.ArrayList;
import java.util.HashMap;

import at.a1ta.cuco.core.shared.dto.Party;

public class EquipmentTree extends Equipment {
  private ArrayList<EquipmentSum> equipmentSums;
  private EquipmentConsignee equipmentConsignee;
  private Party party;
  private long materialSum;

  @SuppressWarnings("unused")
  private HashMap<String, String> eqtypDictionary;
  @SuppressWarnings("unused")
  private HashMap<String, String> eqartDictionary;

  public Party getParty() {
    return party;
  }

  public void setParty(Party party) {
    this.party = party;
  }

  public ArrayList<EquipmentSum> getEquipmentSums() {
    return equipmentSums;
  }

  public void setEquipmentSums(ArrayList<EquipmentSum> materialCatalog) {
    this.equipmentSums = materialCatalog;
  }

  public EquipmentConsignee getEquipmentConsignee() {
    return equipmentConsignee;
  }

  public void setEquipmentConsignee(EquipmentConsignee equipmentConsignee) {
    this.equipmentConsignee = equipmentConsignee;
  }

  public long getMaterialSum() {
    return materialSum;
  }

  public void setMaterialSum(long materialSum) {
    this.materialSum = materialSum;
  }
}
