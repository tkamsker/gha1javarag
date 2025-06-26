package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.util.Date;

public class MetaDataEntry implements Serializable {
  private String name;
  private String description;
  private String value;
  private String id;
  private MetaDataEntryType type;
  private Date validForStart;
  private Date validForEnd;

  public MetaDataEntry() {}

  public MetaDataEntry(String name, String desc, String value, MetaDataEntryType type) {
    this.name = name;
    this.description = desc;
    this.value = value;
    this.type = type;
  }

  public MetaDataEntry(String name, String desc, String value, MetaDataEntryType type, String id) {
    this.name = name;
    this.description = desc;
    this.value = value;
    this.type = type;
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public String getValue() {
    return value;
  }

  public void setValue(String value) {
    this.value = value;
  }

  public MetaDataEntryType getType() {
    return type;
  }

  public void setType(MetaDataEntryType type) {
    this.type = type;
  }

  public Date getValidForEnd() {
    return validForEnd;
  }

  public void setValidForEnd(Date validForEnd) {
    this.validForEnd = validForEnd;
  }

  public Date getValidForStart() {
    return validForStart;
  }

  @Override
  public String toString() {
    return "name=" + name + "; value=" + value + "; type=" + type + "; validForStart=" + validForStart + "; validForEnd=" + validForEnd + "; id=" + id;
  }

  public void setValidForStart(Date validForStart) {
    this.validForStart = validForStart;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }
}
