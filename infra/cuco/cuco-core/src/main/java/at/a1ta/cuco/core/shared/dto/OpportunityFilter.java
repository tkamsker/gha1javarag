package at.a1ta.cuco.core.shared.dto;

import java.util.Date;

public class OpportunityFilter {

  public enum FilterType {
    ALL, MYQUOTES, MYAPPROVINGS, MYCUSTOMERS
  };

  public static final String QUOTE_NUMBER = "QUOTENUMBER";
  public static final String FILTER_TYPE = "FILTERTYPE";
  public static final String PARTY_ID = "PARTY_ID";
  public static final String FIRST_NAME = "FIRSTNAME";
  public static final String LAST_NAME = "LASTNAME";
  public static final String CREATOR = "CREATOR";
  public static final String LAST_MODIFIER = "LAST_MODIFIER";
  public static final String LAST_MOD_DATE = "LAST_MOD_DATE";
  public static final String PRODUCT_OFFERING_NAME = "PRODUCTOFFERINGNAME";
  public static final String STATUS = "STATUS";
  public static final String CREATE_DATE = "CREATEDATE";
  public static final String VALID_TO_DATE = "VALIDTODATE";
  public static final String TITLE = "NOTE_TEXT";
  public static final String ASSIGNEE = "ASSIGNEE";

  private String quoteNumber;
  private FilterType filterType;
  private Long userId;
  private Long clearanceUserId;
  private String betreuer;
  private String partyId;
  private String firstName;
  private String lastName;
  private String creator;
  private String lastModifier;
  private String title;
  private String assignee;
  private Date lastModDate;
  private ProductOffering productOfferingName;
  private Salesstage.Status status;
  private Date createDate;
  private Date validToDate;

  public void setPartyId(String partyId) {
    this.partyId = partyId;
  }

  public String getPartyId() {
    return partyId;
  }

  public String getQuoteNumber() {
    return quoteNumber;
  }

  public void setQuoteNumber(String quoteNumber) {
    this.quoteNumber = quoteNumber;
  }

  public String getFirstName() {
    return firstName;
  }

  public void setFirstName(String firstName) {
    this.firstName = firstName;
  }

  public String getLastName() {
    return lastName;
  }

  public void setLastName(String lastName) {
    this.lastName = lastName;
  }

  public ProductOffering getProductOfferingName() {
    return productOfferingName;
  }

  public void setProductOfferingName(ProductOffering productOfferingName) {
    this.productOfferingName = productOfferingName;
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

  public Salesstage.Status getStatus() {
    return status;
  }

  public void setStatus(Salesstage.Status status) {
    this.status = status;
  }

  public Long getUserId() {
    return userId;
  }

  public void setUserId(Long userId) {
    this.userId = userId;
  }

  public String getCreator() {
    return creator;
  }

  public void setCreator(String creator) {
    this.creator = creator;
  }

  public String getLastModifier() {
    return lastModifier;
  }

  public void setLastModifier(String lastModifier) {
    this.lastModifier = lastModifier;
  }

  public FilterType getFilterType() {
    return filterType;
  }

  public void setFilterType(FilterType filterType) {
    this.filterType = filterType;
  }

  public String getBetreuer() {
    return betreuer;
  }

  public void setBetreuer(String betreuer) {
    this.betreuer = betreuer;
  }

  public Date getLastModDate() {
    return lastModDate;
  }

  public void setLastModDate(Date lastModDate) {
    this.lastModDate = lastModDate;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public String getAssignee() {
    return assignee;
  }

  public void setAssignee(String assignee) {
    this.assignee = assignee;
  }

  public Long getClearanceUserId() {
    return clearanceUserId;
  }

  public void setClearanceUserId(Long clearanceUserId) {
    this.clearanceUserId = clearanceUserId;
  }
}
