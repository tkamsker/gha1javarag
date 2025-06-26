package at.a1ta.cuco.core.shared.dto.salesinfo;

public class SalesConvProductNoteRow {
  private long productNoteId;
  private String predecessorSiNoteId;
  private String productCategory;
  private String productDisplayName;
  private String setupCategory;
  private String quoteStatus;
  private String turnoverQuantity;
  private String assigneeType;
  private int contactCount;
  private boolean deleted;

  public String getProductCategory() {
    return productCategory;
  }

  public void setProductCategory(String productCategory) {
    this.productCategory = productCategory;
  }

  public String getProductDisplayName() {
    return productDisplayName;
  }

  public void setProductDisplayName(String productDisplayName) {
    this.productDisplayName = productDisplayName;
  }

  public String getSetupCategory() {
    return setupCategory;
  }

  public void setSetupCategory(String setupCategory) {
    this.setupCategory = setupCategory;
  }

  public String getQuoteStatus() {
    return quoteStatus;
  }

  public void setQuoteStatus(String quoteStatus) {
    this.quoteStatus = quoteStatus;
  }

  public String getTurnoverQuantity() {
    return turnoverQuantity;
  }

  public void setTurnoverQuantity(String turnoverQuantity) {
    this.turnoverQuantity = turnoverQuantity;
  }

  public String getAssigneeType() {
    return assigneeType;
  }

  public void setAssigneeType(String assigneeType) {
    this.assigneeType = assigneeType;
  }

  public int getContactCount() {
    return contactCount;
  }

  public void setContactCount(int contactCount) {
    this.contactCount = contactCount;
  }

  public long getProductNoteId() {
    return productNoteId;
  }

  public void setProductNoteId(long productNoteId) {
    this.productNoteId = productNoteId;
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
}
