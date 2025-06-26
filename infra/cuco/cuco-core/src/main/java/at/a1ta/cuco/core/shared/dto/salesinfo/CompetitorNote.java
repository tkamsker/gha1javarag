package at.a1ta.cuco.core.shared.dto.salesinfo;

import java.util.Date;

public class CompetitorNote extends SalesInfoNote {
  private String name;
  private String productGroupName;
  private String productName;
  private Date bindingDate;
  private Date reminderMailSentDate;

  /**
   * Copy Constructor
   * 
   * @param competitorNote a <code>CompetitorNote</code> object
   */
  public CompetitorNote(CompetitorNote competitorNote) {
    super(competitorNote);
    this.name = competitorNote.name;
    this.productGroupName = competitorNote.productGroupName;
    this.productName = competitorNote.productName;
    this.bindingDate = competitorNote.bindingDate;
    this.reminderMailSentDate = competitorNote.reminderMailSentDate;
  }
public CompetitorNote(){
super();}
  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getProductGroupName() {
    return productGroupName;
  }

  public void setProductGroupName(String productGroupName) {
    this.productGroupName = productGroupName;
  }

  public String getProductName() {
    return productName;
  }

  public void setProductName(String productName) {
    this.productName = productName;
  }

  public Date getBindingDate() {
    return bindingDate;
  }

  public void setBindingDate(Date bindingDate) {
    this.bindingDate = bindingDate;
  }

  public Date getReminderMailSentDate() {
    return reminderMailSentDate;
  }

  public void setReminderMailSentDate(Date reminderMailSentDate) {
    this.reminderMailSentDate = reminderMailSentDate;
  }

  @Override
  public String toString() {
    return "CompetitorNote [name=" + name + ", productGroupName=" + productGroupName + ", productName=" + productName + ", bindingDate=" + bindingDate + ", reminderMailSentDate=" + reminderMailSentDate + "]";
  }

}
