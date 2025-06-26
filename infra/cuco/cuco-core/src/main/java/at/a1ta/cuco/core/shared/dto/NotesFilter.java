package at.a1ta.cuco.core.shared.dto;

import java.util.Date;

import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;
import at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote.ToDoStatus;

public class NotesFilter {

  public static final String USER_ID = "USER_ID";
  public static final String LAST_MOD_DATE = "LAST_MOD_DATE";
  public static final String NOTE_TYPE = "NOTE_TYPE";
  public static final String NOTE_TEXT = "NOTE_TEXT";
  public static final String CREATOR = "CREATOR";
  public static final String LAST_MODIFIER = "LAST_MODIFIER";
  public static final String ASSIGNEE = "ASSIGNEE";
  public static final String REMINDER = "REMINDER";
  public static final String PARTY_ID = "PARTY_ID";
  public static final String FIRSTNAME = "FIRSTNAME";
  public static final String LASTNAME = "LASTNAME";
  public static final String STATUS = "STATUS";
  public static final String GROUP_NAME = "GROUP_NAME";
  public static final String GROUP_STATUS = "GROUP_STATUS";
  private long userId;
  private Date lastModDate;
  private SalesInfoNoteType noteType;
  private String noteText;
  private String status;
  private String creator;
  private String lastModifier;
  private String assignee;
  private String reminderOperator;
  private String partyId;
  private String firstname;
  private String lastname;
  private String groupName;
  private ToDoStatus groupStatus;

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

  public SalesInfoNoteType getNoteType() {
    return noteType;
  }

  public void setNoteType(SalesInfoNoteType noteType) {
    this.noteType = noteType;
  }

  public String getNoteText() {
    return noteText;
  }

  public void setNoteText(String noteText) {
    this.noteText = noteText;
  }

  public String getStatus() {
    return status;
  }

  public void setStatus(String status) {
    this.status = status;
  }

  public String getLastModifier() {
    return lastModifier;
  }

  public void setLastModifier(String lastModifier) {
    this.lastModifier = lastModifier;
  }

  public String getReminderOperator() {
    return reminderOperator;
  }

  public void setReminderOperator(String reminder) {
    this.reminderOperator = reminder;
  }

  public String getCreator() {
    return creator;
  }

  public void setCreator(String creator) {
    this.creator = creator;
  }

  public String getAssignee() {
    return assignee;
  }

  public void setAssignee(String assignee) {
    this.assignee = assignee;
  }

  public String getPartyId() {
    return partyId;
  }

  public void setPartyId(String partyId) {
    this.partyId = partyId;
  }

  public String getFirstname() {
    return firstname;
  }

  public void setFirstname(String firstname) {
    this.firstname = firstname;
  }

  public String getLastname() {
    return lastname;
  }

  public void setLastname(String lastname) {
    this.lastname = lastname;
  }

  public String getGroupName() {
    return groupName;
  }

  public void setGroupName(String groupName) {
    this.groupName = groupName;
  }

  public ToDoStatus getGroupStatus() {
    return groupStatus;
  }

  public void setGroupStatus(ToDoStatus groupStatus) {
    this.groupStatus = groupStatus;
  }

}
