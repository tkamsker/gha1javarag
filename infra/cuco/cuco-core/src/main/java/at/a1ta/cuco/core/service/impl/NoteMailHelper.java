package at.a1ta.cuco.core.service.impl;

import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.service.SalesInfoService;
import at.a1ta.cuco.core.service.visitreport.VisitReportService;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;
import at.a1ta.cuco.core.shared.dto.salesinfo.Task;

public class NoteMailHelper {

  private VisitReportService visitReportService;
  private SalesInfoService salesInfoService;
  private MailService mailService;

  public NoteMailHelper(VisitReportService visitReportService, SalesInfoService salesInfoService, MailService mailService) {
    this.visitReportService = visitReportService;
    this.salesInfoService = salesInfoService;
    this.mailService = mailService;
  }

  public void sendInsertMails(SalesInfoNote note) throws Exception {
    if (isVcalMailActive(note.getTask())) {
      mailService.sendVcalMail(note);
    }
  }

  public void sendUpdateMails(SalesInfoNote note) throws Exception {
    SalesInfoNote origNote = null;

    if (SalesInfoNoteType.SI_SIMPLE_NOTE == note.getSalesInfoNoteType()) {
      origNote = salesInfoService.getSimpleNoteByNoteId(note.getSalesInfoNoteId());
    } else if (SalesInfoNoteType.SI_COMPETITOR_NOTE == note.getSalesInfoNoteType()) {
      origNote = salesInfoService.getCompetitorNoteByNoteId(note.getSalesInfoNoteId());
    } else if (SalesInfoNoteType.SI_SALES_CONV_NOTE == note.getSalesInfoNoteType()) {
      origNote = visitReportService.getSalesConvNoteByNoteId(note.getSalesInfoNoteId());
    }

    if (origNote == null) {
      return;
    }
    Task currTask = note.getTask();
    Task origTask = origNote.getTask();

    if (isVcalMailActive(currTask) && (hasTextChanged(note, origNote) || hasTimeChanged(origTask, currTask) || hasAssigneeChanged(origTask, currTask))) {
      mailService.sendVcalMail(note);
    }

    if ((isVcalMailActive(origTask) && !isVcalMailActive(currTask)) || (hasAssigneeChanged(origTask, currTask) && isVcalMailActive(origTask))) {
      mailService.sendVcalCancelMail(origNote);
    }
  }

  private boolean isVcalMailActive(Task task) {
    return task.isActive() && task.isSendVCalendarMail();
  }

  private boolean hasTextChanged(SalesInfoNote orig, SalesInfoNote curr) {
    String origText = orig.getNoteText();
    String currText = curr.getNoteText();
    if (currText == null) {
      return origText != null;
    }
    return !currText.equals(origText);
  }

  private boolean hasTimeChanged(Task orig, Task curr) {
    Date origDate = orig.getStartDate();
    Date currDate = curr.getStartDate();
    if (currDate == null) {
      return origDate != null;
    }
    return !currDate.equals(origDate);
  }

  private boolean hasAssigneeChanged(Task orig, Task curr) {

    BiteUser currUser = curr.getAssigneeUser();
    if (currUser == null) {
      return orig != null;
    }
    BiteUser origUser = orig.getAssigneeUser();
    return !currUser.getId().equals(origUser.getId());
  }
}
