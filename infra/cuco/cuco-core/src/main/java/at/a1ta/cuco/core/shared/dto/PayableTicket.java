package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class PayableTicket implements Serializable {

  private Long id;
  private Long customerId;
  private String ban;
  private String lknz;
  private String onkz;
  private String number;
  private Service service;
  private String comment;
  private BiteUser agent;
  private Date exportedDate;
  private Long clearingAccountNumber;
  private Date createDate;
  private Double costs;
  private Party party;

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public Long getCustomerId() {
    return customerId;
  }

  public void setCustomerId(Long customerId) {
    this.customerId = customerId;
  }

  public String getOnkz() {
    return onkz;
  }

  public void setOnkz(String onkz) {
    this.onkz = onkz;
  }

  public String getNumber() {
    return number;
  }

  public void setNumber(String number) {
    this.number = number;
  }

  public Service getService() {
    return service;
  }

  public void setService(Service service) {
    this.service = service;
  }

  public String getComment() {
    return comment;
  }

  public void setComment(String comment) {
    this.comment = comment;
  }

  public BiteUser getAgent() {
    return agent;
  }

  public void setAgent(BiteUser agent) {
    this.agent = agent;
  }

  public Date getExportedDate() {
    return exportedDate;
  }

  public void setExportedDate(Date exportedDate) {
    this.exportedDate = exportedDate;
  }

  public Long getClearingAccountNumber() {
    return clearingAccountNumber;
  }

  public void setClearingAccountNumber(Long clearingAccountNumber) {
    this.clearingAccountNumber = clearingAccountNumber;
  }

  public void setCreateDate(Date createDate) {
    this.createDate = createDate;
  }

  public Date getCreateDate() {
    return createDate;
  }

  public void setCosts(Double costs) {
    this.costs = costs;
  }

  public Double getCosts() {
    return costs;
  }

  public Party getParty() {
    return party;
  }

  public void setParty(Party party) {
    this.party = party;
  }

  @Override
  public int hashCode() {
    return super.hashCode();
  }

  @Override
  public boolean equals(Object obj) {
    if (!(obj instanceof PayableTicket)) {
      return false;
    }
    PayableTicket other = (PayableTicket) obj;
    return id.equals(other.id);
  }

  public static Builder builder() {
    return new Builder();
  }

  public void setBan(String ban) {
    this.ban = ban;
  }

  public String getBan() {
    return ban;
  }

  public void setLknz(String lknz) {
    this.lknz = lknz;
  }

  public String getLknz() {
    return lknz;
  }

  public static class Builder {

    private PayableTicket ticket;

    public Builder() {
      ticket = new PayableTicket();
      ticket.createDate = new Date();
    }

    public Builder forPhoneNumber(PhoneNumber phoneNumber) {
      ticket.setLknz(phoneNumber.getCountryIdentificationNumber());
      ticket.onkz = phoneNumber.getCityIdentificationNumber();
      ticket.number = phoneNumber.getSubscriberNumber();
      ticket.setBan(phoneNumber.getBanId());
      return this;
    }

    public Builder withProductCode(String productCode) {
      getService().setProductCode(productCode);
      return this;
    }

    public Builder disposeExpenses(Double amount) {
      ticket.costs = amount;
      return this;
    }

    public Builder createdBy(BiteUser user) {
      ticket.agent = user;
      return this;
    }

    public Builder chargedAs(ChargingType charging) {
      getService().setChargingType(charging);
      return this;
    }

    private Service getService() {
      if (ticket.service == null) {
        ticket.service = new Service();
      }
      return ticket.service;
    }

    public PayableTicket build() {
      return ticket;
    }

  }

}
