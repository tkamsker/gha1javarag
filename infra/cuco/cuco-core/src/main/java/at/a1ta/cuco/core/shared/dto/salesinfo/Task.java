package at.a1ta.cuco.core.shared.dto.salesinfo;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.shared.dto.StandardAddress;

public class Task implements Serializable {
  private static final long serialVersionUID = 1L;

  /**
   * Copy Constructor
   * 
   * @param task a <code>Task</code> object
   */
  public Task(Task task) {
    this.taskId = task.taskId;
    this.active = task.active;
    this.status = task.status;
    this.type = task.type;
    this.assigneeUser = task.assigneeUser;
    this.startDate = task.startDate;
    this.endDate = task.endDate;
    this.sendReminderMail = task.sendReminderMail;
    this.sendVCalendarMail = task.sendVCalendarMail;
    this.address = task.address;
    this.reminderMailSentDate = task.reminderMailSentDate;
    this.vCalMailSentDate = task.vCalMailSentDate;
    this.vCalMailTo = task.vCalMailTo;
    this.vCalMailCC = task.vCalMailCC;
  }

  public Task() {
    // default constructor to support GWT parsing
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + (active ? 1231 : 1237);
    result = prime * result + ((address == null) ? 0 : address.hashCode());
    result = prime * result + ((assigneeUser == null) ? 0 : assigneeUser.hashCode());
    result = prime * result + ((endDate == null) ? 0 : endDate.hashCode());
    result = prime * result + ((reminderMailSentDate == null) ? 0 : reminderMailSentDate.hashCode());
    result = prime * result + (sendReminderMail ? 1231 : 1237);
    result = prime * result + (sendVCalendarMail ? 1231 : 1237);
    result = prime * result + ((startDate == null) ? 0 : startDate.hashCode());
    result = prime * result + ((status == null) ? 0 : status.hashCode());
    result = prime * result + (int) (taskId ^ (taskId >>> 32));
    result = prime * result + ((type == null) ? 0 : type.hashCode());
    result = prime * result + ((vCalMailCC == null) ? 0 : vCalMailCC.hashCode());
    result = prime * result + ((vCalMailSentDate == null) ? 0 : vCalMailSentDate.hashCode());
    result = prime * result + ((vCalMailTo == null) ? 0 : vCalMailTo.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (obj == null) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    Task other = (Task) obj;
    if (active != other.active) {
      return false;
    }
    if (address == null) {
      if (other.address != null) {
        return false;
      }
    } else if (!address.equals(other.address)) {
      return false;
    }
    if (assigneeUser == null) {
      if (other.assigneeUser != null) {
        return false;
      }
    } else if (!assigneeUser.equals(other.assigneeUser)) {
      return false;
    }
    if (endDate == null) {
      if (other.endDate != null) {
        return false;
      }
    } else if (!endDate.equals(other.endDate)) {
      return false;
    }
    if (reminderMailSentDate == null) {
      if (other.reminderMailSentDate != null) {
        return false;
      }
    } else if (!reminderMailSentDate.equals(other.reminderMailSentDate)) {
      return false;
    }
    if (sendReminderMail != other.sendReminderMail) {
      return false;
    }
    if (sendVCalendarMail != other.sendVCalendarMail) {
      return false;
    }
    if (startDate == null) {
      if (other.startDate != null) {
        return false;
      }
    } else if (!startDate.equals(other.startDate)) {
      return false;
    }
    if (status != other.status) {
      return false;
    }
    if (taskId != other.taskId) {
      return false;
    }
    if (type != other.type) {
      return false;
    }
    if (vCalMailCC == null) {
      if (other.vCalMailCC != null) {
        return false;
      }
    } else if (!vCalMailCC.equals(other.vCalMailCC)) {
      return false;
    }
    if (vCalMailSentDate == null) {
      if (other.vCalMailSentDate != null) {
        return false;
      }
    } else if (!vCalMailSentDate.equals(other.vCalMailSentDate)) {
      return false;
    }
    if (vCalMailTo == null) {
      if (other.vCalMailTo != null) {
        return false;
      }
    } else if (!vCalMailTo.equals(other.vCalMailTo)) {
      return false;
    }
    return true;
  }

  public enum TaskStatus {
    NONE, OPEN, WORKING, DONE, OBSOLESCED_BY_SUCCESSOR
  };

  public enum TaskType {
    NONE, CALL, QUOTE, INQUIRY, APPOINTMENT, SI_VR_SBS_PRODUCT_NOTE
  };

  private long taskId;
  private boolean active;
  private TaskStatus status;
  private TaskType type;
  private BiteUser assigneeUser;
  private Date startDate;
  private Date endDate;
  private boolean sendReminderMail;
  private boolean sendVCalendarMail;

  private StandardAddress address;

  private Date reminderMailSentDate;
  private Date vCalMailSentDate;
  private String vCalMailTo;
  private String vCalMailCC;

  public long getTaskId() {
    return taskId;
  }

  public void setTaskId(long taskId) {
    this.taskId = taskId;
  }

  public boolean isActive() {
    return active;
  }

  public void setActive(boolean active) {
    this.active = active;
  }

  public TaskStatus getStatus() {
    return status;
  }

  public void setStatus(TaskStatus status) {
    this.status = status;
  }

  public TaskType getType() {
    return type;
  }

  public void setType(TaskType type) {
    this.type = type;
  }

  public BiteUser getAssigneeUser() {
    return assigneeUser;
  }

  public void setAssigneeUser(BiteUser assigneeUser) {
    this.assigneeUser = assigneeUser;
  }

  public Date getStartDate() {
    return startDate;
  }

  public void setStartDate(Date startDate) {
    this.startDate = startDate;
  }

  public Date getEndDate() {
    return endDate;
  }

  public void setEndDate(Date endDate) {
    this.endDate = endDate;
  }

  public boolean isSendReminderMail() {
    return sendReminderMail;
  }

  public void setSendReminderMail(boolean sendReminderMail) {
    this.sendReminderMail = sendReminderMail;
  }

  public boolean isSendVCalendarMail() {
    return sendVCalendarMail;
  }

  public void setSendVCalendarMail(boolean sendVCalendarMail) {
    this.sendVCalendarMail = sendVCalendarMail;
  }

  public Date getReminderMailSentDate() {
    return reminderMailSentDate;
  }

  public void setReminderMailSentDate(Date reminderMailSentDate) {
    this.reminderMailSentDate = reminderMailSentDate;
  }

  public Date getvCalMailSentDate() {
    return vCalMailSentDate;
  }

  public void setvCalMailSentDate(Date vCalMailSentDate) {
    this.vCalMailSentDate = vCalMailSentDate;
  }

  @Override
  public String toString() {
    return "Task [taskId=" + taskId + ", active=" + active + ", status=" + status + ", type=" + type + ", assigneeUser=" + assigneeUser + ", startDate=" + startDate + ", endDate=" + endDate
        + ", sendReminderMail=" + sendReminderMail + ", sendVCalendarMail=" + sendVCalendarMail + "]";
  }

  public String getvCalMailTo() {
    return vCalMailTo;
  }

  public void setvCalMailTo(String vCalMailTo) {
    this.vCalMailTo = vCalMailTo;
  }

  public String getvCalMailCC() {
    return vCalMailCC;
  }

  public void setvCalMailCC(String vCalMailCC) {
    this.vCalMailCC = vCalMailCC;
  }

  public StandardAddress getAddress() {
    return address;
  }

  public void setAddress(StandardAddress address) {
    this.address = address;
  }

}
