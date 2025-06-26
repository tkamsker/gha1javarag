package at.a1ta.cuco.core.shared.dto.salesinfo;

import java.util.ArrayList;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.PointOfSaleInfo;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProductNote;

// this relates to Abwicklungsauftrag
@SuppressWarnings("serial")
public class ToDoGroupNote extends SalesInfoNote {
  public enum ToDoStatus {
    CREATED, ASSIGNED, ACCEPTED, INPROGRESS, DONE
  };

  private String toDoGroupName;
  private ToDoStatus toDoGroupStatus = ToDoStatus.CREATED;
  private String creatorNotes;
  private String assigneeNotes;
  private ArrayList<SBSProductNote> relatedNotes = new ArrayList<SBSProductNote>();
  private ArrayList<Attribute> attributes = new ArrayList<Attribute>();
  private BiteUser assignedToUser;
  private String assigneeDealerId = "";
  private String emailAdditionalText = "";
  private PointOfSaleInfo assignedToDelearInfo;
  private boolean sendAssignmentEmail = false;
  private boolean sendCompletionEmail = false;

  public ToDoGroupNote() {
    super();
    this.setSalesInfoNoteType(SalesInfoNoteType.SI_TODO_GROUP_NOTE);
  }

  public String getToDoGroupName() {
    return toDoGroupName;
  }

  public void setToDoGroupName(String toDoGroupName) {
    this.toDoGroupName = toDoGroupName;
  }

  public ToDoStatus getToDoGroupstatus() {
    return toDoGroupStatus;
  }

  public void setToDoGroupstatus(ToDoStatus toDoGroupstatus) {
    this.toDoGroupStatus = toDoGroupstatus;
  }

  public String getCreatorNote() {
    return creatorNotes;
  }

  public void setCreatorNote(String creatorNote) {
    this.creatorNotes = creatorNote;
  }

  public String getAssigneeNotes() {
    return assigneeNotes;
  }

  public void setAssigneeNotes(String assigneeNotes) {
    this.assigneeNotes = assigneeNotes;
  }

  public ArrayList<SBSProductNote> getRelatedNotes() {
    return relatedNotes;
  }

  public void setRelatedNotes(ArrayList<SBSProductNote> relatedNotes) {
    this.relatedNotes = relatedNotes;
  }

  public ArrayList<Attribute> getAttributes() {
    return attributes;
  }

  public void setAttributes(ArrayList<Attribute> attributes) {
    this.attributes = attributes;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = super.hashCode();
    result = prime * result + ((assignedToUser == null) ? 0 : assignedToUser.hashCode());
    result = prime * result + ((assigneeDealerId == null) ? 0 : assigneeDealerId.hashCode());
    result = prime * result + ((assigneeNotes == null) ? 0 : assigneeNotes.hashCode());
    result = prime * result + ((attributes == null) ? 0 : attributes.hashCode());
    result = prime * result + ((creatorNotes == null) ? 0 : creatorNotes.hashCode());
    result = prime * result + ((emailAdditionalText == null) ? 0 : emailAdditionalText.hashCode());
    result = prime * result + ((relatedNotes == null) ? 0 : relatedNotes.hashCode());
    result = prime * result + ((toDoGroupName == null) ? 0 : toDoGroupName.hashCode());
    result = prime * result + ((toDoGroupStatus == null) ? 0 : toDoGroupStatus.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) return true;
    if (!super.equals(obj)) return false;
    if (getClass() != obj.getClass()) return false;
    ToDoGroupNote other = (ToDoGroupNote) obj;
    if (assignedToUser == null) {
      if (other.assignedToUser != null) return false;
    } else if (!assignedToUser.equals(other.assignedToUser)) return false;
    if (assigneeDealerId == null) {
      if (other.assigneeDealerId != null) return false;
    } else if (!assigneeDealerId.equals(other.assigneeDealerId)) return false;
    if (assigneeNotes == null) {
      if (other.assigneeNotes != null) return false;
    } else if (!assigneeNotes.equals(other.assigneeNotes)) return false;
    if (attributes == null) {
      if (other.attributes != null) return false;
    } else if (!attributes.equals(other.attributes)) return false;
    if (creatorNotes == null) {
      if (other.creatorNotes != null) return false;
    } else if (!creatorNotes.equals(other.creatorNotes)) return false;
    if (emailAdditionalText == null) {
      if (other.emailAdditionalText != null) return false;
    } else if (!emailAdditionalText.equals(other.emailAdditionalText)) return false;
    if (relatedNotes == null) {
      if (other.relatedNotes != null) return false;
    } else if (!relatedNotes.equals(other.relatedNotes)) return false;
    if (toDoGroupName == null) {
      if (other.toDoGroupName != null) return false;
    } else if (!toDoGroupName.equals(other.toDoGroupName)) return false;
    if (toDoGroupStatus != other.toDoGroupStatus) return false;
    return true;
  }

  @Override
  public String toString() {
    return "ToDoGroupNote [toDoGroupName=" + toDoGroupName + ", toDoGroupStatus=" + toDoGroupStatus + ", creatorNotes=" + creatorNotes + ", assigneeNotes=" + assigneeNotes + ", relatedNotes="
        + relatedNotes + ", attributes=" + attributes + ", assignedToUser=" + assignedToUser + ", assigneeDealerId=" + assigneeDealerId + ", emailAdditionalText=" + emailAdditionalText + "]";
  }

  public BiteUser getAssignedToUser() {
    return assignedToUser;
  }

  public void setAssignedToUser(BiteUser assignedToUser) {
    this.assignedToUser = assignedToUser;
  }

  public String getEmailAdditionalText() {
    return emailAdditionalText;
  }

  public void setEmailAdditionalText(String emailAdditionalText) {
    this.emailAdditionalText = emailAdditionalText;
  }

  public String getAssigneeDealerId() {
    return assigneeDealerId;
  }

  public void setAssigneeDealerId(String assigneeDealerId) {
    this.assigneeDealerId = assigneeDealerId;
  }

  public PointOfSaleInfo getAssignedToDelearInfo() {
    return assignedToDelearInfo;
  }

  public void setAssignedToDelearInfo(PointOfSaleInfo assignedToDelearInfo) {
    this.assignedToDelearInfo = assignedToDelearInfo;
  }

  public boolean isSendAssignmentEmail() {
    return sendAssignmentEmail;
  }

  public void setSendAssignmentEmail(boolean sendAssignmentEmail) {
    this.sendAssignmentEmail = sendAssignmentEmail;
  }

  public boolean isSendCompletionEmail() {
    return sendCompletionEmail;
  }

  public void setSendCompletionEmail(boolean sendCompletionEmail) {
    this.sendCompletionEmail = sendCompletionEmail;
  }

  public boolean isToDoCompleted() {
    if (getAttributes() == null) {
      return false;
    }
    boolean allToDosCompleted = true;
    for (Attribute attrib : getAttributes()) {
      if (!attrib.getNSBooleanValue()) {
        allToDosCompleted = false;
        break;
      }
    }
    return allToDosCompleted;
  }

  public boolean isToDoInProgress() {
    if (getAttributes() == null) {
      return false;
    }
    boolean anyToDoCompleted = false;
    boolean allToDosCompleted = true;
    for (Attribute attrib : getAttributes()) {
      if (attrib.getNSBooleanValue()) {
        anyToDoCompleted = true;
      } else {
        allToDosCompleted = false;
      }
    }
    return !allToDosCompleted && anyToDoCompleted;
  }

}
