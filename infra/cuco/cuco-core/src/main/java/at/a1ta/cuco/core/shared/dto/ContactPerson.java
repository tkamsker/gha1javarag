package at.a1ta.cuco.core.shared.dto;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class ContactPerson extends Person {
  private static final long serialVersionUID = 1L;
  private Long customerId;
  private String customerRole;
  private String dayPhoneNumber;
  private String faxNumber;
  private Long id;
  private boolean isMainContact;
  private String mail;
  private String mobilephoneNumber;
  private String nightPhoneNumber;
  private String taRoleId;
  private String taRoleName;
  private String cctRoleName;
  private String addressLine1;
  private String addressLine2;
  private String source;
  private String uUserId;

  public String getuUserId() {
    return uUserId;
  }

  public void setuUserId(String uUserId) {
    this.uUserId = uUserId;
  }

  private ContactPersonType typeBasedOnSource;
  private boolean active;
  private boolean referenceExists;
  private boolean selected;

  public boolean isReferenceExists() {
    return referenceExists;
  }

  public void setReferenceExists(boolean referenceExists) {
    this.referenceExists = referenceExists;
  }

  private int deleted = 0;
  private BiteUser lastModifier;

  public enum ContactPersonType {
    FIXED_LINE("TA"), KUMS("MK"), MOBILE("KUMS"), CUCO("CU");
    private String dbValue;

    private ContactPersonType(String value) {
      this.dbValue = value;
    }

    public String getDbValue() {
      return dbValue;
    }
  }

  public void setCustomerId(Long customerId) {
    this.customerId = customerId;
  }

  public void setCustomerRole(String customerRole) {
    this.customerRole = customerRole;
  }

  public void setDayPhoneNumber(String dayPhoneNumber) {
    this.dayPhoneNumber = dayPhoneNumber;
  }

  public void setFaxNumber(String faxNumber) {
    this.faxNumber = faxNumber;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public void setMainContact(boolean isMainContact) {
    this.isMainContact = isMainContact;
  }

  public void setMail(String mail) {
    this.mail = mail;
  }

  public void setMobilephoneNumber(String mobilephoneNumber) {
    this.mobilephoneNumber = mobilephoneNumber;
  }

  public void setNightPhoneNumber(String nightPhoneNumber) {
    this.nightPhoneNumber = nightPhoneNumber;
  }

  public void setTARoleId(String roleId) {
    taRoleId = roleId;
  }

  public void setTARoleName(String roleName) {
    taRoleName = roleName;
  }

  public void setAddressLine1(String addressLine1) {
    this.addressLine1 = addressLine1;
  }

  public void setAddressLine2(String addressLine2) {
    this.addressLine2 = addressLine2;
  }

  public Long getCustomerId() {
    return this.customerId;
  }

  public String getCustomerRole() {
    return this.customerRole;
  }

  public String getDayPhoneNumber() {
    return this.dayPhoneNumber;
  }

  public String getFaxNumber() {
    return this.faxNumber;
  }

  public Long getId() {
    return this.id;
  }

  public boolean isMainContact() {
    return this.isMainContact;
  }

  public String getMail() {
    return this.mail;
  }

  public String getMobilephoneNumber() {
    return this.mobilephoneNumber;
  }

  public String getNightPhoneNumber() {
    return this.nightPhoneNumber;
  }

  public String getTARoleId() {
    return this.taRoleId;
  }

  public String getTARoleName() {
    return this.taRoleName;
  }

  public String getAddressLine1() {
    return this.addressLine1;
  }

  public String getAddressLine2() {
    return this.addressLine2;
  }

  public String getCity() {
    return this.addressLine2;
  }

  public String getCountry() {
    return null;
  }

  public String getHousenumber() {
    return null;
  }

  public String getPoBox() {
    return null;
  }

  public String getStreet() {
    return this.addressLine2;
  }

  public void setSource(String source) {
    this.source = source;
  }

  public String getSource() {
    return source;
  }

  public String getDisplayName() {
    StringBuilder sb = new StringBuilder();
    if (getSalutation() != null) {
      sb.append(getSalutation() + ", ");
    }
    if (getTitle() != null && !getTitle().trim().isEmpty()) {
      sb.append(getTitle() + " ");
    }
    if (getLastname() != null) {
      sb.append(getLastname() + " ");
    }
    if (getFirstname() != null) {
      sb.append(getFirstname());
    }

    return sb.toString();
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((taRoleId == null) ? 0 : taRoleId.hashCode());
    result = prime * result + ((taRoleName == null) ? 0 : taRoleName.hashCode());
    result = prime * result + ((addressLine1 == null) ? 0 : addressLine1.hashCode());
    result = prime * result + ((addressLine2 == null) ? 0 : addressLine2.hashCode());
    result = prime * result + ((customerId == null) ? 0 : customerId.hashCode());
    result = prime * result + ((customerRole == null) ? 0 : customerRole.hashCode());
    result = prime * result + ((dayPhoneNumber == null) ? 0 : dayPhoneNumber.hashCode());
    result = prime * result + ((faxNumber == null) ? 0 : faxNumber.hashCode());
    result = prime * result + ((id == null) ? 0 : id.hashCode());
    result = prime * result + (isMainContact ? 1231 : 1237);
    result = prime * result + ((mail == null) ? 0 : mail.hashCode());
    result = prime * result + ((mobilephoneNumber == null) ? 0 : mobilephoneNumber.hashCode());
    result = prime * result + ((nightPhoneNumber == null) ? 0 : nightPhoneNumber.hashCode());
    result = prime * result + ((source == null) ? 0 : source.hashCode());
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
    ContactPerson other = (ContactPerson) obj;
    if (taRoleId == null) {
      if (other.taRoleId != null) {
        return false;
      }
    } else if (!taRoleId.equals(other.taRoleId)) {
      return false;
    }
    if (taRoleName == null) {
      if (other.taRoleName != null) {
        return false;
      }
    } else if (!taRoleName.equals(other.taRoleName)) {
      return false;
    }
    if (addressLine1 == null) {
      if (other.addressLine1 != null) {
        return false;
      }
    } else if (!addressLine1.equals(other.addressLine1)) {
      return false;
    }
    if (addressLine2 == null) {
      if (other.addressLine2 != null) {
        return false;
      }
    } else if (!addressLine2.equals(other.addressLine2)) {
      return false;
    }
    if (customerId == null) {
      if (other.customerId != null) {
        return false;
      }
    } else if (!customerId.equals(other.customerId)) {
      return false;
    }
    if (customerRole == null) {
      if (other.customerRole != null) {
        return false;
      }
    } else if (!customerRole.equals(other.customerRole)) {
      return false;
    }
    if (dayPhoneNumber == null) {
      if (other.dayPhoneNumber != null) {
        return false;
      }
    } else if (!dayPhoneNumber.equals(other.dayPhoneNumber)) {
      return false;
    }
    if (faxNumber == null) {
      if (other.faxNumber != null) {
        return false;
      }
    } else if (!faxNumber.equals(other.faxNumber)) {
      return false;
    }
    if (id == null) {
      if (other.id != null) {
        return false;
      }
    } else if (!id.equals(other.id)) {
      return false;
    }
    if (isMainContact != other.isMainContact) {
      return false;
    }
    if (mail == null) {
      if (other.mail != null) {
        return false;
      }
    } else if (!mail.equals(other.mail)) {
      return false;
    }
    if (mobilephoneNumber == null) {
      if (other.mobilephoneNumber != null) {
        return false;
      }
    } else if (!mobilephoneNumber.equals(other.mobilephoneNumber)) {
      return false;
    }
    if (nightPhoneNumber == null) {
      if (other.nightPhoneNumber != null) {
        return false;
      }
    } else if (!nightPhoneNumber.equals(other.nightPhoneNumber)) {
      return false;
    }
    if (source == null) {
      if (other.source != null) {
        return false;
      }
    } else if (!source.equals(other.source)) {
      return false;
    }
    return true;
  }

  public boolean equalsById(ContactPerson otherContact) {
    return ((getId() != null && getId().equals(otherContact.getId())) || (getuUserId() != null && getuUserId().equalsIgnoreCase(otherContact.getId() + "")))
        || (getuUserId() != null && getuUserId().equalsIgnoreCase(otherContact.getuUserId()));
  }

  public boolean isActive() {
    return active;
  }

  public void setActive(boolean active) {
    this.active = active;
  }

  public BiteUser getLastModifier() {
    return lastModifier;
  }

  public void setLastModifier(BiteUser lastModifier) {
    this.lastModifier = lastModifier;
  }

  public ContactPersonType getTypeBasedOnSource() {
    if (source == null || source.isEmpty()) {
      return null;
    } else if (source.equalsIgnoreCase("TA")) {
      return ContactPersonType.FIXED_LINE;
    } else if (source.equalsIgnoreCase("MK")) {
      return ContactPersonType.MOBILE;
    } else if (source.equalsIgnoreCase("KUMS")) {
      return ContactPersonType.KUMS;
    } else if (source.equalsIgnoreCase("CU")) {
      return ContactPersonType.CUCO;
    }
    return null;
  }

  @Override
  public String toString() {
    return "ContactPerson [customerId=" + customerId + ", customerRole=" + customerRole + ", dayPhoneNumber=" + dayPhoneNumber + ", faxNumber=" + faxNumber + ", id=" + id + ", isMainContact="
        + isMainContact + ", mail=" + mail + ", mobilephoneNumber=" + mobilephoneNumber + ", nightPhoneNumber=" + nightPhoneNumber + ", TARoleId=" + taRoleId + ", TARoleName=" + taRoleName
        + ", addressLine1=" + addressLine1 + ", addressLine2=" + addressLine2 + ", source=" + source + ", typeBasedOnSource=" + typeBasedOnSource + ", active=" + active + ", lastModifier="
        + getLastModifier() + "]" + super.toString();
  }

  public String toStringForUISearch() {
    return customerRole + " " + dayPhoneNumber + " " + faxNumber + " " + mail + " " + mobilephoneNumber + " " + nightPhoneNumber + " " + taRoleId + " " + taRoleName + " " + source + " "
        + typeBasedOnSource + " " + getFormattedName();
  }

  public int getDeleted() {
    return deleted;
  }

  public boolean isDeleted() {
    return deleted == 1;
  }

  public void setDeleted(int deleted) {
    this.deleted = deleted;
  }

  public boolean isCuCoContact() {
    return getSource() != null && getSource().equalsIgnoreCase("CU");
  }

  public boolean isKUMSContact() {
    return getSource() != null && getSource().equalsIgnoreCase("KUMS");
  }

  public String getFormattedName() {
    StringBuilder sb = new StringBuilder();

    if (getSalutation() != null) {
      sb.append(getSalutation() + " ");
    }
    if (getLastname() != null) {
      sb.append(getLastname() + " ");
    }
    if (getFirstname() != null) {
      sb.append(getFirstname());
    }
    if (getTitle() != null) {
      sb.append(", " + getTitle());
    }
    return sb.toString();
  }

  public String getFormattedNameWithoutSalutation() {
    StringBuilder sb = new StringBuilder();

    if (getLastname() != null) {
      sb.append(getLastname() + " ");
    }
    if (getFirstname() != null) {
      sb.append(getFirstname());
    }
    if (getTitle() != null) {
      sb.append(", " + getTitle());
    }
    return sb.toString();
  }

  public String getFullAddress() {
    StringBuilder sbr = new StringBuilder();
    if (getAddressLine1() != null) {
      sbr.append(getAddressLine1()).append(getAddressLine2() != null ? "," : "");
    }
    if (getAddressLine2() != null) {
      sbr.append(getAddressLine2());
    }
    return sbr.toString();
  }

  public boolean isSelected() {
    return selected;
  }

  public void setSelected(boolean selected) {
    this.selected = selected;
  }

  public String getCctRoleName() {
    return cctRoleName;
  }

  public void setCctRoleName(String cctRoleName) {
    this.cctRoleName = cctRoleName;
  }
}
