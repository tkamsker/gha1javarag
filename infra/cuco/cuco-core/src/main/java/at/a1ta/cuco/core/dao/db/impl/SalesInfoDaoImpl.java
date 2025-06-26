package at.a1ta.cuco.core.dao.db.impl;

import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.SalesInfoDao;
import at.a1ta.cuco.core.shared.dto.salesinfo.AppointmentNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.CompetitorNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesConvNoteReportRow;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote.SalesInfoNoteType;
import at.a1ta.cuco.core.shared.dto.salesinfo.SbsNoteReportRow;
import at.a1ta.cuco.core.shared.dto.salesinfo.SimpleNote;
import at.a1ta.cuco.core.shared.dto.salesinfo.Task;
import at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote.TeamEmailAdminGroup;

public class SalesInfoDaoImpl extends AbstractDao implements SalesInfoDao {
  @Override
  public List<SalesInfoNote> getNotesByPartyId(long partyId, List<SalesInfoNoteType> salesInfoNoteTypesToLoad) {
    Map<String, Object> params = new HashMap<String, Object>(2);
    params.put("partyId", Long.valueOf(partyId));
    params.put("salesInfoNoteTypesToLoad", salesInfoNoteTypesToLoad);
    return performListQuery("SalesInfo.getNotesByPartyId", params);
  }

  @Override
  public void insertNote(SalesInfoNote salesInfoNote) {
    executeInsert("SalesInfo.insertNote", salesInfoNote);
  }

  @Override
  public void updateNote(SalesInfoNote salesInfoNote) {
    executeUpdate("SalesInfo.updateNote", salesInfoNote);
  }

  @Override
  public SimpleNote getSimpleNoteByNoteId(long noteId) {
    return performObjectQuery("SalesInfo.getSimpleNoteByNoteId", noteId);
  }

  @Override
  public void insertSimpleNote(SimpleNote simpleNote) {
    executeInsert("SalesInfo.insertSimpleNote", simpleNote);
  }

  @Override
  public CompetitorNote getCompetitorNoteByNoteId(long noteId) {
    return performObjectQuery("SalesInfo.getCompetitorNoteByNoteId", noteId);
  }

  @Override
  public AppointmentNote getAppointmentNoteByNoteId(long noteId) {
    return performObjectQuery("SalesInfo.getAppointmentNoteByNoteId", noteId);
  }

  @Override
  public void insertCompetitorNote(CompetitorNote competitorNote) {
    executeInsert("SalesInfo.insertCompetitorNote", competitorNote);
  }

  @Override
  public void updateCompetitorNote(CompetitorNote competitorNote) {
    executeUpdate("SalesInfo.updateCompetitorNote", competitorNote);
  }

  @Override
  public void updateAppointmentNote(AppointmentNote note) {
    executeUpdate("SalesInfo.updateAppointmentNote", note);
  }

  @Override
  public Task getTask(long taskId) {
    return performObjectQuery("SalesInfo.getTask", taskId);
  }

  @Override
  public void insertTask(Task task) {
    executeInsert("SalesInfo.insertTask", task);
  }

  @Override
  public void updateTask(Task task) {
    executeUpdate("SalesInfo.updateTask", task);
  }

  @Override
  public List<SalesInfoNote> getNotesForReminderMail() {
    return performListQuery("SalesInfo.getNotesForReminderMail");
  }

  @Override
  public void updateTaskReminderMailSentDate(Task task) {
    executeUpdate("SalesInfo.updateTaskReminderMailSentDate", task);
  }

  @Override
  public void updateTaskVcalMailSentInfo(Task task) {
    executeUpdate("SalesInfo.updateTaskVcalMailSentInfo", task);
  }

  @Override
  public SalesInfoNote getSalesInfoNote(long salesInfoNoteId) {
    return performObjectQuery("SalesInfo.getSalesInfoNote", salesInfoNoteId);
  }

  @Override
  public List<SbsNoteReportRow> getSbsNoteReportData(Date begin, Date end) {
    HashMap<String, Date> params = new HashMap<String, Date>();
    params.put("begin", begin);
    params.put("end", end);
    return performListQuery("SalesInfo.getSbsNoteReportData", params);
  }

  @Override
  public List<SalesConvNoteReportRow> getSalesConvNoteReportData(Date begin, Date end) {
    HashMap<String, Date> params = new HashMap<String, Date>();
    params.put("begin", begin);
    params.put("end", end);
    return performListQuery("SalesInfo.getSalesConvNoteReportData", params);
  }

  @Override
  public void updateBindingPeriodReminderMailSentDate(CompetitorNote cpNote) {
    executeUpdate("SalesInfo.updateBindingPeriodReminderMailSentDate", cpNote);
  }

  @Override
  public List<CompetitorNote> getNotesForBindingPeriodReminderMail(long numDays) {

    HashMap<String, Long> params = new HashMap<String, Long>();
    params.put("numDays", numDays);
    return performListQuery("SalesInfo.getNotesForBindingPeriodReminderMail", params);
  }

  @Override
  public List<TeamEmailAdminGroup> getTeamEmailAdminGroups() {
    return performListQuery("SalesInfo.getTeamEmailAdminGroups");
  }

  @Override
  public void updateTeamEmailAdminGroup(TeamEmailAdminGroup teamEmailAdminGroup) {
    executeUpdate("SalesInfo.updateTeamEmailAdminGroup", teamEmailAdminGroup);
  }

  @Override
  public void deleteTeamEmailAdminUsersByTeamEmailId(long teamEmailId) {
    executeDelete("SalesInfo.deleteTeamEmailAdminUsersByTeamEmailId", teamEmailId);
  }

  @Override
  public void insertTeamEmailAdminUser(long teamEmailId, long userId) {
    HashMap<String, Long> params = new HashMap<String, Long>();
    params.put("teamEmailId", teamEmailId);
    params.put("userId", userId);
    executeInsert("SalesInfo.insertTeamEmailAdminUser", params);
  }

  @Override
  public List<SalesInfoNote> getSalesConvNotesForReminderMail() {
    return performListQuery("SalesInfo.getSalesConvNotesForReminderMail");
  }

  @Override
  public void updateLastReminderMailSentDateForSalesConvNote(long salesConvNoteId) {
    executeUpdate("SalesInfo.updateLastReminderMailSentDateForSalesConvNote", salesConvNoteId);
  }

  @Override
  public void markNoteAsDeleted(SalesInfoNote salesInfoNote) {
    executeUpdate("SalesInfo.markNoteAsDeleted", salesInfoNote);
  }

  @Override
  public void insertAppointmentNote(AppointmentNote note) {
    executeInsert("SalesInfo.insertAppointmentNote", note);
  }

  @Override
  public SalesInfoNote getAppointmentNoteForHistoryByNoteId(Long historyNoteId) {
    return performObjectQuery("SalesInfo.getAppointmentNoteForHistoryByNoteId", historyNoteId);
  }

  @Override
  public SalesInfoNote getTaskNoteForHistoryByNoteId(Long historyNoteId) {
    SalesInfoNote note = performObjectQuery("SalesInfo.getSalesInfoNote", historyNoteId);
    if (note != null) {
      if (note.getSalesInfoNoteType() == SalesInfoNoteType.SI_SIMPLE_NOTE) {
        return performObjectQuery("SalesInfo.getSimpleNoteForHistoryByNoteId", historyNoteId);
      } else if (note.getSalesInfoNoteType() == SalesInfoNoteType.SI_COMPETITOR_NOTE) {
        return performObjectQuery("SalesInfo.getCompetitorNoteForHistoryByNoteId", historyNoteId);
      }
    }
    return note;
  }
}
