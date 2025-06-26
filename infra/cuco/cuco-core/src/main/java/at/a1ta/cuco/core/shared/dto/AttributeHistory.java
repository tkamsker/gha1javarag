package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;

@SuppressWarnings("serial")
public class AttributeHistory implements Serializable {
  private Long attributeId;
  private AttributeConfig attributeConfig;
  private Long kundeId;
  private Boolean booleanValue;
  private Integer numberValue;
  private String textValue;
  private BiteUser creator;
  private Date createDate;

  public Long getAttributeId() {
    return attributeId;
  }

  public void setAttributeId(Long attributeId) {
    this.attributeId = attributeId;
  }

  public AttributeConfig getAttributeConfig() {
    return attributeConfig;
  }

  public void setAttributeConfig(AttributeConfig attributeConfig) {
    this.attributeConfig = attributeConfig;
  }

  public Long getKundeId() {
    return kundeId;
  }

  public void setKundeId(Long kundeId) {
    this.kundeId = kundeId;
  }

  public Boolean getBooleanValue() {
    return booleanValue;
  }

  public void setBooleanValue(Boolean booleanValue) {
    this.booleanValue = booleanValue;
  }

  public Integer getNumberValue() {
    return numberValue;
  }

  public void setNumberValue(Integer numberValue) {
    this.numberValue = numberValue;
  }

  public BiteUser getCreator() {
    return creator;
  }

  public void setCreator(BiteUser creator) {
    this.creator = creator;
  }

  public Date getCreateDate() {
    return createDate;
  }

  public void setCreateDate(Date createDate) {
    this.createDate = createDate;
  }

  public String getTextValue() {
    return textValue;
  }

  public void setTextValue(String textValue) {
    this.textValue = textValue;
  }

}
