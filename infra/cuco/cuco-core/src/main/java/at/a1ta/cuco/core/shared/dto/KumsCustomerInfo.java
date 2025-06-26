package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class KumsCustomerInfo implements Serializable {
  private Integer vipStatus;
  private String lastChangeDate;

  public Integer getVipStatus() {
    return vipStatus;
  }

  public void setVipStatus(Integer vipStatus) {
    this.vipStatus = vipStatus;
  }

  public String getLastChangeDate() {
    return lastChangeDate;
  }

  public void setLastChangeDate(String lastChangeDate) {
    this.lastChangeDate = lastChangeDate;
  }

}
