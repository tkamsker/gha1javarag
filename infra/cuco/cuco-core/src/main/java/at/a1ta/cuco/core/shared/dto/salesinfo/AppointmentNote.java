package at.a1ta.cuco.core.shared.dto.salesinfo;

import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.CommunicationChannel;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.CommunicationType;
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.ContactType;

@SuppressWarnings("serial")
public class AppointmentNote extends SalesInfoNote {
  private CommunicationType communicationType;
  private CommunicationChannel communicationChannel;
  private ContactType contactType;

  /**
   * Copy Constructor
   * 
   * @param appointmentNote a <code>AppointmentNote</code> object
   */
  public AppointmentNote(AppointmentNote appointmentNote) {
    super(appointmentNote);
    this.setSalesInfoNoteType(SalesInfoNoteType.SI_APPOINTMENT_NOTE);
    this.communicationType = appointmentNote.communicationType;
    this.communicationChannel = appointmentNote.communicationChannel;
    this.contactType = appointmentNote.contactType;
  }

  public AppointmentNote() {
    super();
    this.setSalesInfoNoteType(SalesInfoNoteType.SI_APPOINTMENT_NOTE);
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

  /**
   * Constructs a <code>String</code> with all attributes
   * in name = value format.
   * 
   * @return a <code>String</code> representation
   *         of this object.
   */
  @Override
  public String toString() {
    final String TAB = "    ";

    String retValue = "";

    retValue = "AppointmentNote ( " + super.toString() + TAB + "communicationType = " + this.communicationType + TAB
        + "communicationChannel = " + this.communicationChannel + TAB + "contactType = " + this.contactType + TAB + " )";

    return retValue;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = super.hashCode();
    result = prime * result + ((communicationChannel == null) ? 0 : communicationChannel.hashCode());
    result = prime * result + ((communicationType == null) ? 0 : communicationType.hashCode());
    result = prime * result + ((contactType == null) ? 0 : contactType.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) return true;
    if (!super.equals(obj)) return false;
    if (getClass() != obj.getClass()) return false;
    AppointmentNote other = (AppointmentNote) obj;
    if (communicationChannel != other.communicationChannel) return false;
    if (communicationType != other.communicationType) return false;
    if (contactType != other.contactType) return false;
    return true;
  }

}
