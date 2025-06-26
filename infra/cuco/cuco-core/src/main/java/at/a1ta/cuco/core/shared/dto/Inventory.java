package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

public class Inventory implements Serializable {
  private Long aonCustomerNumber;
  private Long assetId;
  private Date contractBindingDate;
  private Long contractId;
  private Long customerId;
  private long id;
  private String unlistedNumberIdentification;
  private String networkOperator;
  private String phoneNumber;
  private Date validFromDate;
  private String productDescription;
  private Long nrInstallations;
  private String detailedDescription;
  private String productCategory;
  private String serviceDescription;
  private String productSsaId;
  private String indexation;

  public Long getAonCustomerNumber() {
    return aonCustomerNumber;
  }

  public void setAonCustomerNumber(Long aonCustomerNumber) {
    this.aonCustomerNumber = aonCustomerNumber;
  }

  public Long getAssetId() {
    return assetId;
  }

  public void setAssetId(Long assetId) {
    this.assetId = assetId;
  }

  public Date getContractBindingDate() {
    return contractBindingDate;
  }

  public void setContractBindingDate(Date contractBindingDate) {
    this.contractBindingDate = contractBindingDate;
  }

  public Long getContractId() {
    return contractId;
  }

  public void setContractId(Long contractId) {
    this.contractId = contractId;
  }

  public Long getCustomerId() {
    return customerId;
  }

  public void setCustomerId(Long customerId) {
    this.customerId = customerId;
  }

  public long getId() {
    return id;
  }

  public void setId(long id) {
    this.id = id;
  }

  public String getNetworkOperator() {
    return networkOperator;
  }

  public void setNetworkOperator(String networkOperator) {
    this.networkOperator = networkOperator;
  }

  public String getPhoneNumber() {
    return phoneNumber;
  }

  public void setPhoneNumber(String phoneNumber) {
    this.phoneNumber = phoneNumber;
  }

  public Date getValidFromDate() {
    return validFromDate;
  }

  public void setValidFromDate(Date validFromDate) {
    this.validFromDate = validFromDate;
  }

  public String getProductDescription() {
    return productDescription;
  }

  public void setProductDescription(String productDescription) {
    this.productDescription = productDescription;
  }

  public Long getNrInstallations() {
    return nrInstallations;
  }

  public void setNrInstallations(Long nrInstallations) {
    this.nrInstallations = nrInstallations;
  }

  public String getUnlistedNumberIdentification() {
    return unlistedNumberIdentification;
  }

  public void setUnlistedNumberIdentification(String unlistedNumberIdentification) {
    this.unlistedNumberIdentification = unlistedNumberIdentification;
  }

  public void setDetailedDescription(String detailedDescription) {
    this.detailedDescription = detailedDescription;
  }

  public String getDetailedDescription() {
    return detailedDescription;
  }

  public void setProductCategory(String productCategory) {
    this.productCategory = productCategory;
  }

  public String getProductCategory() {
    return productCategory;
  }

  public void setServiceDescription(String serviceDescription) {
    this.serviceDescription = serviceDescription;
  }

  public String getServiceDescription() {
    return serviceDescription;
  }

  public void setProductSsaId(String productSsaId) {
    this.productSsaId = productSsaId;
  }

  public String getProductSsaId() {
    return productSsaId;
  }

  public String getIndexation() {
    return indexation;
  }

  public void setIndexation(String indexation) {
    this.indexation = indexation;
  }

}
