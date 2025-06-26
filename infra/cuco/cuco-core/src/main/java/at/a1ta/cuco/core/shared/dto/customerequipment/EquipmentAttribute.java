package at.a1ta.cuco.core.shared.dto.customerequipment;

import at.a1ta.bite.core.shared.dto.KeyValuePair;

public class EquipmentAttribute extends KeyValuePair {
  private String equipmentId;

  public EquipmentAttribute() {}

  public EquipmentAttribute(String equipmentId, String key, String value) {
    super(key, value);
    this.equipmentId = equipmentId;
  }

  public String getEquipmentId() {
    return equipmentId;
  }

  public void setEquipmentId(String equipmentId) {
    this.equipmentId = equipmentId;
  }
}
