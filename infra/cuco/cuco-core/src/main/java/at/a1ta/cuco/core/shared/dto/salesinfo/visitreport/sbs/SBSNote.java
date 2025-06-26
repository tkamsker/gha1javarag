package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.ContactPerson;
import at.a1ta.cuco.core.shared.dto.salesinfo.AppointmentNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.ToDoGroupNote.ToDoStatus;

public class SBSNote extends SalesInfoNote {
  private static final long serialVersionUID = 1L;
  private CommunicationType communicationType;
  private CommunicationChannel communicationChannel;
  private ContactType contactType;
  private ContactSource contactSource;

  private ContactPerson contactPerson;

  private List<SBSProductNote> productNotes;
  private List<SalesInfoNote> tasks;
  private List<AppointmentNote> appointments = new ArrayList<AppointmentNote>();

  private List<Attribute> feedbackAttributes;
  private String feedbackText;
  private List<Attribute> reflectionAttributes;
  private String reflectionText;

  private List<ContactPerson> availableContactPersons = new ArrayList<ContactPerson>();
  private List<ToDoGroupNote> productNoteGroups = new ArrayList<ToDoGroupNote>();

  private SBSNote savedInstance;

  public SBSNote() {
    super();
  }

  /**
   * Copy Constructor
   * 
   * @param sBSNote a <code>SBSNote</code> object
   */
  public SBSNote(SBSNote sBSNote) {
    super(sBSNote);
    this.communicationType = sBSNote.communicationType;
    this.communicationChannel = sBSNote.communicationChannel;
    this.contactType = sBSNote.contactType;
    this.contactSource = sBSNote.contactSource;
    this.contactPerson = sBSNote.contactPerson;
    this.productNotes = sBSNote.productNotes;
    this.tasks = sBSNote.tasks;
    this.appointments = sBSNote.appointments;
    this.feedbackAttributes = sBSNote.feedbackAttributes;
    this.feedbackText = sBSNote.feedbackText;
    this.reflectionAttributes = sBSNote.reflectionAttributes;
    this.reflectionText = sBSNote.reflectionText;
  }

  public CommunicationType getCommunicationType() {
    return communicationType;
  }

  public void setCommunicationType(CommunicationType communicationType) {
    this.communicationType = communicationType;
  }

  public CommunicationChannel getCommunicationChannel() {
    return communicationChannel;
  }

  public void setCommunicationChannel(CommunicationChannel communicationChannel) {
    this.communicationChannel = communicationChannel;
  }

  public ContactType getContactType() {
    return contactType;
  }

  public void setContactType(ContactType contactType) {
    this.contactType = contactType;
  }

  public List<SBSProductNote> getProductNotes() {
    return productNotes;
  }

  public void setProductNotes(List<SBSProductNote> productNotes) {
    this.productNotes = productNotes;
  }

  public List<SalesInfoNote> getTasks() {
    return tasks;
  }

  public void setTasks(List<SalesInfoNote> tasks) {
    this.tasks = tasks;
  }

  public List<Attribute> getFeedbackAttributes() {
    return feedbackAttributes;
  }

  public void setFeedbackAttributes(List<Attribute> feedbackAttributes) {
    this.feedbackAttributes = feedbackAttributes;
  }

  public String getFeedbackText() {
    return feedbackText;
  }

  public void setFeedbackText(String feedbackText) {
    this.feedbackText = feedbackText;
  }

  public List<Attribute> getReflectionAttributes() {
    return reflectionAttributes;
  }

  public void setReflectionAttributes(List<Attribute> reflectionAttributes) {
    this.reflectionAttributes = reflectionAttributes;
  }

  public String getReflectionText() {
    return reflectionText;
  }

  public void setReflectionText(String reflectionText) {
    this.reflectionText = reflectionText;
  }

  public ContactSource getContactSource() {
    return contactSource;
  }

  public void setContactSource(ContactSource contactSource) {
    this.contactSource = contactSource;
  }

  public ContactPerson getContactPerson() {
    return contactPerson;
  }

  public void setContactPerson(ContactPerson contactPerson) {
    this.contactPerson = contactPerson;
  }

  @Override
  public String toString() {
    return "SBSNote [communicationType=" + communicationType + ", communicationChannel=" + communicationChannel + ", contactType=" + contactType + ", contactSource=" + contactSource
        + ", productNotes=" + productNotes + ", tasks=" + tasks + ", appointments=" + appointments + ", feedbackAttributes=" + feedbackAttributes + ", feedbackText=" + feedbackText
        + ", reflectionAttributes=" + reflectionAttributes + ", reflectionText=" + reflectionText + super.toString() + "]";
  }

  public List<AppointmentNote> getAppointments() {
    return appointments;
  }

  public void setAppointments(List<AppointmentNote> appointments) {
    this.appointments = appointments;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = super.hashCode();
    result = prime * result + ((appointments == null) ? 0 : appointments.hashCode());
    result = prime * result + ((availableContactPersons == null) ? 0 : availableContactPersons.hashCode());
    result = prime * result + ((communicationChannel == null) ? 0 : communicationChannel.hashCode());
    result = prime * result + ((communicationType == null) ? 0 : communicationType.hashCode());
    result = prime * result + ((contactPerson == null) ? 0 : contactPerson.hashCode());
    result = prime * result + ((contactSource == null) ? 0 : contactSource.hashCode());
    result = prime * result + ((contactType == null) ? 0 : contactType.hashCode());
    result = prime * result + ((feedbackAttributes == null) ? 0 : feedbackAttributes.hashCode());
    result = prime * result + ((feedbackText == null) ? 0 : feedbackText.hashCode());
    result = prime * result + ((productNoteGroups == null) ? 0 : productNoteGroups.hashCode());
    result = prime * result + ((productNotes == null) ? 0 : productNotes.hashCode());
    result = prime * result + ((reflectionAttributes == null) ? 0 : reflectionAttributes.hashCode());
    result = prime * result + ((reflectionText == null) ? 0 : reflectionText.hashCode());
    result = prime * result + ((tasks == null) ? 0 : tasks.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (!super.equals(obj)) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    SBSNote other = (SBSNote) obj;
    if (appointments == null) {
      if (other.appointments != null) {
        return false;
      }
    } else if (!appointments.equals(other.appointments)) {
      return false;
    }
    if (availableContactPersons == null) {
      if (other.availableContactPersons != null) {
        return false;
      }
    } else if (!availableContactPersons.equals(other.availableContactPersons)) {
      return false;
    }
    if (communicationChannel != other.communicationChannel) {
      return false;
    }
    if (communicationType != other.communicationType) {
      return false;
    }
    if (contactPerson == null) {
      if (other.contactPerson != null) {
        return false;
      }
    } else if (!contactPerson.equals(other.contactPerson)) {
      return false;
    }
    if (contactSource != other.contactSource) {
      return false;
    }
    if (contactType != other.contactType) {
      return false;
    }
    if (feedbackAttributes == null) {
      if (other.feedbackAttributes != null) {
        return false;
      }
    } else if (!feedbackAttributes.equals(other.feedbackAttributes)) {
      return false;
    }
    if (feedbackText == null) {
      if (other.feedbackText != null) {
        return false;
      }
    } else if (!feedbackText.equals(other.feedbackText)) {
      return false;
    }
    if (productNoteGroups == null) {
      if (other.productNoteGroups != null) {
        return false;
      }
    } else if (!productNoteGroups.equals(other.productNoteGroups)) {
      return false;
    }
    if (productNotes == null) {
      if (other.productNotes != null) {
        return false;
      }
    } else if (!productNotes.equals(other.productNotes)) {
      return false;
    }
    if (reflectionAttributes == null) {
      if (other.reflectionAttributes != null) {
        return false;
      }
    } else if (!reflectionAttributes.equals(other.reflectionAttributes)) {
      return false;
    }
    if (reflectionText == null) {
      if (other.reflectionText != null) {
        return false;
      }
    } else if (!reflectionText.equals(other.reflectionText)) {
      return false;
    }
    if (tasks == null) {
      if (other.tasks != null) {
        return false;
      }
    } else if (!tasks.equals(other.tasks)) {
      return false;
    }
    return true;
  }

  public boolean equalsUIEditableAttributes(Object obj) {
    if (this == obj) {
      return true;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    SBSNote other = (SBSNote) obj;

    if (getNoteText() == null || getNoteText().isEmpty()) {
      if (other.getNoteText() != null && !other.getNoteText().isEmpty()) {
        return false;
      }
    } else if (!getNoteText().equals(other.getNoteText())) {
      return false;
    }
    if (getSalesInfoNoteId() != other.getSalesInfoNoteId()) {
      return false;
    }
    if (getSalesInfoNoteType() != other.getSalesInfoNoteType()) {
      return false;
    }
    if (getStatus() == null) {
      if (other.getStatus() != null) {
        return false;
      }
    } else if (!getStatus().equals(other.getStatus())) {
      return false;
    }
    if (getTask() == null) {
      if (other.getTask() != null) {
        return false;
      }
    } else if (!getTask().equals(other.getTask())) {
      return false;
    }

    if (communicationChannel != other.communicationChannel) {
      return false;
    }
    if (communicationType != other.communicationType) {
      return false;
    }
    if (contactPerson == null) {
      if (other.contactPerson != null) {
        return false;
      }
    } else if (!contactPerson.equals(other.contactPerson)) {
      return false;
    }
    if (contactSource != other.contactSource) {
      return false;
    }
    if (contactType != other.contactType) {
      return false;
    }
    if (feedbackAttributes == null) {
      if (other.feedbackAttributes != null) {
        return false;
      }
    } else if (!feedbackAttributes.equals(other.feedbackAttributes)) {
      return false;
    }
    if (feedbackText == null || feedbackText.isEmpty()) {
      if (other.feedbackText != null && !other.feedbackText.isEmpty()) {
        return false;
      }
    } else if (!feedbackText.equals(other.feedbackText)) {
      return false;
    }
    if (reflectionAttributes == null) {
      if (other.reflectionAttributes != null) {
        return false;
      }
    } else if (!reflectionAttributes.equals(other.reflectionAttributes)) {
      return false;
    }
    if (reflectionText == null || reflectionText.isEmpty()) {
      if (other.reflectionText != null && !other.reflectionText.isEmpty()) {
        return false;
      }
    } else if (!reflectionText.equals(other.reflectionText)) {
      return false;
    }

    return true;
  }

  public List<ContactPerson> getAvailableContactPersons() {
    return availableContactPersons;
  }

  public void setAvailableContactPersons(List<ContactPerson> availableContactPersons) {
    this.availableContactPersons = availableContactPersons;
  }

  public List<ToDoGroupNote> getProductNoteGroups() {
    return productNoteGroups;
  }

  public void setProductNoteGroups(List<ToDoGroupNote> productNoteGroups) {
    this.productNoteGroups = productNoteGroups;
  }

  public SBSNote getSavedInstance() {
    if (savedInstance == null) {
      return new SBSNote(this);
    }
    return savedInstance;
  }

  public void setSavedInstance(SBSNote savedInstance) {
    this.savedInstance = savedInstance;
  }

  public boolean hasAnyOpenProductNote() {
    if (getProductNotes() == null || getProductNotes().isEmpty()) {
      return false;
    }
    for (SBSProductNote note : getProductNotes()) {
      if (note.getQuoteStatus() != QuoteStatus.ACCEPTED && note.getQuoteStatus() != QuoteStatus.DECLINED && note.getQuoteStatus() != QuoteStatus.OBSOLETE) {
        return true;
      }
    }
    return false;
  }

  public boolean hasAnyOpenToDos() {
    if (getProductNoteGroups() == null || getProductNoteGroups().isEmpty()) {
      return false;
    }

    for (ToDoGroupNote note : getProductNoteGroups()) {
      if (note.getToDoGroupstatus() != ToDoStatus.DONE) {
        return true;
      }
    }
    return false;
  }

}
