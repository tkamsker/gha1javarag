package at.a1ta.cuco.core.shared.dto;

import java.util.Date;
import java.util.List;

import org.apache.solr.client.solrj.beans.Field;

import at.a1ta.cuco.core.shared.dto.nbo.VBMProduct;

public class Customer extends Person {
  private static final long serialVersionUID = 1L;
  private String businessRuleDescription;
  private String businessSegment;
  private Integer businessVolume;
  private String centralAssociationNumber;
  private String churnLikeliness;
  private String commercialRegisterNumber;
  private String commercialSector;
  private Date contactPersonBirthdate;
  private String contactPersonFirstName;
  private String contactPersonGender;
  private String contactPersonLastName;
  private String contactPersonSalutation;
  private String contactPersonTitle;
  private String contactPhoneNumber1;
  private String contactPhoneNumber2;
  private String cooperationDescription;
  private String creditworthiness;
  private long id;
  private String customerWorthclass;
  private boolean deliveryBlock;
  private String eMailAddress;
  private String faxNumber;
  private long headerId;
  private String homepageAddress;
  private String mobilePhoneNumber;
  private Integer nrEmployees;
  private String productUsageCS;
  private String productUsagePPC;
  private String region;
  private String supportUserId;
  private String supportUserName;
  private String teamName;
  private boolean listedInFramework;
  private boolean onBlacklist;
  private boolean onRobinsonlist;
  private String city;
  private String village;
  private String country;
  private String housenumber;
  private String poBox;
  private String street;
  private String currentBinding;
  private String currentBindingRuntime;
  private boolean hasOpenOffer;
  private String customerType;
  private boolean subsidised;
  private Date timestamp;
  // time zone independent date of birth
  private long dateOfBirth;
  private String indexation;
  private List<VBMProduct> availableVbmProducts;

  public Date getTimestamp() {
    return timestamp;
  }

  public void setTimestamp(Date timestamp) {
    this.timestamp = timestamp;
  }

  public String getBusinessRuleDescription() {
    return businessRuleDescription;
  }

  public String getBusinessSegment() {
    return businessSegment;
  }

  public Integer getBusinessVolume() {
    return businessVolume;
  }

  public String getCentralAssociationNumber() {
    return centralAssociationNumber;
  }

  public String getChurnLikeliness() {
    return churnLikeliness;
  }

  public String getCommercialRegisterNumber() {
    return commercialRegisterNumber;
  }

  public String getCommercialSector() {
    return commercialSector;
  }

  public Date getContactPersonBirthdate() {
    return contactPersonBirthdate;
  }

  public String getContactPersonFirstName() {
    return contactPersonFirstName;
  }

  public String getContactPersonGender() {
    return contactPersonGender;
  }

  public String getContactPersonLastName() {
    return contactPersonLastName;
  }

  public String getContactPersonSalutation() {
    return contactPersonSalutation;
  }

  public String getContactPersonTitle() {
    return contactPersonTitle;
  }

  public String getContactPhoneNumber1() {
    return contactPhoneNumber1;
  }

  public String getContactPhoneNumber2() {
    return contactPhoneNumber2;
  }

  public String getCooperationDescription() {
    return cooperationDescription;
  }

  public String getCreditworthiness() {
    return creditworthiness;
  }

  public long getCustomerNumber() {
    return id;
  }

  public String getCustomerWorthclass() {
    return customerWorthclass;
  }

  public boolean hasDeliveryBlock() {
    return deliveryBlock;
  }

  public String getEMailAddress() {
    return eMailAddress;
  }

  public long getHeaderId() {
    return headerId;
  }

  public String getHomepageAddress() {
    return homepageAddress;
  }

  public long getId() {
    return id;
  }

  public String getMobilePhoneNumber() {
    return mobilePhoneNumber;
  }

  public Integer getNrEmployees() {
    return nrEmployees;
  }

  public String getProductUsageCS() {
    return productUsageCS;
  }

  public String getProductUsagePPC() {
    return productUsagePPC;
  }

  public String getRegion() {
    return region;
  }

  public String getSupportUserId() {
    return supportUserId;
  }

  public String getSupportUserName() {
    return supportUserName;
  }

  public String getTeamName() {
    return teamName;
  }

  public boolean isListedInFramework() {
    return listedInFramework;
  }

  public boolean isOnBlacklist() {
    return onBlacklist;
  }

  public boolean isOnRobinsonlist() {
    return onRobinsonlist;
  }

  public String getAddressWithoutVillage() {
    final StringBuilder sb = new StringBuilder(30);
    if (this.street != null) {
      sb.append(this.street);
      if (this.housenumber != null) {
        sb.append(" ");
        sb.append(this.housenumber);
      }
      sb.append(", ");
    }
    if (this.poBox != null) {
      sb.append(this.poBox);
    }
    if (this.city != null) {
      sb.append(" ");
      sb.append(this.city);
    }
    return sb.toString();
  }

  public String getFullAddress() {
    return getAddressLine1() + ", " + getAddressLine2();
  }

  public String getAddressLine1() {
    final StringBuilder sb = new StringBuilder(30);
    if (this.street != null) {
      sb.append(this.street);
      if (this.housenumber != null) {
        sb.append(" ");
        sb.append(this.housenumber);
      }
    }
    return sb.toString();
  }

  public String getAddressLine2() {
    final StringBuilder sb = new StringBuilder(30);
    if (this.poBox != null) {
      sb.append(this.poBox);
    }
    if (this.city != null) {
      sb.append(" ");
      sb.append(this.city);
    }
    if (this.village != null) {
      sb.append(" (");
      sb.append(this.village);
      sb.append(")");
    }
    return sb.toString();
  }

  public String getCity() {
    return city;
  }

  public String getCountry() {
    return country;
  }

  public String getHousenumber() {
    return housenumber;
  }

  public String getPoBox() {
    return poBox;
  }

  public String getStreet() {
    return street;
  }

  public String getCurrentBinding() {
    return currentBinding;
  }

  public boolean getHasOpenOffer() {
    return hasOpenOffer;
  }

  public String getIndexation() {
    return indexation;
  }

  public void setBusinessRuleDescription(String businessRuleDescription) {
    this.businessRuleDescription = businessRuleDescription;
  }

  @Field("segment")
  public void setBusinessSegment(String businessSegment) {
    this.businessSegment = businessSegment;
  }

  public void setBusinessVolume(Integer businessVolume) {
    this.businessVolume = businessVolume;
  }

  @Field("centralassociationnumber")
  public void setCentralAssociationNumber(String centralAssociationNumber) {
    this.centralAssociationNumber = centralAssociationNumber;
  }

  public void setChurnLikeliness(String churnLikeliness) {
    this.churnLikeliness = churnLikeliness;
  }

  @Field("commercialregisternumber")
  public void setCommercialRegisterNumber(String commercialRegisterNumber) {
    this.commercialRegisterNumber = commercialRegisterNumber;
  }

  public void setCommercialSector(String commercialSector) {
    this.commercialSector = commercialSector;
  }

  public void setContactPersonBirthdate(Date contactPersonBirthdate) {
    this.contactPersonBirthdate = contactPersonBirthdate;
  }

  public void setContactPersonFirstName(String contactPersonFirstName) {
    this.contactPersonFirstName = contactPersonFirstName;
  }

  public void setContactPersonGender(String contactPersonGender) {
    this.contactPersonGender = contactPersonGender;
  }

  public void setContactPersonLastName(String contactPersonLastName) {
    this.contactPersonLastName = contactPersonLastName;
  }

  public void setContactPersonSalutation(String contactPersonSalutation) {
    this.contactPersonSalutation = contactPersonSalutation;
  }

  public void setContactPersonTitle(String contactPersonTitle) {
    this.contactPersonTitle = contactPersonTitle;
  }

  public void setContactPhoneNumber1(String contactPhoneNumber1) {
    this.contactPhoneNumber1 = contactPhoneNumber1;
  }

  public void setContactPhoneNumber2(String contactPhoneNumber2) {
    this.contactPhoneNumber2 = contactPhoneNumber2;
  }

  public void setCooperationDescription(String cooperationDescription) {
    this.cooperationDescription = cooperationDescription;
  }

  public void setCreditworthiness(String creditworthiness) {
    this.creditworthiness = creditworthiness;
  }

  public void setId(long id) {
    this.id = id;
  }

  @Field("customernumber")
  void setId(String id) {
    this.id = Long.valueOf(id);
  }

  public void setCustomerWorthclass(String customerWorthclass) {
    this.customerWorthclass = customerWorthclass;
  }

  public void setDeliveryBlock(boolean deliveryBlock) {
    this.deliveryBlock = deliveryBlock;
  }

  @Field("email")
  public void setEMailAddress(String eMailAddress) {
    this.eMailAddress = eMailAddress;
  }

  @Field("headerid")
  void setHeaderId(String headerId) {
    this.headerId = Long.valueOf(headerId);
  }

  public void setHeaderId(long headerId) {
    this.headerId = headerId;
  }

  @Field("homepage")
  public void setHomepageAddress(String homepageAddress) {
    this.homepageAddress = homepageAddress;
  }

  public void setMobilePhoneNumber(String mobilePhoneNumber) {
    this.mobilePhoneNumber = mobilePhoneNumber;
  }

  public void setNrEmployees(Integer nrEmployees) {
    this.nrEmployees = nrEmployees;
  }

  public void setProductUsageCS(String productUsageCS) {
    this.productUsageCS = productUsageCS;
  }

  public void setProductUsagePPC(String productUsagePPC) {
    this.productUsagePPC = productUsagePPC;
  }

  public void setRegion(String region) {
    this.region = region;
  }

  @Field("serviceagentuser")
  public void setSupportUserId(String supportUserId) {
    this.supportUserId = supportUserId;
  }

  @Field("serviceagentname")
  public void setSupportUserName(String supportUserName) {
    this.supportUserName = supportUserName;
  }

  public void setTeamName(String teamName) {
    this.teamName = teamName;
  }

  public void setListedInFramework(boolean listedInFramework) {
    this.listedInFramework = listedInFramework;
  }

  public void setOnBlacklist(boolean onBlacklist) {
    this.onBlacklist = onBlacklist;
  }

  public void setOnRobinsonlist(boolean onRobinsonlist) {
    this.onRobinsonlist = onRobinsonlist;
  }

  @Field("city")
  public void setCity(String city) {
    this.city = city;
  }

  @Field("country")
  public void setCountry(String country) {
    this.country = country;
  }

  @Field("housenumber")
  public void setHousenumber(String housenumber) {
    this.housenumber = housenumber;
  }

  @Field("postcode")
  public void setPoBox(String poBox) {
    this.poBox = poBox;
  }

  @Field("street")
  public void setStreet(String street) {
    this.street = street;
  }

  public String getVillage() {
    return village;
  }

  @Field("village")
  public void setVillage(String village) {
    this.village = village;
  }

  public void setCurrentBinding(String currentBinding) {
    this.currentBinding = currentBinding;
  }

  public void setHasOpenOffer(boolean hasOpenOffer) {
    this.hasOpenOffer = hasOpenOffer;
  }

  public String getCustomerType() {
    return customerType;
  }

  public void setCustomerType(String customerType) {
    this.customerType = customerType;
  }

  public String getFaxNumber() {
    return faxNumber;
  }

  public void setFaxNumber(String faxNumber) {
    this.faxNumber = faxNumber;
  }

  public boolean hasCurrentBindingRuntime() {
    return currentBindingRuntime != null;
  }

  public String getCurrentBindingRuntime() {
    return currentBindingRuntime;
  }

  public void setCurrentBindingRuntime(String currentBindingRuntime) {
    this.currentBindingRuntime = currentBindingRuntime;
  }

  public boolean isSubsidised() {
    return subsidised;
  }

  public void setSubsidised(boolean subsidised) {
    this.subsidised = subsidised;
  }

  public void setDateOfBirth(long dateOfBirth) {
    this.dateOfBirth = dateOfBirth;
  }

  public void setIndexation(String indexation) {
    this.indexation = indexation;
  }

  public long getDateOfBirth() {
    return dateOfBirth <= 0 ? (getBirthdate() != null ? getBirthdate().getTime() : 0) : dateOfBirth;
  }

  public List<VBMProduct> getAvailableVbmProducts() {
    return availableVbmProducts;
  }

  public void setAvailableVbmProducts(List<VBMProduct> availableVbmProducts) {
    this.availableVbmProducts = availableVbmProducts;
  }

  public String getVbmProductsAsString() {
    String result = "";
    if (availableVbmProducts != null && !availableVbmProducts.isEmpty()) {
      for (VBMProduct product : availableVbmProducts) {
        if (product.getProductDetails() != null) {
          result += "," + product.getProductDetails().getProductName();
        }
      }
      if (result.trim().startsWith(",")) {
        result = result.trim().replaceFirst(",", "");
      }
    }
    return result;
  }

  public String getVbmProductsWithSeparator() {
    String result = "";
    if (availableVbmProducts != null && !availableVbmProducts.isEmpty()) {
      for (VBMProduct product : availableVbmProducts) {
        if (product.getProductDetails() != null) {
          result += ";" + product.getProductDetails().getProductName();
        }
      }
      if (result.trim().startsWith(";")) {
        result = result.trim().replaceFirst(";", "");
      }
    }
    return result;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = super.hashCode();
    result = prime * result + ((availableVbmProducts == null) ? 0 : availableVbmProducts.hashCode());
    result = prime * result + ((businessRuleDescription == null) ? 0 : businessRuleDescription.hashCode());
    result = prime * result + ((businessSegment == null) ? 0 : businessSegment.hashCode());
    result = prime * result + ((businessVolume == null) ? 0 : businessVolume.hashCode());
    result = prime * result + ((centralAssociationNumber == null) ? 0 : centralAssociationNumber.hashCode());
    result = prime * result + ((churnLikeliness == null) ? 0 : churnLikeliness.hashCode());
    result = prime * result + ((city == null) ? 0 : city.hashCode());
    result = prime * result + ((commercialRegisterNumber == null) ? 0 : commercialRegisterNumber.hashCode());
    result = prime * result + ((commercialSector == null) ? 0 : commercialSector.hashCode());
    result = prime * result + ((contactPersonBirthdate == null) ? 0 : contactPersonBirthdate.hashCode());
    result = prime * result + ((contactPersonFirstName == null) ? 0 : contactPersonFirstName.hashCode());
    result = prime * result + ((contactPersonGender == null) ? 0 : contactPersonGender.hashCode());
    result = prime * result + ((contactPersonLastName == null) ? 0 : contactPersonLastName.hashCode());
    result = prime * result + ((contactPersonSalutation == null) ? 0 : contactPersonSalutation.hashCode());
    result = prime * result + ((contactPersonTitle == null) ? 0 : contactPersonTitle.hashCode());
    result = prime * result + ((contactPhoneNumber1 == null) ? 0 : contactPhoneNumber1.hashCode());
    result = prime * result + ((contactPhoneNumber2 == null) ? 0 : contactPhoneNumber2.hashCode());
    result = prime * result + ((cooperationDescription == null) ? 0 : cooperationDescription.hashCode());
    result = prime * result + ((country == null) ? 0 : country.hashCode());
    result = prime * result + ((creditworthiness == null) ? 0 : creditworthiness.hashCode());
    result = prime * result + ((currentBinding == null) ? 0 : currentBinding.hashCode());
    result = prime * result + ((currentBindingRuntime == null) ? 0 : currentBindingRuntime.hashCode());
    result = prime * result + ((customerType == null) ? 0 : customerType.hashCode());
    result = prime * result + ((customerWorthclass == null) ? 0 : customerWorthclass.hashCode());
    result = prime * result + (int) (dateOfBirth ^ (dateOfBirth >>> 32));
    result = prime * result + (deliveryBlock ? 1231 : 1237);
    result = prime * result + ((eMailAddress == null) ? 0 : eMailAddress.hashCode());
    result = prime * result + ((faxNumber == null) ? 0 : faxNumber.hashCode());
    result = prime * result + (hasOpenOffer ? 1231 : 1237);
    result = prime * result + (int) (headerId ^ (headerId >>> 32));
    result = prime * result + ((homepageAddress == null) ? 0 : homepageAddress.hashCode());
    result = prime * result + ((housenumber == null) ? 0 : housenumber.hashCode());
    result = prime * result + (int) (id ^ (id >>> 32));
    result = prime * result + ((indexation == null) ? 0 : indexation.hashCode());
    result = prime * result + (listedInFramework ? 1231 : 1237);
    result = prime * result + ((mobilePhoneNumber == null) ? 0 : mobilePhoneNumber.hashCode());
    result = prime * result + ((nrEmployees == null) ? 0 : nrEmployees.hashCode());
    result = prime * result + (onBlacklist ? 1231 : 1237);
    result = prime * result + (onRobinsonlist ? 1231 : 1237);
    result = prime * result + ((poBox == null) ? 0 : poBox.hashCode());
    result = prime * result + ((productUsageCS == null) ? 0 : productUsageCS.hashCode());
    result = prime * result + ((productUsagePPC == null) ? 0 : productUsagePPC.hashCode());
    result = prime * result + ((region == null) ? 0 : region.hashCode());
    result = prime * result + ((street == null) ? 0 : street.hashCode());
    result = prime * result + (subsidised ? 1231 : 1237);
    result = prime * result + ((supportUserId == null) ? 0 : supportUserId.hashCode());
    result = prime * result + ((supportUserName == null) ? 0 : supportUserName.hashCode());
    result = prime * result + ((teamName == null) ? 0 : teamName.hashCode());
    result = prime * result + ((timestamp == null) ? 0 : timestamp.hashCode());
    result = prime * result + ((village == null) ? 0 : village.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (!super.equals(obj)) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    Customer other = (Customer) obj;
    if (availableVbmProducts == null) {
      if (other.availableVbmProducts != null) {
        return false;
      }
    } else if (!availableVbmProducts.equals(other.availableVbmProducts)) {
      return false;
    }
    if (businessRuleDescription == null) {
      if (other.businessRuleDescription != null) {
        return false;
      }
    } else if (!businessRuleDescription.equals(other.businessRuleDescription)) {
      return false;
    }
    if (businessSegment == null) {
      if (other.businessSegment != null) {
        return false;
      }
    } else if (!businessSegment.equals(other.businessSegment)) {
      return false;
    }
    if (businessVolume == null) {
      if (other.businessVolume != null) {
        return false;
      }
    } else if (!businessVolume.equals(other.businessVolume)) {
      return false;
    }
    if (centralAssociationNumber == null) {
      if (other.centralAssociationNumber != null) {
        return false;
      }
    } else if (!centralAssociationNumber.equals(other.centralAssociationNumber)) {
      return false;
    }
    if (churnLikeliness == null) {
      if (other.churnLikeliness != null) {
        return false;
      }
    } else if (!churnLikeliness.equals(other.churnLikeliness)) {
      return false;
    }
    if (city == null) {
      if (other.city != null) {
        return false;
      }
    } else if (!city.equals(other.city)) {
      return false;
    }
    if (commercialRegisterNumber == null) {
      if (other.commercialRegisterNumber != null) {
        return false;
      }
    } else if (!commercialRegisterNumber.equals(other.commercialRegisterNumber)) {
      return false;
    }
    if (commercialSector == null) {
      if (other.commercialSector != null) {
        return false;
      }
    } else if (!commercialSector.equals(other.commercialSector)) {
      return false;
    }
    if (contactPersonBirthdate == null) {
      if (other.contactPersonBirthdate != null) {
        return false;
      }
    } else if (!contactPersonBirthdate.equals(other.contactPersonBirthdate)) {
      return false;
    }
    if (contactPersonFirstName == null) {
      if (other.contactPersonFirstName != null) {
        return false;
      }
    } else if (!contactPersonFirstName.equals(other.contactPersonFirstName)) {
      return false;
    }
    if (contactPersonGender == null) {
      if (other.contactPersonGender != null) {
        return false;
      }
    } else if (!contactPersonGender.equals(other.contactPersonGender)) {
      return false;
    }
    if (contactPersonLastName == null) {
      if (other.contactPersonLastName != null) {
        return false;
      }
    } else if (!contactPersonLastName.equals(other.contactPersonLastName)) {
      return false;
    }
    if (contactPersonSalutation == null) {
      if (other.contactPersonSalutation != null) {
        return false;
      }
    } else if (!contactPersonSalutation.equals(other.contactPersonSalutation)) {
      return false;
    }
    if (contactPersonTitle == null) {
      if (other.contactPersonTitle != null) {
        return false;
      }
    } else if (!contactPersonTitle.equals(other.contactPersonTitle)) {
      return false;
    }
    if (contactPhoneNumber1 == null) {
      if (other.contactPhoneNumber1 != null) {
        return false;
      }
    } else if (!contactPhoneNumber1.equals(other.contactPhoneNumber1)) {
      return false;
    }
    if (contactPhoneNumber2 == null) {
      if (other.contactPhoneNumber2 != null) {
        return false;
      }
    } else if (!contactPhoneNumber2.equals(other.contactPhoneNumber2)) {
      return false;
    }
    if (cooperationDescription == null) {
      if (other.cooperationDescription != null) {
        return false;
      }
    } else if (!cooperationDescription.equals(other.cooperationDescription)) {
      return false;
    }
    if (country == null) {
      if (other.country != null) {
        return false;
      }
    } else if (!country.equals(other.country)) {
      return false;
    }
    if (creditworthiness == null) {
      if (other.creditworthiness != null) {
        return false;
      }
    } else if (!creditworthiness.equals(other.creditworthiness)) {
      return false;
    }
    if (currentBinding == null) {
      if (other.currentBinding != null) {
        return false;
      }
    } else if (!currentBinding.equals(other.currentBinding)) {
      return false;
    }
    if (currentBindingRuntime == null) {
      if (other.currentBindingRuntime != null) {
        return false;
      }
    } else if (!currentBindingRuntime.equals(other.currentBindingRuntime)) {
      return false;
    }
    if (customerType == null) {
      if (other.customerType != null) {
        return false;
      }
    } else if (!customerType.equals(other.customerType)) {
      return false;
    }
    if (customerWorthclass == null) {
      if (other.customerWorthclass != null) {
        return false;
      }
    } else if (!customerWorthclass.equals(other.customerWorthclass)) {
      return false;
    }
    if (dateOfBirth != other.dateOfBirth) {
      return false;
    }
    if (deliveryBlock != other.deliveryBlock) {
      return false;
    }
    if (eMailAddress == null) {
      if (other.eMailAddress != null) {
        return false;
      }
    } else if (!eMailAddress.equals(other.eMailAddress)) {
      return false;
    }
    if (faxNumber == null) {
      if (other.faxNumber != null) {
        return false;
      }
    } else if (!faxNumber.equals(other.faxNumber)) {
      return false;
    }
    if (hasOpenOffer != other.hasOpenOffer) {
      return false;
    }
    if (headerId != other.headerId) {
      return false;
    }
    if (homepageAddress == null) {
      if (other.homepageAddress != null) {
        return false;
      }
    } else if (!homepageAddress.equals(other.homepageAddress)) {
      return false;
    }
    if (housenumber == null) {
      if (other.housenumber != null) {
        return false;
      }
    } else if (!housenumber.equals(other.housenumber)) {
      return false;
    }
    if (id != other.id) {
      return false;
    }
    if (indexation == null) {
      if (other.indexation != null) {
        return false;
      }
    } else if (!indexation.equals(other.indexation)) {
      return false;
    }
    if (listedInFramework != other.listedInFramework) {
      return false;
    }
    if (mobilePhoneNumber == null) {
      if (other.mobilePhoneNumber != null) {
        return false;
      }
    } else if (!mobilePhoneNumber.equals(other.mobilePhoneNumber)) {
      return false;
    }
    if (nrEmployees == null) {
      if (other.nrEmployees != null) {
        return false;
      }
    } else if (!nrEmployees.equals(other.nrEmployees)) {
      return false;
    }
    if (onBlacklist != other.onBlacklist) {
      return false;
    }
    if (onRobinsonlist != other.onRobinsonlist) {
      return false;
    }
    if (poBox == null) {
      if (other.poBox != null) {
        return false;
      }
    } else if (!poBox.equals(other.poBox)) {
      return false;
    }
    if (productUsageCS == null) {
      if (other.productUsageCS != null) {
        return false;
      }
    } else if (!productUsageCS.equals(other.productUsageCS)) {
      return false;
    }
    if (productUsagePPC == null) {
      if (other.productUsagePPC != null) {
        return false;
      }
    } else if (!productUsagePPC.equals(other.productUsagePPC)) {
      return false;
    }
    if (region == null) {
      if (other.region != null) {
        return false;
      }
    } else if (!region.equals(other.region)) {
      return false;
    }
    if (street == null) {
      if (other.street != null) {
        return false;
      }
    } else if (!street.equals(other.street)) {
      return false;
    }
    if (subsidised != other.subsidised) {
      return false;
    }
    if (supportUserId == null) {
      if (other.supportUserId != null) {
        return false;
      }
    } else if (!supportUserId.equals(other.supportUserId)) {
      return false;
    }
    if (supportUserName == null) {
      if (other.supportUserName != null) {
        return false;
      }
    } else if (!supportUserName.equals(other.supportUserName)) {
      return false;
    }
    if (teamName == null) {
      if (other.teamName != null) {
        return false;
      }
    } else if (!teamName.equals(other.teamName)) {
      return false;
    }
    if (timestamp == null) {
      if (other.timestamp != null) {
        return false;
      }
    } else if (!timestamp.equals(other.timestamp)) {
      return false;
    }
    if (village == null) {
      if (other.village != null) {
        return false;
      }
    } else if (!village.equals(other.village)) {
      return false;
    }
    return true;
  }

}
