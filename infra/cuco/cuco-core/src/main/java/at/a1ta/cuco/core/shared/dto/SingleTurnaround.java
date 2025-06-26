package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

public class SingleTurnaround implements Serializable {
  private long customerId;
  private RTCode rtCode;
  private Date date;
  private double amount;

  public long getCustomerId() {
    return customerId;
  }

  public void setCustomerId(long customerId) {
    this.customerId = customerId;
  }

  public RTCode getRtCode() {
    return rtCode;
  }

  public void setRtCode(RTCode rtCode) {
    this.rtCode = rtCode;
  }

  public Date getDate() {
    return date;
  }

  public void setDate(Date date) {
    this.date = date;
  }

  public double getAmount() {
    return amount;
  }

  public void setAmount(double amount) {
    this.amount = amount;
  }
}
