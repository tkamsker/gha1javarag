package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class Salesstage implements Serializable {

  public enum Status {
    // @formatter:off
    CREATED("Erstellt"), SAVED("Gespeichert"), APPROVED("Freigegeben"), DISAPPROVED("Ablehnen"), FINALIZED("Finalisiert"), SENT("An Kunde Übergeben"), ACCEPTED("Angenommen"), DECLINED("Abgelehnt"), ORDERED(
        "Bestellt"), CLOSED("Geschlossen"), PRINTED("Gedruckt"), CANCELED("Abgebrochen"), ARCHIVED("Gelöscht"), CLEARANCE_PENDING("Zur Freigabe"), CLEARANCE_IN_PROGRESS("Vorabfreigabe"), CLEARANCE_COMPLETED(
        "Endfreigabe"), CLEARANCE_DECLINED("Nicht Freigegeben");
    // @formatter:on

    private String name;

    private Status(String name) {
      this.name = name;
    }

    public String getName() {
      return name;
    }

    public static Status findByName(String name) {
      for (Status value : values()) {
        if (value.name().equals(name)) {
          return value;
        }
      }
      return null;
    }
  }

  private Status status;
  private Date changeDate;
  private Long quoteId;
  private BiteUser executor;

  public Status getStatus() {
    return status;
  }

  public void setStatus(Status status) {
    this.status = status;
  }

  public Long getQuoteId() {
    return quoteId;
  }

  public void setQuoteId(Long quoteId) {
    this.quoteId = quoteId;
  }

  public Date getChangeDate() {
    return changeDate;
  }

  public void setChangeDate(Date changeDate) {
    this.changeDate = changeDate;
  }

  public BiteUser getExecutor() {
    return executor;
  }

  public void setExecutor(BiteUser executor) {
    this.executor = executor;
  }
}
