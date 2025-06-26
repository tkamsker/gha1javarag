package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.math.BigDecimal;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class MyOpportunity implements Serializable {

  private static final long serialVersionUID = 1L;
  private Long partyid;
  private String leadId;
  private int partyType;
  private String quoteNumber;
  private String firstname;
  private String lastname;
  private String creator;
  private BiteUser creatorPerson;
  private String lastModifier;
  private BiteUser lastModifierPerson;
  private ProductOffering productOffering;
  private Salesstage.Status status;
  private Date createDate;
  private Date validToDate;
  private BigDecimal monthlyTurnoverFixed;
  private BigDecimal monthlyTurnoverMobile;
  private BigDecimal monthlyTurnoverOther;
  private BigDecimal onetimeCostTotal;
  private BigDecimal yearlyCostTotal;
  private BigDecimal monthlyCostTotal;
  private String clearanceInitiator;
  private String clearanceFinalApprover;
  private String clearancePendingWith;

  public Long getPartyid() {
    return partyid;
  }

  public void setPartyid(Long partyid) {
    this.partyid = partyid;
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

  public ProductOffering getProductOffering() {
    return productOffering;
  }

  public void setProductOffering(ProductOffering productOffering) {
    this.productOffering = productOffering;
  }

  public Salesstage.Status getStatus() {
    return status;
  }

  public void setStatus(Salesstage.Status status) {
    this.status = status;
  }

  public Date getCreateDate() {
    return createDate;
  }

  public void setCreateDate(Date createDate) {
    this.createDate = createDate;
  }

  public Date getValidToDate() {
    return validToDate;
  }

  public void setValidToDate(Date validToDate) {
    this.validToDate = validToDate;
  }

  public BigDecimal getMonthlyTurnoverFixed() {
    return monthlyTurnoverFixed;
  }

  public void setMonthlyTurnoverFixed(BigDecimal monthlyTturnoverFixed) {
    this.monthlyTurnoverFixed = monthlyTturnoverFixed;
  }

  public BigDecimal getMonthlyTurnoverMobile() {
    return monthlyTurnoverMobile;
  }

  public void setMonthlyTurnoverMobile(BigDecimal monthlyTurnoverMobile) {
    this.monthlyTurnoverMobile = monthlyTurnoverMobile;
  }

  public BigDecimal getMonthlyTurnoverOther() {
    return monthlyTurnoverOther;
  }

  public BigDecimal getMonthlyTurnoverSum() {
    return monthlyTurnoverFixed.add(monthlyTurnoverMobile).add(monthlyTurnoverOther);
  }

  public void setMonthlyTurnoverOther(BigDecimal monthlyTurnoverOther) {
    this.monthlyTurnoverOther = monthlyTurnoverOther;
  }

  public BigDecimal getOnetimeCostTotal() {
    return onetimeCostTotal;
  }

  public void setOnetimeCostTotal(BigDecimal onetimeCostTotal) {
    this.onetimeCostTotal = onetimeCostTotal;
  }

  public BigDecimal getYearlyCostTotal() {
    return yearlyCostTotal;
  }

  public void setYearlyCostTotal(BigDecimal yearlyCostTotal) {
    this.yearlyCostTotal = yearlyCostTotal;
  }

  public BigDecimal getMonthlyCostTotal() {
    return monthlyCostTotal;
  }

  public void setMonthlyCostTotal(BigDecimal monthlyCostTotal) {
    this.monthlyCostTotal = monthlyCostTotal;
  }

  @Override
  public String toString() {
    return "MyOpportunity [partyid=" + partyid + ", firstname=" + firstname + ", lastname=" + lastname + ", productOffering=" + productOffering + ", status=" + status + ", createDate=" + createDate
        + ", validToDate=" + validToDate + ", monthlyTturnoverFixed=" + monthlyTurnoverFixed + ", monthlyTurnoverMobile=" + monthlyTurnoverMobile + ", monthlyTurnoverOther=" + monthlyTurnoverOther
        + ", onetimeCostTotal=" + onetimeCostTotal + ", yearlyCostTotal=" + yearlyCostTotal + ", monthlyCostTotal=" + monthlyCostTotal + "]";
  }

  public String getQuoteNumber() {
    return quoteNumber;
  }

  public void setQuoteNumber(String quoteNumber) {
    this.quoteNumber = quoteNumber;
  }

  public String getLastModifier() {
    return lastModifier;
  }

  public void setLastModifier(String lastModifier) {
    this.lastModifier = lastModifier;
  }

  public String getCreator() {
    return creator;
  }

  public void setCreator(String creator) {
    this.creator = creator;
  }

  public BiteUser getCreatorPerson() {
    return creatorPerson;
  }

  public void setCreatorPerson(BiteUser creatorPerson) {
    this.creatorPerson = creatorPerson;
  }

  public BiteUser getLastModifierPerson() {
    return lastModifierPerson;
  }

  public void setLastModifierPerson(BiteUser lastModifierPerson) {
    this.lastModifierPerson = lastModifierPerson;
  }

  public String getLeadId() {
    return leadId;
  }

  public void setLeadId(String leadId) {
    this.leadId = leadId;
  }

  public int getPartyType() {
    return partyType;
  }

  public void setPartyType(int partyType) {
    this.partyType = partyType;
  }

  public String getClearanceInitiator() {
    return clearanceInitiator;
  }

  public void setClearanceInitiator(String clearanceInitiator) {
    this.clearanceInitiator = clearanceInitiator;
  }

  public String getClearanceFinalApprover() {
    return clearanceFinalApprover;
  }

  public void setClearanceFinalApprover(String clearanceFinalApprover) {
    this.clearanceFinalApprover = clearanceFinalApprover;
  }

  public String getClearancePendingWith() {
    return clearancePendingWith;
  }

  public void setClearancePendingWith(String clearancePendingWith) {
    this.clearancePendingWith = clearancePendingWith;
  }

}
