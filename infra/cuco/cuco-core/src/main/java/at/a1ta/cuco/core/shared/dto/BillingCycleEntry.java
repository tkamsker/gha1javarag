package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

public class BillingCycleEntry implements Serializable {
  private Long id;
  private String vBlock;
  private int column;
  private String step;
  private Date from;
  private Date to;
  private Date hr;

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getvBlock() {
    return vBlock;
  }

  public void setvBlock(String vBlock) {
    this.vBlock = vBlock;
  }

  public int getColumn() {
    return column;
  }

  public void setColumn(int column) {
    this.column = column;
  }

  public String getStep() {
    return step;
  }

  public void setStep(String step) {
    this.step = step;
  }

  public Date getFrom() {
    return from;
  }

  public void setFrom(Date from) {
    this.from = from;
  }

  public Date getTo() {
    return to;
  }

  public void setTo(Date to) {
    this.to = to;
  }

  public Date getHr() {
    return hr;
  }

  public void setHr(Date hr) {
    this.hr = hr;
  }
}
