package at.a1ta.cuco.core.shared.model.productdetail;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;

import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PhoneNumber;
import at.a1ta.cuco.core.shared.model.AddressLinkData;

public class ProductDetail implements Serializable {
  private String category;
  private String locationId;
  private String location;
  private String serviceNumber;
  private String aonCustomerNumber;
  private String customerMarker;
  private String customerType;
  private String productName;
  private String baseService;
  private String secretLevel;
  private String ban;
  private String description;
  private String indexation;
  private String details;
  private Date validFrom;
  private Date binding;
  private boolean anb;

  private Long partyId;
  private Party party;

  private boolean locationExpanded = true;
  private boolean numberExpanded = true;
  private ArrayList<ProductDetail> locationSiblings = new ArrayList<ProductDetail>();
  private ArrayList<ProductDetail> numberSiblings = new ArrayList<ProductDetail>();
  private AddressLinkData addressLinkData;

  private PhoneNumber phoneNumber;

  public ProductDetail() {}

  public ProductDetail(Long partyId) {
    this.partyId = partyId;
  }

  public String getLocation() {
    return location;
  }

  public void setLocation(String location) {
    this.location = location;
  }

  public String getServiceNumber() {
    return serviceNumber;
  }

  public void setServiceNumber(String serviceNumber) {
    this.serviceNumber = serviceNumber;
  }

  public void setAonCustomerNumber(String aonCustomerNumber) {
    this.aonCustomerNumber = aonCustomerNumber;
  }

  public String getAonCustomerNumber() {
    return aonCustomerNumber;
  }

  public String getCustomerMarker() {
    return customerMarker;
  }

  public void setCustomerMarker(String customerMarker) {
    this.customerMarker = customerMarker;
  }

  public String getCustomerType() {
    return customerType;
  }

  public void setCustomerType(String customerType) {
    this.customerType = customerType;
  }

  public String getProductName() {
    return productName;
  }

  public void setProductName(String productName) {
    this.productName = productName;
  }

  public String getBaseService() {
    return baseService;
  }

  public void setBaseService(String baseService) {
    this.baseService = baseService;
  }

  public String getSecretLevel() {
    return secretLevel;
  }

  public void setSecretLevel(String secretLevel) {
    this.secretLevel = secretLevel;
  }

  public String getBan() {
    return ban;
  }

  public void setBan(String ban) {
    this.ban = ban;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public String getIndexation() {
    return indexation;
  }

  public void setIndexation(String indexation) {
    this.indexation = indexation;
  }

  public String getDetails() {
    return details;
  }

  public void setDetails(String details) {
    this.details = details;
  }

  public Date getBinding() {
    return binding;
  }

  public void setBinding(Date binding) {
    this.binding = binding;
  }

  public ArrayList<ProductDetail> getNumberSiblings() {
    return numberSiblings;
  }

  public void setNumberSiblings(ArrayList<ProductDetail> numberSiblings) {
    this.numberSiblings = numberSiblings;
  }

  public void setPartyId(Long partyId) {
    this.partyId = partyId;
  }

  public Long getPartyId() {
    return partyId;
  }

  public void setParty(Party party) {
    this.party = party;
  }

  public Party getParty() {
    return party;
  }

  public boolean hasNumberSiblings() {
    return numberSiblings != null && numberSiblings.size() > 0;
  }

  public void addNumberSibling(ProductDetail sibling) {
    if (sibling != this) {
      numberSiblings.add(sibling);
    }
  }

  public void setLocationId(String locationId) {
    this.locationId = locationId;
  }

  public String getLocationId() {
    return locationId;
  }

  public void setLocationSiblings(ArrayList<ProductDetail> locationSiblings) {
    this.locationSiblings = locationSiblings;
  }

  public ArrayList<ProductDetail> getLocationSiblings() {
    return locationSiblings;
  }

  public void addLocationSibling(ProductDetail sibling) {
    if (sibling != this) {
      locationSiblings.add(sibling);
    }
  }

  public void setNumberExpanded(boolean numberExpanded) {
    this.numberExpanded = numberExpanded;
  }

  public boolean isNumberExpanded() {
    return numberExpanded;
  }

  public void setLocationExpanded(boolean locationExpanded) {
    this.locationExpanded = locationExpanded;
  }

  public boolean isLocationExpanded() {
    return locationExpanded;
  }

  public void setAnb(boolean anb) {
    this.anb = anb;
  }

  public boolean isAnb() {
    return anb;
  }

  public void setCategory(String category) {
    this.category = category;
  }

  public String getCategory() {
    return category;
  }

  public PhoneNumber getPhoneNumber() {
    return phoneNumber;
  }

  public void setPhoneNumber(PhoneNumber phoneNumber) {
    this.phoneNumber = phoneNumber;
  }

  public Date getValidFrom() {
    return validFrom;
  }

  public void setValidFrom(Date validFrom) {
    this.validFrom = validFrom;
  }

  public AddressLinkData getAddressLinkData() {
    return addressLinkData;
  }

  public void setAddressLinkData(AddressLinkData addressLinkData) {
    this.addressLinkData = addressLinkData;
  }
}
