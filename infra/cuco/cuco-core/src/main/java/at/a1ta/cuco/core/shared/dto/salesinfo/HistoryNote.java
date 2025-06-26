package at.a1ta.cuco.core.shared.dto.salesinfo;

@SuppressWarnings("serial")
public class HistoryNote extends SalesInfoNote {
  public enum HistoryLevel {
    NOTE, PRODUCT_NOTE, TODO_GROUP_NOTE
  }

  public enum HistoryTitle {
    NOTE_CREATED, NOTE_UPDATED, NOTE_FINALIZED, NOTE_DELETED, ATTACHMENT_ADDED, ATTACHMENT_DELETED, TERMIN_CREATED, TERMIN_MIGRATED, TERMIN_DELETED, PRODUCT_CREATED, PRODUCT_DELETED, PRODUCT_GROUP_CREATED, PRODUCT_GROUP_DELETED, PRODUCT_GROUP_ASSIGNED, PRODUCT_GROUP_MODIFIED, PRODUCT_GROUP_COMPLETED, TASK_CREATD, TASK_MODIFIED, TASK_DELETED, PRODUCT_UPDATED
  }

  private HistoryTitle historyTitle;
  private HistoryLevel level;
  private Long historyNoteId;

  public HistoryNote() {
    super();
    this.setSalesInfoNoteType(SalesInfoNoteType.SI_HISTORY_NOTE);
  }

  public HistoryNote(HistoryLevel level, HistoryTitle title) {
    super();
    this.setSalesInfoNoteType(SalesInfoNoteType.SI_HISTORY_NOTE);
    this.historyTitle = title;
    this.level = level;
  }

  public HistoryTitle getHistoryTitle() {
    return historyTitle;
  }

  public void setHistoryTitle(HistoryTitle historyTitle) {
    this.historyTitle = historyTitle;
  }

  public void setHistoryTitle(String historyTitle) {
    this.historyTitle = HistoryTitle.valueOf(historyTitle);
  }

  public HistoryLevel getLevel() {
    return level;
  }

  public void setLevel(HistoryLevel level) {
    this.level = level;
  }

  public void setLevel(String level) {
    this.level = HistoryLevel.valueOf(level);
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = super.hashCode();
    result = prime * result + ((historyTitle == null) ? 0 : historyTitle.hashCode());
    result = prime * result + ((level == null) ? 0 : level.hashCode());
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
    if (!(obj instanceof HistoryNote)) {
      return false;
    }
    HistoryNote other = (HistoryNote) obj;
    if (historyTitle == null) {
      if (other.historyTitle != null) {
        return false;
      }
    } else if (!historyTitle.equals(other.historyTitle)) {
      return false;
    }
    if (level != other.level) {
      return false;
    }
    return true;
  }

  @Override
  public String toString() {
    return "HistoryNote [historyTitle=" + historyTitle + ", level=" + level + "]";
  }

  public Long getHistoryNoteId() {
    return historyNoteId;
  }

  public void setHistoryNoteId(Long historyNoteId) {
    this.historyNoteId = historyNoteId;
  }

}
