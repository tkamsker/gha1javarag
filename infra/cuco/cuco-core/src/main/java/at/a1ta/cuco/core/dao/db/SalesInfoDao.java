package at.a1ta.cuco.core.dao.db;

import java.util.Date;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.salesinfo.AppointmentNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.CompetitorNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesConvNoteReportRow;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;
import at.a1ta.cuco.core.shared.dto.salesinfo.SbsNoteReportRow;
import at.a1ta.cuco.core.shared.dto.salesinfo.SimpleNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.Task;
import at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote.TeamEmailAdminGroup;

public interface SalesInfoDao {

  List<SalesInfoNote> getNotesByPartyId(long partyId, List<SalesInfoNoteType> salesInfoNoteTypesToLoad);

  void insertNote(SalesInfoNote salesInfoNote);

  void updateNote(SalesInfoNote salesInfoNote);

  void markNoteAsDeleted(SalesInfoNote salesInfoNote);

  SimpleNote getSimpleNoteByNoteId(long noteId);

  void insertSimpleNote(SimpleNote simpleNote);

  CompetitorNote getCompetitorNoteByNoteId(long noteId);

  void insertCompetitorNote(CompetitorNote competitorNote);

  void updateCompetitorNote(CompetitorNote competitorNote);

  Task getTask(long taskId);

  void insertTask(Task task);

  void updateTask(Task task);

  List<SalesInfoNote> getNotesForReminderMail();

  void updateTaskReminderMailSentDate(Task task);

  void updateTaskVcalMailSentInfo(Task task);

  SalesInfoNote getSalesInfoNote(long salesInfoNoteId);

  List<SbsNoteReportRow> getSbsNoteReportData(Date begin, Date end);

  List<SalesConvNoteReportRow> getSalesConvNoteReportData(Date begin, Date end);

  void updateBindingPeriodReminderMailSentDate(CompetitorNote cpNote);

  List<CompetitorNote> getNotesForBindingPeriodReminderMail(long numDays);

  List<TeamEmailAdminGroup> getTeamEmailAdminGroups();

  void updateTeamEmailAdminGroup(TeamEmailAdminGroup teamEmailAdminGroup);

  void deleteTeamEmailAdminUsersByTeamEmailId(long teamEmailId);

  void insertTeamEmailAdminUser(long teamEmailId, long userId);

  List<SalesInfoNote> getSalesConvNotesForReminderMail();

  void updateLastReminderMailSentDateForSalesConvNote(long salesConvNoteId);

  void insertAppointmentNote(AppointmentNote note);

  void updateAppointmentNote(AppointmentNote note);

  AppointmentNote getAppointmentNoteByNoteId(long noteId);

  SalesInfoNote getAppointmentNoteForHistoryByNoteId(Long historyNoteId);

  SalesInfoNote getTaskNoteForHistoryByNoteId(Long historyNoteId);

}
