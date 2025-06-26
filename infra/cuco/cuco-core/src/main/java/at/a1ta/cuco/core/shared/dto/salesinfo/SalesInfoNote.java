package at.a1ta.cuco.core.shared.dto.salesinfo;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.shared.dto.Party;

@XmlAccessorType(XmlAccessType.NONE)
public class SalesInfoNote extends SalesInfoOverviewRow {
  private static final long serialVersionUID = 1L;

  public SalesInfoNote() {
    super();
  }

  /**
   * Copy Constructor
   * 
   * @param salesInfoNote a <code>SalesInfoNote</code> object
   */
  public SalesInfoNote(SalesInfoNote salesInfoNote) {
    super(salesInfoNote);
    this.salesInfoNoteId = salesInfoNote.salesInfoNoteId;
    this.salesInfoNoteType = salesInfoNote.salesInfoNoteType;
    this.predecessorSalesInfoNoteId = salesInfoNote.predecessorSalesInfoNoteId;
    this.partyId = salesInfoNote.partyId;
    this.party = salesInfoNote.party;
    this.noteText = salesInfoNote.noteText;
    this.status = salesInfoNote.status;
    this.task = salesInfoNote.task;
    this.creationUser = salesInfoNote.creationUser;
    this.creationTimestamp = salesInfoNote.creationTimestamp;
    this.lastModificationUser = salesInfoNote.lastModificationUser;
    this.lastModificationTimestamp = salesInfoNote.lastModificationTimestamp;
    this.deleted = salesInfoNote.deleted;
    this.finalized = salesInfoNote.finalized;
    this.historyNotes = salesInfoNote.historyNotes;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = super.hashCode();
    result = prime * result + ((creationTimestamp == null) ? 0 : creationTimestamp.hashCode());
    result = prime * result + ((creationUser == null) ? 0 : creationUser.hashCode());
    result = prime * result + (deleted ? 1231 : 1237);
    result = prime * result + ((historyNotes == null) ? 0 : historyNotes.hashCode());
    result = prime * result + ((lastModificationTimestamp == null) ? 0 : lastModificationTimestamp.hashCode());
    result = prime * result + ((lastModificationUser == null) ? 0 : lastModificationUser.hashCode());
    result = prime * result + ((noteText == null) ? 0 : noteText.hashCode());
    result = prime * result + ((party == null) ? 0 : party.hashCode());
    result = prime * result + (int) (partyId ^ (partyId >>> 32));
    result = prime * result + ((predecessorSalesInfoNoteId == null) ? 0 : predecessorSalesInfoNoteId.hashCode());
    result = prime * result + (int) (salesInfoNoteId ^ (salesInfoNoteId >>> 32));
    result = prime * result + ((salesInfoNoteType == null) ? 0 : salesInfoNoteType.hashCode());
    result = prime * result + ((status == null) ? 0 : status.hashCode());
    result = prime * result + ((task == null) ? 0 : task.hashCode());
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
    SalesInfoNote other = (SalesInfoNote) obj;
    if (creationTimestamp == null) {
      if (other.creationTimestamp != null) {
        return false;
      }
    } else if (!creationTimestamp.equals(other.creationTimestamp)) {
      return false;
    }
    if (creationUser == null) {
      if (other.creationUser != null) {
        return false;
      }
    } else if (!creationUser.equals(other.creationUser)) {
      return false;
    }
    if (deleted != other.deleted) {
      return false;
    }
    if (finalized != other.finalized) {
      return false;
    }
    if (historyNotes == null) {
      if (other.historyNotes != null) {
        return false;
      }
    } else if (!historyNotes.equals(other.historyNotes)) {
      return false;
    }
    if (lastModificationTimestamp == null) {
      if (other.lastModificationTimestamp != null) {
        return false;
      }
    } else if (!lastModificationTimestamp.equals(other.lastModificationTimestamp)) {
      return false;
    }
    if (lastModificationUser == null) {
      if (other.lastModificationUser != null) {
        return false;
      }
    } else if (!lastModificationUser.equals(other.lastModificationUser)) {
      return false;
    }
    if (noteText == null) {
      if (other.noteText != null) {
        return false;
      }
    } else if (!noteText.equals(other.noteText)) {
      return false;
    }
    if (party == null) {
      if (other.party != null) {
        return false;
      }
    } else if (!party.equals(other.party)) {
      return false;
    }
    if (partyId != other.partyId) {
      return false;
    }
    if (predecessorSalesInfoNoteId == null) {
      if (other.predecessorSalesInfoNoteId != null) {
        return false;
      }
    } else if (!predecessorSalesInfoNoteId.equals(other.predecessorSalesInfoNoteId)) {
      return false;
    }
    if (salesInfoNoteId != other.salesInfoNoteId) {
      return false;
    }
    if (salesInfoNoteType != other.salesInfoNoteType) {
      return false;
    }
    if (status == null) {
      if (other.status != null) {
        return false;
      }
    } else if (!status.equals(other.status)) {
      return false;
    }
    if (task == null) {
      if (other.task != null) {
        return false;
      }
    } else if (!task.equals(other.task)) {
      return false;
    }
    return true;
  }

  public enum SalesInfoNoteType {
    SI_HISTORY_NOTE, SI_SIMPLE_NOTE, SI_COMPETITOR_NOTE, SI_APPOINTMENT_NOTE, SI_VR_SBS_NOTE, SI_VR_SBS_PRODUCT_NOTE, SI_VR_GENERIC_NOTE, SI_VR_ANGEBOTE, SI_VR_DIGITAL_SELLING, SI_SALES_CONV_NOTE, SI_SALES_CONV_PRODUCT_NOTE, SI_TODO_GROUP_NOTE
  }

  private long salesInfoNoteId;
  private SalesInfoNoteType salesInfoNoteType;
  private Long predecessorSalesInfoNoteId;
  private long partyId;
  private Party party;
  private String noteText;
  private String status;
  private Task task;
  private BiteUser creationUser;
  private Date creationTimestamp;
  private BiteUser lastModificationUser;
  private Date lastModificationTimestamp;
  private boolean deleted;
  private boolean finalized;
  private List<HistoryNote> historyNotes = new ArrayList<HistoryNote>();

  public long getSalesInfoNoteId() {
    return salesInfoNoteId;
  }

  public void setSalesInfoNoteId(long salesInfoNoteId) {
    this.salesInfoNoteId = salesInfoNoteId;
  }

  public SalesInfoNoteType getSalesInfoNoteType() {
    return salesInfoNoteType;
  }

  public void setSalesInfoNoteType(SalesInfoNoteType salesInfoNoteType) {
    this.salesInfoNoteType = salesInfoNoteType;
  }

  public Long getPredecessorSalesInfoNoteId() {
    return predecessorSalesInfoNoteId;
  }

  public void setPredecessorSalesInfoNoteId(Long predecessorSalesInfoNoteId) {
    this.predecessorSalesInfoNoteId = predecessorSalesInfoNoteId;
  }

  public long getPartyId() {
    return partyId;
  }

  public void setPartyId(long partyId) {
    this.partyId = partyId;
  }

  public String getNoteText() {
    return noteText;
  }

  public void setNoteText(String noteText) {
    this.noteText = noteText;
  }

  public Task getTask() {
    return task;
  }

  public void setTask(Task task) {
    this.task = task;
  }

  public String getStatus() {
    return status;
  }

  public void setStatus(String status) {
    this.status = status;
  }

  public BiteUser getCreationUser() {
    return creationUser;
  }

  public void setCreationUser(BiteUser creationUser) {
    this.creationUser = creationUser;
  }

  public Date getCreationTimestamp() {
    return creationTimestamp;
  }

  public void setCreationTimestamp(Date creationTimestamp) {
    this.creationTimestamp = creationTimestamp;
  }

  public BiteUser getLastModificationUser() {
    return lastModificationUser;
  }

  public void setLastModificationUser(BiteUser lastModificationUser) {
    this.lastModificationUser = lastModificationUser;
  }

  public Date getLastModificationTimestamp() {
    return lastModificationTimestamp;
  }

  public void setLastModificationTimestamp(Date lastModificationTimestamp) {
    this.lastModificationTimestamp = lastModificationTimestamp;
  }

  public boolean isDeleted() {
    return deleted;
  }

  public void setDeleted(boolean deleted) {
    this.deleted = deleted;
  }

  @Override
  public Date getLastModDate() {
    return lastModificationTimestamp;
  }

  @Override
  public String toString() {
    return "SalesInfoNote [salesInfoNoteId=" + salesInfoNoteId + ", salesInfoNoteType=" + salesInfoNoteType + ", predecessorSalesInfoNoteId=" + predecessorSalesInfoNoteId + ", partyId=" + partyId
        + ", noteText=" + noteText + ", task=" + task + ", creationUser=" + creationUser + ", creationTimestamp=" + creationTimestamp + ", lastModificationUser=" + lastModificationUser
        + ", lastModificationTimestamp=" + lastModificationTimestamp + ", deleted=" + deleted + ",finalized=" + finalized + ", status=" + status + "]";
  }

  public Party getParty() {
    return party;
  }

  public void setParty(Party party) {
    this.party = party;
  }

  public List<HistoryNote> getHistoryNotes() {
    return historyNotes;
  }

  public void setHistoryNotes(List<HistoryNote> historyNotes) {
    this.historyNotes = historyNotes;
  }

  public boolean isFinalized() {
    return finalized;
  }

  public void setFinalized(boolean finalized) {
    this.finalized = finalized;
  }

}
