package at.a1ta.cuco.core.shared.dto.customerequipment;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;

public class Equipment implements Serializable, Comparable<Equipment> {
  private static final String TOP_LEVEL_PARENT_ID = "";
  private static final String EMPTY = "";

  private String id;
  private String name;
  private Equipment parent;
  private String parentId;
  private String serialNumber;
  private String status;
  private Date warrentyBegin;
  private Date warrentyEnd;
  private String materialId;
  private String materialName;
  private ArrayList<EquipmentAttribute> attributes;
  private ArrayList<Equipment> children = new ArrayList<Equipment>();
  private String equipmentTyp;
  private String typBezeichnung;
  private String equipmentArt;
  private String artBezeichnung;

  public String getId() {
    return id;
  }

  public void setId(final String id) {
    this.id = id;
  }

  public boolean hasEquipmentId() {
    return id != null && !EMPTY.equals(id);
  }

  public boolean isPartListMaterial() {
    return !hasEquipmentId();
  }

  public String getName() {
    return name;
  }

  public void setName(final String name) {
    this.name = name;
  }

  public Equipment getParent() {
    return parent;
  }

  public void setParent(final Equipment parent) {
    this.parent = parent;
  }

  public String getParentId() {
    return parentId;
  }

  public void setParentId(final String parentId) {
    this.parentId = parentId;
  }

  public boolean isTopLevel() {
    return parentId == null || TOP_LEVEL_PARENT_ID.equals(parentId);
  }

  public boolean isMaterial() {
    // TODO correct implementation
    return materialId != null && !materialId.isEmpty();
  }

  public void addChild(final Equipment child) {
    this.children.add(child);
  }

  public boolean hasChildren() {
    return children != null && !children.isEmpty();
  }

  public ArrayList<Equipment> getChildren() {
    return children;
  }

  public void setChildren(ArrayList<Equipment> children) {
    this.children = children;
  }

  public String getSerialNumber() {
    return serialNumber;
  }

  public void setSerialNumber(final String serialNumber) {
    this.serialNumber = serialNumber;
  }

  public String getStatus() {
    return status;
  }

  public void setStatus(final String status) {
    this.status = status;
  }

  public Date getWarrentyBegin() {
    return warrentyBegin;
  }

  public void setWarrentyBegin(final Date warrentyBegin) {
    this.warrentyBegin = warrentyBegin;
  }

  public Date getWarrentyEnd() {
    return warrentyEnd;
  }

  public void setWarrentyEnd(final Date warrentyEnd) {
    this.warrentyEnd = warrentyEnd;
  }

  public String getMaterialId() {
    return materialId;
  }

  public void setMaterialId(String materialId) {
    this.materialId = materialId;
  }

  public String getMaterialName() {
    return materialName;
  }

  public void setMaterialName(String materialName) {
    this.materialName = materialName;
  }

  public ArrayList<EquipmentAttribute> getAttributes() {
    return attributes;
  }

  public void setAttributes(ArrayList<EquipmentAttribute> attributes) {
    this.attributes = attributes;
  }

  public boolean hasAttributes() {
    return attributes != null && !attributes.isEmpty();
  }

  public boolean hasEquipmentTyp() {
    return equipmentTyp != null && !equipmentTyp.isEmpty();
  }

  public String getEquipmentTyp() {
    return equipmentTyp;
  }

  public void setEquipmentTyp(String equipmentTyp) {
    this.equipmentTyp = equipmentTyp;
  }

  public String getTypBezeichnung() {
    return typBezeichnung;
  }

  public void setTypBezeichnung(String typBezeichnung) {
    this.typBezeichnung = typBezeichnung;
  }

  public boolean hasEquipmentArt() {
    return equipmentArt != null && !equipmentArt.isEmpty();
  }

  public String getEquipmentArt() {
    return equipmentArt;
  }

  public void setEquipmentArt(String equipmentArt) {
    this.equipmentArt = equipmentArt;
  }

  public String getArtBezeichnung() {
    return artBezeichnung;
  }

  public void setArtBezeichnung(String artBezeichnung) {
    this.artBezeichnung = artBezeichnung;
  }

  /**
   * Returns the tree level of the Equipment. A tree level of 0 means that the Equipment is a top level node without a
   * parent, a level of 2 means that the Equipment has a parent and a grand-parent node
   * 
   * @return The actual tree level
   */
  public int calculateTreeLevel() {
    return calculateTreeLevel(this, 0);
  }

  private int calculateTreeLevel(final Equipment equipment, int level) {
    if (equipment.parent == null) {
      return level;
    }
    return calculateTreeLevel(equipment.parent, level + 1);
  }

  @Override
  public int compareTo(final Equipment o) {
    final String thisName = name != null ? name : EMPTY;
    final String otherName = o.name != null ? o.name : EMPTY;
    return thisName.compareTo(otherName);
  }

  @Override
  public String toString() {
    return "Equipment: " + "ID=" + id + ", ParentID=" + parentId;
  }

  public String toTreeString() {
    return toTreeString(0);
  }

  public String toTreeString(int level) {
    String prefix = "";
    String prefixSpace = "  ";
    for (int i = 0; i < level; i++) {
      prefix += prefixSpace;
    }

    String s = "\r\n" + prefix + "[" + id + "] " + getName();
    if (hasChildren()) {
      for (Equipment child : children) {
        s += child.toTreeString(level + 1);
      }
    }
    return s;
  }

}
