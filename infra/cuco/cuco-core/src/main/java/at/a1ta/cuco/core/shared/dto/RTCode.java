package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class RTCode implements Serializable {
  private String prodNum;
  private String description;
  private String sales;
  private Integer months;

  public String getDescription() {
    return description;
  }

  public String getProdNum() {
    return prodNum;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public void setProdNum(String prodNum) {
    this.prodNum = prodNum;
  }

  public String getSales() {
    return sales;
  }

  public void setSales(String sales) {
    this.sales = sales;
  }

  public Integer getMonths() {
    return months;
  }

  public void setMonths(Integer months) {
    this.months = months;
  }
}
