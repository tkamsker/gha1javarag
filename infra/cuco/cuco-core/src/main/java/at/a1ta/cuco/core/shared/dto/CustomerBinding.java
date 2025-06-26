package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.cuco.core.shared.model.AddressLinkData;

public class CustomerBinding implements Serializable {
  private String partyId;
  private Date contractStart;
  private Date contractEnd;
  private String productDescription;
  private Customer customer;
  private String service;
  private String productNumber;
  private String serviceNumber;
  private Long aonCustomerNumber;
  private String productCategory;
  private String connectorSpecification;
  private AddressLinkData location;
  private Long contractId;
  private int type;
  private String indexation;

  public String getProductDescription() {
    return productDescription;
  }

  public void setProductDescription(String productDescription) {
    this.productDescription = productDescription;
  }

  public Date getContractEnd() {
    return contractEnd;
  }

  public void setContractEnd(Date contractEnd) {
    this.contractEnd = contractEnd;
  }

  public Date getContractStart() {
    return contractStart;
  }

  public void setContractStart(Date contractStart) {
    this.contractStart = contractStart;
  }

  public String getPartyId() {
    return partyId;
  }

  public void setPartyId(String partyId) {
    this.partyId = partyId;
  }

  public void setCustomer(Customer customer) {
    this.customer = customer;
  }

  public Customer getCustomer() {
    return customer;
  }

  public void setService(String service) {
    this.service = service;
  }

  public String getService() {
    return service;
  }

  public void setProductNumber(String productNumber) {
    this.productNumber = productNumber;
  }

  public String getProductNumber() {
    return productNumber;
  }

  public void setLocation(AddressLinkData location) {
    this.location = location;
  }

  public AddressLinkData getLocation() {
    return location;
  }

  public void setProductCategory(String productCategory) {
    this.productCategory = productCategory;
  }

  public String getProductCategory() {
    return productCategory;
  }

  public void setConnectorSpecification(String connectorSpecification) {
    this.connectorSpecification = connectorSpecification;
  }

  public String getConnectorSpecification() {
    return connectorSpecification;
  }

  public void setServiceNumber(String serviceNumber) {
    this.serviceNumber = serviceNumber;
  }

  public String getServiceNumber() {
    return serviceNumber;
  }

  public void setAonCustomerNumber(Long aonCustomerNumber) {
    this.aonCustomerNumber = aonCustomerNumber;
  }

  public Long getAonCustomerNumber() {
    return aonCustomerNumber;
  }

  public void setContractId(Long contractId) {
    this.contractId = contractId;
  }

  public Long getContractId() {
    return contractId;
  }

  public void setType(int type) {
    this.type = type;
  }

  public int getType() {
    return type;
  }

  public String getIndexation() {
    return indexation;
  }

  public void setIndexation(String indexation) {
    this.indexation = indexation;
  }
}
