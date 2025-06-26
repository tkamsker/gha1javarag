package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class SAPProductNode extends BaseNode implements Serializable {
  private String text;
  private MetaData equipmentAttributes;

  @Override
  public String getText() {
    return text;
  }

  public void setText(String text) {
    this.text = text;
  }

  public MetaData getEquipmentAttributes() {
    return equipmentAttributes;
  }

  public void setEquipmentAttributes(MetaData equipmentAttributes) {
    this.equipmentAttributes = equipmentAttributes;
  }

}
