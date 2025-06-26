package at.a1ta.cuco.core.shared.dto.salesinfo;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.UserInfo;

public class SalesInfoNoteHistory implements Serializable {
  private long salesInfoNoteId;
  private Date modificationTimestamp;
  private UserInfo modificationUser;
  private SalesInfoNoteHistoryModificationType modificationType;
  private Long predecessorSalesInfoNoteId; // only filled out when modificationType == CREATED_BY_PREDECESSOR
  private Long followerSalesInfoNoteId; // only filled out when modificationType == FOLLOWER_CREATED

  public SalesInfoNoteHistory() {}

  public SalesInfoNoteHistory(long salesInfoNoteId, Date modificationTimestamp, UserInfo modificationUser, SalesInfoNoteHistoryModificationType modificationType, Long predecessorSalesInfoNoteId, Long followerSalesInfoNoteId) {
    this.salesInfoNoteId = salesInfoNoteId;
    this.modificationTimestamp = modificationTimestamp;
    this.modificationUser = modificationUser;
    this.modificationType = modificationType;
    this.predecessorSalesInfoNoteId = predecessorSalesInfoNoteId;
    this.followerSalesInfoNoteId = followerSalesInfoNoteId;
  }

  public long getSalesInfoNoteId() {
    return salesInfoNoteId;
  }

  public void setSalesInfoNoteId(long salesInfoNoteId) {
    this.salesInfoNoteId = salesInfoNoteId;
  }

  public Date getModificationTimestamp() {
    return modificationTimestamp;
  }

  public void setModificationTimestamp(Date modificationTimestamp) {
    this.modificationTimestamp = modificationTimestamp;
  }

  public UserInfo getModificationUser() {
    return modificationUser;
  }

  public void setModificationUser(UserInfo modificationUser) {
    this.modificationUser = modificationUser;
  }

  public SalesInfoNoteHistoryModificationType getModificationType() {
    return modificationType;
  }

  public void setModificationType(SalesInfoNoteHistoryModificationType modificationType) {
    this.modificationType = modificationType;
  }

  public Long getPredecessorSalesInfoNoteId() {
    return predecessorSalesInfoNoteId;
  }

  public void setPredecessorSalesInfoNoteId(Long predecessorSalesInfoNoteId) {
    this.predecessorSalesInfoNoteId = predecessorSalesInfoNoteId;
  }

  public Long getFollowerSalesInfoNoteId() {
    return followerSalesInfoNoteId;
  }

  public void setFollowerSalesInfoNoteId(Long followerSalesInfoNoteId) {
    this.followerSalesInfoNoteId = followerSalesInfoNoteId;
  }

  @Override
  public String toString() {
    return "SalesInfoNoteHistory [salesInfoNoteId=" + salesInfoNoteId + ", modificationTimestamp=" + modificationTimestamp + ", modificationUser=" + modificationUser + ", modificationType=" + modificationType + ", predecessorSalesInfoNoteId=" + predecessorSalesInfoNoteId + ", followerSalesInfoNoteId=" + followerSalesInfoNoteId + "]";
  }
}
