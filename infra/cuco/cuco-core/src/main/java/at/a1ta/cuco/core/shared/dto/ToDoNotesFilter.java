package at.a1ta.cuco.core.shared.dto;

import java.util.Date;

import at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote.ToDoStatus;

public class ToDoNotesFilter {

  public static final String USER_ID = "USER_ID";
  public static final String LAST_MOD_DATE = "LAST_MOD_DATE";
  public static final String CREATE_DATE = "CREATE_DATE";
  public static final String GROUP_NAME = "GROUP_NAME";
  public static final String PARENT_SBS_NOTE = "PARENT_SBS_NOTE";
  public static final String PARTY_ID = "PARTY_ID";
  public static final String GROUP_STATUS = "GROUP_STATUS";
  public static final String EDIT_TODO = "EDIT_TODO";
  private long userId;
  private Date lastModDate;
  private Date createDate;
  private String groupName;
  private String ParentSbsNote;
  private String partyId;
  private ToDoStatus groupStatus;

  public Date getCreateDate() {
    return createDate;
  }

  public void setCreateDate(Date createDate) {
    this.createDate = createDate;
  }

  public String getGroupName() {
    return groupName;
  }

  public void setGroupName(String groupName) {
    this.groupName = groupName;
  }

  public String getParentSbsNote() {
    return ParentSbsNote;
  }

  public void setParentSbsNote(String parentSbsNote) {
    ParentSbsNote = parentSbsNote;
  }

  public long getUserId() {
    return userId;
  }

  public void setUserId(long userId) {
    this.userId = userId;
  }

  public Date getLastModDate() {
    return lastModDate;
  }

  public void setLastModDate(Date lastModDate) {
    this.lastModDate = lastModDate;
  }

  public String getPartyId() {
    return partyId;
  }

  public void setPartyId(String partyId) {
    this.partyId = partyId;
  }

  public ToDoStatus getGroupStatus() {
    return groupStatus;
  }

  public void setGroupStatus(ToDoStatus groupStatus) {
    this.groupStatus = groupStatus;
  }

}
