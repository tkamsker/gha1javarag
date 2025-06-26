package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;

@SuppressWarnings("serial")
public class Attribute implements Serializable {
  private Long attributeId;
  private AttributeConfig attributeConfig;
  private Long kundeId;

  /**
   * Copy Constructor
   * 
   * @param attribute a <code>Attribute</code> object
   */
  public Attribute(Attribute attribute) {
    this.attributeId = attribute.getAttributeId();
    this.attributeConfig = new AttributeConfig(attribute.getAttributeConfig());
    this.kundeId = attribute.getKundeId();
    this.booleanValue = attribute.getBooleanValue();
    this.numberValue = attribute.getNumberValue();
    this.lastModifier = attribute.getLastModifier();
    this.lastUpdate = attribute.getLastUpdate();
    this.hasHistory = attribute.isHasHistory();
    this.textValue = attribute.textValue;
  }

  public Attribute() {
    super();
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((attributeConfig == null) ? 0 : attributeConfig.hashCode());
    result = prime * result + ((attributeId == null) ? 0 : attributeId.hashCode());
    result = prime * result + ((booleanValue == null) ? 0 : booleanValue.hashCode());
    result = prime * result + (hasHistory ? 1231 : 1237);
    result = prime * result + ((kundeId == null) ? 0 : kundeId.hashCode());
    result = prime * result + ((lastModifier == null) ? 0 : lastModifier.hashCode());
    result = prime * result + ((lastUpdate == null) ? 0 : lastUpdate.hashCode());
    result = prime * result + ((numberValue == null) ? 0 : numberValue.hashCode());
    result = prime * result + ((textValue == null) ? 0 : textValue.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (obj == null) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    Attribute other = (Attribute) obj;
    if (attributeConfig == null) {
      if (other.attributeConfig != null) {
        return false;
      }
    } else if (!attributeConfig.equals(other.attributeConfig)) {
      return false;
    }
    if (attributeId == null) {
      if (other.attributeId != null) {
        return false;
      }
    } else if (!attributeId.equals(other.attributeId)) {
      return false;
    }
    if (booleanValue == null) {
      if (other.booleanValue != null) {
        return false;
      }
    } else if (!booleanValue.equals(other.booleanValue)) {
      return false;
    }
    if (hasHistory != other.hasHistory) {
      return false;
    }
    if (lastModifier == null) {
      if (other.lastModifier != null) {
        return false;
      }
    } else if (!lastModifier.equals(other.lastModifier)) {
      return false;
    }
    if (lastUpdate == null) {
      if (other.lastUpdate != null) {
        return false;
      }
    } else if (!lastUpdate.equals(other.lastUpdate)) {
      return false;
    }
    if (numberValue == null) {
      if (other.numberValue != null) {
        return false;
      }
    } else if (!numberValue.equals(other.numberValue)) {
      return false;
    }
    if (textValue == null) {
      if (other.textValue != null) {
        return false;
      }
    } else if (!textValue.equals(other.textValue)) {
      return false;
    }
    return true;
  }

  private Boolean booleanValue;
  private Integer numberValue;
  private BiteUser lastModifier;
  private Date lastUpdate;
  private String textValue;
  private boolean hasHistory;

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

  public boolean getNSBooleanValue() {
    return booleanValue == null ? false : booleanValue.booleanValue();
  }

  public void setBooleanValue(Boolean booleanValue) {
    this.booleanValue = booleanValue;
  }

  public Integer getNumberValue() {
    return numberValue;
  }

  public int getNSNumberValue() {
    return numberValue == null ? 0 : numberValue.intValue();
  }

  public void setNumberValue(Integer numberValue) {
    this.numberValue = numberValue;
  }

  public BiteUser getLastModifier() {
    return lastModifier;
  }

  public void setLastModifier(BiteUser lastModifier) {
    this.lastModifier = lastModifier;
  }

  public Date getLastUpdate() {
    return lastUpdate;
  }

  public void setLastUpdate(Date lastUpdate) {
    this.lastUpdate = lastUpdate;
  }

  public boolean isHasHistory() {
    return hasHistory;
  }

  public void setHasHistory(boolean hasHistory) {
    this.hasHistory = hasHistory;
  }

  public String getTextValue() {
    return textValue;
  }

  public void setTextValue(String textValue) {
    this.textValue = textValue;
  }

  @Override
  public String toString() {
    return "Attribute [attributeId=" + attributeId + ", attributeConfig=" + attributeConfig + ", kundeId=" + kundeId + ", booleanValue=" + booleanValue + ", numberValue=" + numberValue
        + ", lastModifier=" + lastModifier + ", lastUpdate=" + lastUpdate + ", textValue=" + textValue + ", hasHistory=" + hasHistory + "]";
  }

}
