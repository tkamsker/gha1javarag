package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs;

import java.io.Serializable;

import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;

public class VisitReportDetail implements Serializable {
  private SalesInfoNote note;
  private boolean editable;

  public SalesInfoNote getNote() {
    return note;
  }

  public void setNote(SalesInfoNote note) {
    this.note = note;
  }

  public boolean isEditable() {
    return editable;
  }

  public void setEditable(boolean editable) {
    this.editable = editable;
  }

}
