package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;
import java.util.List;

public class BillingCycle implements Serializable {
  private Date billingDate;
  private List<BillingCycleEntry> entries;

  public Date getBillingDate() {
    return billingDate;
  }

  public void setBillingDate(Date billingDate) {
    this.billingDate = billingDate;
  }

  public void setEntries(List<BillingCycleEntry> entries) {
    this.entries = entries;
  }

  public List<BillingCycleEntry> getEntries() {
    return entries;
  }
}
