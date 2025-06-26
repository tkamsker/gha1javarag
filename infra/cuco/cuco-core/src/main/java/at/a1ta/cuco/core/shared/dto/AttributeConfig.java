package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

import at.a1ta.bite.core.shared.dto.BiteUser;

@SuppressWarnings("serial")
public class AttributeConfig implements Serializable {

  public AttributeConfig() {
    super();
  }

  /**
   * Copy Constructor
   * 
   * @param attributeConfig a <code>AttributeConfig</code> object
   */
  public AttributeConfig(AttributeConfig attributeConfig) {
    this.attributeConfigId = attributeConfig.attributeConfigId;
    this.attributeName = attributeConfig.attributeName;
    this.attributeType = attributeConfig.attributeType;
    this.lowerBounds = attributeConfig.lowerBounds;
    this.upperBounds = attributeConfig.upperBounds;
    this.active = attributeConfig.active;
    this.deleted = attributeConfig.deleted;
    this.orderNum = attributeConfig.orderNum;
    this.creator = attributeConfig.creator;
    this.createDate = attributeConfig.createDate;
    this.lastModifier = attributeConfig.lastModifier;
    this.lastUpdate = attributeConfig.lastUpdate;
    this.grouping = attributeConfig.grouping;
    this.segments = attributeConfig.segments;
    this.validValues = attributeConfig.validValues;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((active == null) ? 0 : active.hashCode());
    result = prime * result + ((attributeConfigId == null) ? 0 : attributeConfigId.hashCode());
    result = prime * result + ((attributeName == null) ? 0 : attributeName.hashCode());
    result = prime * result + ((attributeType == null) ? 0 : attributeType.hashCode());
    result = prime * result + ((createDate == null) ? 0 : createDate.hashCode());
    result = prime * result + ((creator == null) ? 0 : creator.hashCode());
    result = prime * result + ((deleted == null) ? 0 : deleted.hashCode());
    result = prime * result + ((grouping == null) ? 0 : grouping.hashCode());
    result = prime * result + ((lastModifier == null) ? 0 : lastModifier.hashCode());
    result = prime * result + ((lastUpdate == null) ? 0 : lastUpdate.hashCode());
    result = prime * result + ((lowerBounds == null) ? 0 : lowerBounds.hashCode());
    result = prime * result + ((orderNum == null) ? 0 : orderNum.hashCode());
    result = prime * result + ((segments == null) ? 0 : segments.hashCode());
    result = prime * result + ((upperBounds == null) ? 0 : upperBounds.hashCode());
    result = prime * result + ((validValues == null) ? 0 : validValues.hashCode());
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
    AttributeConfig other = (AttributeConfig) obj;
    if (active == null) {
      if (other.active != null) {
        return false;
      }
    } else if (!active.equals(other.active)) {
      return false;
    }
    if (attributeConfigId == null) {
      if (other.attributeConfigId != null) {
        return false;
      }
    } else if (!attributeConfigId.equals(other.attributeConfigId)) {
      return false;
    }
    if (attributeName == null) {
      if (other.attributeName != null) {
        return false;
      }
    } else if (!attributeName.equals(other.attributeName)) {
      return false;
    }
    if (attributeType != other.attributeType) {
      return false;
    }
    if (createDate == null) {
      if (other.createDate != null) {
        return false;
      }
    } else if (!createDate.equals(other.createDate)) {
      return false;
    }
    if (creator == null) {
      if (other.creator != null) {
        return false;
      }
    } else if (!creator.equals(other.creator)) {
      return false;
    }
    if (deleted == null) {
      if (other.deleted != null) {
        return false;
      }
    } else if (!deleted.equals(other.deleted)) {
      return false;
    }
    if (grouping != other.grouping) {
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
    if (lowerBounds == null) {
      if (other.lowerBounds != null) {
        return false;
      }
    } else if (!lowerBounds.equals(other.lowerBounds)) {
      return false;
    }
    if (orderNum == null) {
      if (other.orderNum != null) {
        return false;
      }
    } else if (!orderNum.equals(other.orderNum)) {
      return false;
    }
    if (segments == null) {
      if (other.segments != null) {
        return false;
      }
    } else if (!segments.equals(other.segments)) {
      return false;
    }
    if (upperBounds == null) {
      if (other.upperBounds != null) {
        return false;
      }
    } else if (!upperBounds.equals(other.upperBounds)) {
      return false;
    }
    if (validValues == null) {
      if (other.validValues != null) {
        return false;
      }
    } else if (!validValues.equals(other.validValues)) {
      return false;
    }
    return true;
  }

  public static enum ConfigTypes {
    BOOLEAN, NUMBER, DROPDOWN, DATE
  }

  public static enum Groupings {
    VISITREPORT_SBS_TODO_ITEM, SALESINFO_CUSTOMERINFO, VISITREPORT_SBS_FEEDBACK, VISITREPORT_SBS_REFLECTION, VISITREPORT_SALES_CONV_FEEDBACK, //
    DIGITAL_SELLING_INTERNET_SPEED_OLD, DIGITAL_SELLING_INTERNET_SPEED_NEW, DIGITAL_SELLING_TV_OLD, DIGITAL_SELLING_TV_NEW, //
    DIGITAL_SELLING_MOBILE_PHONE_OLD, DIGITAL_SELLING_MOBILE_PHONE_NEW, DIGITAL_SELLING_MOBILE_TARIFF_OLD, DIGITAL_SELLING_MOBILE_TARIFF_NEW, //
    DIGITAL_SELLING_MUSIC, DIGITAL_SELLING_SECURITY_OLD, DIGITAL_SELLING_SECURITY_NEW, DIGITAL_SELLING_SMART_HOME_OLD, DIGITAL_SELLING_SMART_HOME_NEW, //
    DIGITAL_SELLING_PAYMENT_OLD, DIGITAL_SELLING_PAYMENT_NEW, DIGITAL_SELLING_SERVICES_OLD, DIGITAL_SELLING_SERVICES_NEW
  }

  private Long attributeConfigId;
  private String attributeName;
  private String validValues;
  private ConfigTypes attributeType;
  private Integer lowerBounds;
  private Integer upperBounds;
  private Boolean active;
  private Boolean deleted;
  private Integer orderNum;
  private BiteUser creator;
  private Date createDate;
  private BiteUser lastModifier;
  private Date lastUpdate;
  private Groupings grouping;
  private List<String> segments;

  public Long getAttributeConfigId() {
    return attributeConfigId;
  }

  public void setAttributeConfigId(Long attributeConfigId) {
    this.attributeConfigId = attributeConfigId;
  }

  public String getAttributeName() {
    return attributeName;
  }

  public void setAttributeName(String attributeName) {
    this.attributeName = attributeName;
  }

  public ConfigTypes getAttributeType() {
    return attributeType;
  }

  public void setAttributeType(ConfigTypes attributeType) {
    this.attributeType = attributeType;
  }

  public Boolean getActive() {
    return active;
  }

  public boolean getNSActive() {
    return active == null ? false : active;
  }

  public void setActive(Boolean active) {
    this.active = active;
  }

  public Boolean getDeleted() {
    return deleted;
  }

  public Boolean getNSDeleted() {
    return deleted == null ? false : deleted;
  }

  public void setDeleted(Boolean deleted) {
    this.deleted = deleted;
  }

  public Integer getOrderNum() {
    return orderNum;
  }

  public void setOrderNum(Integer orderNum) {
    this.orderNum = orderNum;
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

  public Integer getLowerBounds() {
    return lowerBounds;
  }

  public void setLowerBounds(Integer lowerBounds) {
    this.lowerBounds = lowerBounds;
  }

  public Integer getUpperBounds() {
    return upperBounds;
  }

  public void setUpperBounds(Integer upperBounds) {
    this.upperBounds = upperBounds;
  }

  @Override
  public String toString() {
    return "AttributeConfig [attributeConfigId=" + attributeConfigId + ", attributeName=" + attributeName + ", attributeType=" + attributeType + ", lowerBounds=" + lowerBounds + ", upperBounds="
        + upperBounds + ", active=" + active + ", deleted=" + deleted + ", orderNum=" + orderNum + ", creator=" + creator + ", createDate=" + createDate + ", lastModifier=" + lastModifier
        + ", lastUpdate=" + lastUpdate + ", validValues=" + validValues + "]";
  }

  public Groupings getGrouping() {
    return grouping;
  }

  public void setGrouping(Groupings grouping) {
    this.grouping = grouping;
  }

  public List<String> getSegments() {
    return segments;
  }

  public void setSegments(List<String> segments) {
    this.segments = segments;
  }

  public String getValidValues() {
    return validValues;
  }

  public void setValidValues(String validValues) {
    this.validValues = validValues;
  }

  public boolean isBooleanType() {
    return ConfigTypes.BOOLEAN == getAttributeType();
  }

  public boolean isNumberType() {
    return ConfigTypes.NUMBER == getAttributeType();
  }

  public boolean isComboboxType() {
    return ConfigTypes.DROPDOWN == getAttributeType();
  }

  public boolean isDateType() {
    return ConfigTypes.DATE == getAttributeType();
  }
}
