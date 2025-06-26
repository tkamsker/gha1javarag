package at.a1ta.cuco.core.shared.dto.salesinfo;

public class FeedbackQuestionsRow {
  private String attributeName;
  private String attributeType;
  private Integer numberValue;
  private Boolean booleanValue;
  private String textValue;

  public String getAttributeName() {
    return attributeName;
  }

  public void setAttributeName(String attributeName) {
    this.attributeName = attributeName;
  }

  public String getAttributeType() {
    return attributeType;
  }

  public void setAttributeType(String attributeType) {
    this.attributeType = attributeType;
  }

  public Integer getNumberValue() {
    return numberValue;
  }

  public void setNumberValue(Integer numberValue) {
    this.numberValue = numberValue;
  }

  public Boolean getBooleanValue() {
    return booleanValue;
  }

  public void setBooleanValue(Boolean booleanValue) {
    this.booleanValue = booleanValue;
  }

  public String getTextValue() {
    return textValue;
  }

  public void setTextValue(String textValue) {
    this.textValue = textValue;
  }
}
