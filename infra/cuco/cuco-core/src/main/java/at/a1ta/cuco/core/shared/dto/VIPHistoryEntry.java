package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

public class VIPHistoryEntry implements Serializable {
  private Long vipHistoryId;
  private Long customerId;
  private Date created;
  private Long userId;
  private String name;
  private String reported;
  private Integer oldStatus;
  private Integer newStatus;

  public Long getVipHistoryId() {
    return vipHistoryId;
  }

  public void setVipHistoryId(Long vipHistoryId) {
    this.vipHistoryId = vipHistoryId;
  }

  public Long getCustomerId() {
    return customerId;
  }

  public void setCustomerId(Long customerId) {
    this.customerId = customerId;
  }

  public Date getCreated() {
    return created;
  }

  public void setCreated(Date created) {
    this.created = created;
  }

  public Long getUserId() {
    return userId;
  }

  public void setUserId(Long userId) {
    this.userId = userId;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getReported() {
    return reported;
  }

  public void setReported(String reported) {
    this.reported = reported;
  }

  public Integer getOldStatus() {
    return oldStatus;
  }

  public void setOldStatus(Integer oldStatus) {
    this.oldStatus = oldStatus;
  }

  public Integer getNewStatus() {
    return newStatus;
  }

  public void setNewStatus(Integer newStatus) {
    this.newStatus = newStatus;
  }

}
