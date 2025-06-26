package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

public class ProductDetailFilter implements Serializable {

  private String location;
  private String serviceNumber;
  private String customerType;
  private String productName;
  private String baseServiceNumber;
  private Boolean secretLevel;
  private String ban;
  private String description;
  private String indexation;
  private String details;
  private Date validFrom;
  private Date binding;
  private String lkz;
  private String okz;
  private String callNumber;

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

  public String getBaseServiceNumber() {
    return baseServiceNumber;
  }

  public void setBaseServiceNumber(String baseServiceNumber) {
    this.baseServiceNumber = baseServiceNumber;
  }

  public Boolean getSecretLevel() {
    return secretLevel;
  }

  public void setSecretLevel(Boolean secretLevel) {
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

  public Date getValidFrom() {
    return validFrom;
  }

  public void setValidFrom(Date validFrom) {
    this.validFrom = validFrom;
  }

  public Date getBinding() {
    return binding;
  }

  public void setBinding(Date binding) {
    this.binding = binding;
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

}
