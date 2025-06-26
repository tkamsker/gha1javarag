package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

public class PartySearch implements Serializable {
  private String id;
  private String leadId;
  private String lastName;
  private String firstName;
  private Date birthDate;
  private String postcode;
  private String city;
  private String village;
  private String street;
  private String country;
  private String houseNumber;
  private String phoneNumber;
  private String accountingNumber;
  private String aonAccountNumber;
  private String commercialRegisterNumber;
  private String billingAccountNumber;
  private String lkz;
  private String okz;
  private String callNumber;
  private boolean fulltext;
  private String fulltextTerm;
  private String activeSearchField;
  private String supportUserId;
  private boolean nonCustomerSearchRequired;

  private String searchExecutingUserName;

  public String getVillage() {
    return village;
  }

  public void setVillage(String village) {
    this.village = village;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public String getLastName() {
    return lastName;
  }

  public void setLastName(String lastName) {
    this.lastName = lastName;
  }

  public String getFirstName() {
    return firstName;
  }

  public void setFirstName(String firstName) {
    this.firstName = firstName;
  }

  public Date getBirthDate() {
    return birthDate;
  }

  public void setBirthDate(Date birthDate) {
    this.birthDate = birthDate;
  }

  public String getPostcode() {
    return postcode;
  }

  public void setPostcode(String postcode) {
    this.postcode = postcode;
  }

  public String getCity() {
    return city;
  }

  public void setCity(String city) {
    this.city = city;
  }

  public String getStreet() {
    return street;
  }

  public void setStreet(String street) {
    this.street = street;
  }

  public void setCountry(String country) {
    this.country = country;
  }

  public String getCountry() {
    return country;
  }

  public String getHouseNumber() {
    return houseNumber;
  }

  public void setHouseNumber(String houseNumber) {
    this.houseNumber = houseNumber;
  }

  public void setPhoneNumber(String phoneNumber) {
    this.phoneNumber = phoneNumber;
  }

  public String getPhoneNumber() {
    return phoneNumber;
  }

  public void setAccountingNumber(String accountingNumber) {
    this.accountingNumber = accountingNumber;
  }

  public String getAccountingNumber() {
    return accountingNumber;
  }

  public void setAonAccountNumber(String aonAccountNumber) {
    this.aonAccountNumber = aonAccountNumber;
  }

  public String getAonAccountNumber() {
    return aonAccountNumber;
  }

  public void setCommercialRegisterNumber(String commercialRegisterNumber) {
    this.commercialRegisterNumber = commercialRegisterNumber;
  }

  public String getCommercialRegisterNumber() {
    return commercialRegisterNumber;
  }

  public void setBillingAccountNumber(String billingAccountNumber) {
    this.billingAccountNumber = billingAccountNumber;
  }

  public String getBillingAccountNumber() {
    return billingAccountNumber;
  }

  public String getLkz() {
    return lkz;
  }

  public void setLkz(String lkz) {
    this.lkz = lkz;
  }

  public String getOkz() {
    return okz;
  }

  public void setOkz(String okz) {
    this.okz = okz;
  }

  public String getCallNumber() {
    return callNumber;
  }

  public void setCallNumber(String callNumber) {
    this.callNumber = callNumber;
  }

  public boolean isFulltext() {
    return fulltext;
  }

  public void setFulltext(boolean fulltext) {
    this.fulltext = fulltext;
  }

  public String getFulltextTerm() {
    return fulltextTerm;
  }

  public void setFulltextTerm(String fulltextTerm) {
    this.fulltextTerm = fulltextTerm;
  }

  public String getActiveSearchField() {
    return activeSearchField;
  }

  public void setActiveSearchField(String activeSearchField) {
    this.activeSearchField = activeSearchField;
  }

  public void setSearchExecutingUserName(String searchExecutingUserName) {
    this.searchExecutingUserName = searchExecutingUserName;
  }

  public String getSearchExecutingUserName() {
    return searchExecutingUserName;
  }

  public String getLeadId() {
    return leadId;
  }

  public void setLeadId(String leadId) {
    this.leadId = leadId;
  }

  @Override
  public String toString() {
    return this.getClass().getName() + ": id=" + id + "; lastName=" + lastName + "; firstName=" + firstName + "; birthDate=" + birthDate + "; postcode" + postcode + "; city=" + city + "; village=" + village + "; street=" + street + "; country=" + country + "; houseNumber=" + houseNumber
        + "; phoneNumber=" + phoneNumber + "; accountingNumber=" + accountingNumber + "; aonAccountNumber=" + aonAccountNumber + "; commercialRegisterNumber=" + commercialRegisterNumber + "; billingAccountNumber=" + billingAccountNumber + "; lkz=" + lkz + "; okz=" + okz + "; callNumber="
        + callNumber;
  }

  public String getSupportUserId() {
    return supportUserId;
  }

  public void setSupportUserId(String supportUserId) {
    this.supportUserId = supportUserId;
  }

  public boolean isNonCustomerSearchRequired() {
    return nonCustomerSearchRequired;
  }

  public void setNonCustomerSearchRequired(boolean nonCustomerSearchRequired) {
    this.nonCustomerSearchRequired = nonCustomerSearchRequired;
  }

}
