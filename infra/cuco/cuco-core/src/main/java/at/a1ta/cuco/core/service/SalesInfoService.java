package at.a1ta.cuco.core.service;

import java.util.Collection;
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
import at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.sbs.SBSProductNote;

public interface SalesInfoService {

  List<SalesInfoNote> getNotesByPartyId(long partyId, List<SalesInfoNoteType> salesInfoNoteTypesToLoad);

  void insertSalesInfoNote(SalesInfoNote salesInfoNote);

  void updateSalesInfoNote(SalesInfoNote salesInfoNote);

  SimpleNote getSimpleNoteByNoteId(long noteId);

  CompetitorNote getCompetitorNoteByNoteId(long noteId);

  Task getTask(long taskId);

  SalesInfoNote getSalesInfoNote(long salesInfoNoteId);

  List<SbsNoteReportRow> getSbsNoteReportData(Date startDate, Date endDate);

  List<SalesConvNoteReportRow> getSalesConvNoteReportData(Date startDate, Date endDate);

  List<TeamEmailAdminGroup> getTeamEmailAdminGroups();

  String saveTeamEmailAdminGroups(List<TeamEmailAdminGroup> teamEmailAdminGroups);

  Collection<SBSProductNote> getProductNotesByNoteId(long noteId);

  void markNoteAsDeleted(SalesInfoNote note);

  AppointmentNote getAppointmentNoteByNoteId(long noteId);

  SalesInfoNote getAppointmentNoteForHistoryByNoteId(Long historyNoteId);

  SalesInfoNote getTaskNoteForHistoryByNoteId(Long historyNoteId);
}
