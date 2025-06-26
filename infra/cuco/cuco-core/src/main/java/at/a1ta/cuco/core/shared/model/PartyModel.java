package at.a1ta.cuco.core.shared.model;

import java.io.Serializable;
import java.util.Date;

public class PartyModel implements Serializable {

  private static final long serialVersionUID = 1L;
  private Long id;
  private String bans;
  private String commercialRegisterNumber;
  private String businessSegment;
  private String serviceClass;
  private String gender;
  private String firstname;
  private String lastname;
  private String addressLine1;
  private String addressLine2;
  private Date birthdate;
  private String region;
  private String teamName;
  private String supportUserName;
  private String attendingShop;
  private String customerType;
  private String npsString;
  private String type;
  private String churnLikeliness;
  private String accumulatedChurnLikeliness;
  private String customerWorthiness;
  private String cooperation;
  private String framework;
  private String creditworthiness;
  private String faxNumber;
  private String vipStatus;
  private String posString;
  private String binding;
  private String assocRegisterNumber;
  private String indexation;
  private String eveStatus;
  private String a1ConnectPlusInfo;

  public Long getId() {
    return id;
  }

  public String getBans() {
    return bans;
  }

  public String getCommercialRegisterNumber() {
    return commercialRegisterNumber;
  }

  public String getBusinessSegment() {
    return businessSegment;
  }

  public String getGender() {
    return gender;
  }

  public String getName() {
    return firstname + " " + lastname;
  }

  public String getAddress() {
    return addressLine1 + ", " + addressLine2;
  }

  public Date getBirthdate() {
    return birthdate;
  }

  public String getRegion() {
    return region;
  }

  public String getTeamName() {
    return teamName;
  }

  public String getSupportUserName() {
    return supportUserName;
  }

  public String getCustomerType() {
    return customerType;
  }

  public String getType() {
    return type;
  }

  public String getChurnLikeliness() {
    return churnLikeliness;
  }

  public String getCustomerWorthiness() {
    return customerWorthiness;
  }

  public String getCooperation() {
    return cooperation;
  }

  public String getFramework() {
    return framework;
  }

  public String getCreditworthiness() {
    return creditworthiness;
  }

  public String getFaxNumber() {
    return faxNumber;
  }

  public String getVipStatus() {
    return vipStatus;
  }

  public String getBinding() {
    return binding;
  }

  public String getAssocRegisterNumber() {
    return assocRegisterNumber;
  }

  public String getIndexation() {
    return indexation;
  }

  void setId(Long id) {
    this.id = id;
  }

  void setBans(String bans) {
    this.bans = bans;
  }

  void setCommercialRegisterNumber(String commercialRegisterNumber) {
    this.commercialRegisterNumber = commercialRegisterNumber;
  }

  void setBusinessSegment(String businessSegment) {
    this.businessSegment = businessSegment;
  }

  void setGender(String gender) {
    this.gender = gender;
  }

  void setBirthdate(Date birthdate) {
    this.birthdate = birthdate;
  }

  void setRegion(String region) {
    this.region = region;
  }

  void setTeamName(String teamName) {
    this.teamName = teamName;
  }

  void setSupportUserName(String supportUserName) {
    this.supportUserName = supportUserName;
  }

  void setCustomerType(String customerType) {
    this.customerType = customerType;
  }

  void setType(String type) {
    this.type = type;
  }

  void setChurnLikeliness(String churnLikeliness) {
    this.churnLikeliness = churnLikeliness;
  }

  void setCustomerWorthiness(String customerWorthiness) {
    this.customerWorthiness = customerWorthiness;
  }

  void setCooperation(String cooperation) {
    this.cooperation = cooperation;
  }

  void setFramework(String framework) {
    this.framework = framework;
  }

  void setCreditworthiness(String creditworthiness) {
    this.creditworthiness = creditworthiness;
  }

  void setFaxNumber(String faxNumber) {
    this.faxNumber = faxNumber;
  }

  void setVipStatus(String vipStatus) {
    this.vipStatus = vipStatus;
  }

  void setBinding(String binding) {
    this.binding = binding;
  }

  void setAssocRegisterNumber(String assocRegisterNumber) {
    this.assocRegisterNumber = assocRegisterNumber;
  }

  public String getAddressLine1() {
    return addressLine1;
  }

  public void setAddressLine1(String addressLine1) {
    this.addressLine1 = addressLine1;
  }

  public String getAddressLine2() {
    return addressLine2;
  }

  public void setAddressLine2(String addressLine2) {
    this.addressLine2 = addressLine2;
  }

  public String getFirstname() {
    return firstname;
  }

  public void setFirstname(String firstname) {
    this.firstname = firstname;
  }

  public String getLastname() {
    return lastname;
  }

  public void setLastname(String lastname) {
    this.lastname = lastname;
  }

  public void setAccumulatedChurnLikeliness(String accumulatedChurnLikeliness) {
    this.accumulatedChurnLikeliness = accumulatedChurnLikeliness;
  }

  public String getAccumulatedChurnLikeliness() {
    return accumulatedChurnLikeliness;
  }

  public String getAttendingShop() {
    return attendingShop;
  }

  public void setAttendingShop(String attendingShop) {
    this.attendingShop = attendingShop;
  }

  void setIndexation(String indexation) {
    this.indexation = indexation;
  }

  public String getServiceClass() {
    return serviceClass;
  }

  public void setServiceClass(String serviceClass) {
    this.serviceClass = serviceClass;
  }

  public String getPosString() {
    return posString;
  }

  public void setPosString(String posString) {
    this.posString = posString;
  }

  public String getEveStatus() {
    return eveStatus;
  }

  public void setEveStatus(String eveStatus) {
    this.eveStatus = eveStatus;
  }

  public String getNpsString() {
    return npsString;
  }

  public void setNpsString(String npsString) {
    this.npsString = npsString;
  }

  public String getA1ConnectPlusInfo() {
    return a1ConnectPlusInfo;
  }

  public void setA1ConnectPlusInfo(String a1ConnectPlusInfo) {
    this.a1ConnectPlusInfo = a1ConnectPlusInfo;
  }

}
