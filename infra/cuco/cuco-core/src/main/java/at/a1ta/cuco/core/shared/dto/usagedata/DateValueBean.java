package at.a1ta.cuco.core.shared.dto.usagedata;

import java.io.Serializable;
import java.util.Date;

public class DateValueBean implements Serializable {

  private Date date;
  private Double value;

  public DateValueBean() {}

  public DateValueBean(Date date, Double value) {
    this.date = date;
    this.value = value;
  }

  public Date getDate() {
    return date;
  }

  public void setDate(Date date) {
    this.date = date;
  }

  public Double getValue() {
    return value;
  }

  public void setValue(Double value) {
    this.value = value;
  }

}