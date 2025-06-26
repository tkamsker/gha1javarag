package at.a1ta.cuco.core.shared.dto.salesinfo;

import java.util.Date;
import java.util.List;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class SalesConvNoteReportRow {

  private long siNoteId;
  private String predecessorSiNoteId;
  private String campaignId;
  private String campaignName;
  private Date lastUpdate;
  private BiteUser lastModUser;
  private String customerId;
  private String customerFirstName;
  private String customerLastName;
  private String contactType;
  private boolean taskActive;
  private Date taskStartDate;
  private List<SalesConvProductNoteRow> productNotes;
  private List<FeedbackQuestionsRow> feedbackQuestions;
  private boolean deleted;
  private boolean finalized;

  public long getSiNoteId() {
    return siNoteId;
  }

  public void setSiNoteId(long siNoteId) {
    this.siNoteId = siNoteId;
  }

  public String getCampaignId() {
    return campaignId;
  }

  public void setCampaignId(String campaignId) {
    this.campaignId = campaignId;
  }

  public String getCampaignName() {
    return campaignName;
  }

  public void setCampaignName(String campaignName) {
    this.campaignName = campaignName;
  }

  public Date getLastUpdate() {
    return lastUpdate;
  }

  public void setLastUpdate(Date lastUpdate) {
    this.lastUpdate = lastUpdate;
  }

  public BiteUser getLastModUser() {
    return lastModUser;
  }

  public void setLastModUser(BiteUser lastModUser) {
    this.lastModUser = lastModUser;
  }

  public String getCustomerId() {
    return customerId;
  }

  public void setCustomerId(String customerId) {
    this.customerId = customerId;
  }

  public String getCustomerFirstName() {
    return customerFirstName;
  }

  public void setCustomerFirstName(String customerFirstName) {
    this.customerFirstName = customerFirstName;
  }

  public String getCustomerLastName() {
    return customerLastName;
  }

  public void setCustomerLastName(String customerLastName) {
    this.customerLastName = customerLastName;
  }

  public String getContactType() {
    return contactType;
  }

  public void setContactType(String contactType) {
    this.contactType = contactType;
  }

  public boolean isTaskActive() {
    return taskActive;
  }

  public void setTaskActive(boolean taskActive) {
    this.taskActive = taskActive;
  }

  public Date getTaskStartDate() {
    return taskStartDate;
  }

  public void setTaskStartDate(Date taskStartDate) {
    this.taskStartDate = taskStartDate;
  }

  public List<SalesConvProductNoteRow> getProductNotes() {
    return productNotes;
  }

  public void setProductNotes(List<SalesConvProductNoteRow> productNotes) {
    this.productNotes = productNotes;
  }

  public List<FeedbackQuestionsRow> getFeedbackQuestions() {
    return feedbackQuestions;
  }

  public void setFeedbackQuestions(List<FeedbackQuestionsRow> feedbackQuestions) {
    this.feedbackQuestions = feedbackQuestions;
  }

  public String getPredecessorSiNoteId() {
    return predecessorSiNoteId;
  }

  public void setPredecessorSiNoteId(String predecessorSiNoteId) {
    this.predecessorSiNoteId = predecessorSiNoteId;
  }

  public boolean isDeleted() {
    return this.deleted;
  }

  public void setDeleted(boolean deleted) {
    this.deleted = deleted;
  }

  public boolean isFinalized() {
    return finalized;
  }

  public void setFinalized(boolean finalized) {
    this.finalized = finalized;
  }
}