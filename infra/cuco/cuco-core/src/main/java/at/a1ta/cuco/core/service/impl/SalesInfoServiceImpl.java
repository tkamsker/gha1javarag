package at.a1ta.cuco.core.service.impl;

import java.util.Collection;
import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.dao.UserDao;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.cuco.core.dao.db.SalesInfoDao;
import at.a1ta.cuco.core.dao.db.StandardAddressDao;
import at.a1ta.cuco.core.service.SalesInfoService;
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

@Service
public class SalesInfoServiceImpl implements SalesInfoService {
  @Autowired
  private SalesInfoDao salesInfoDao;
  @Autowired
  private StandardAddressDao standardAddressDao;
  @Autowired
  private UserDao userDao;

  @Override
  public List<SalesInfoNote> getNotesByPartyId(long partyId, List<SalesInfoNoteType> salesInfoNoteTypesToLoad) {
    return salesInfoDao.getNotesByPartyId(partyId, salesInfoNoteTypesToLoad);
  }

  @Override
  public void insertSalesInfoNote(SalesInfoNote note) {
    if (note.getTask() != null && note.getTask().getAddress() != null && note.getTask().getAddress().getAddressId() < 0) {
      standardAddressDao.insertAddress(note.getTask().getAddress());
    }
    if (note.getTask() != null) {
      salesInfoDao.insertTask(note.getTask());
    }
    salesInfoDao.insertNote(note);
    if (note instanceof SimpleNote) {
      salesInfoDao.insertSimpleNote((SimpleNote) note);
    } else if (note instanceof CompetitorNote) {
      salesInfoDao.insertCompetitorNote((CompetitorNote) note);
    } else if (note instanceof AppointmentNote) {
      salesInfoDao.insertAppointmentNote((AppointmentNote) note);
    }
  }

  @Override
  public void updateSalesInfoNote(SalesInfoNote note) {
    salesInfoDao.updateNote(note);
    if (note instanceof SimpleNote) {
      // nothing to do
    } else if (note instanceof CompetitorNote) {
      salesInfoDao.updateCompetitorNote((CompetitorNote) note);
    } else if (note instanceof AppointmentNote) {
      salesInfoDao.updateAppointmentNote((AppointmentNote) note);
    }
    if (note.getTask() != null && note.getTask().getAddress() != null) {
      if (note.getTask().getAddress().getAddressId() < 0) {
        standardAddressDao.insertAddress(note.getTask().getAddress());
      } else {
        standardAddressDao.updateAddress(note.getTask().getAddress());
      }
    }
    if (note.getTask() != null) {
      salesInfoDao.updateTask(note.getTask());
    }
  }

  @Override
  public void markNoteAsDeleted(SalesInfoNote note) {

    salesInfoDao.markNoteAsDeleted(note);
  }

  @Override
  public SimpleNote getSimpleNoteByNoteId(long noteId) {
    return salesInfoDao.getSimpleNoteByNoteId(noteId);
  }

  @Override
  public CompetitorNote getCompetitorNoteByNoteId(long noteId) {
    return salesInfoDao.getCompetitorNoteByNoteId(noteId);
  }

  @Override
  public AppointmentNote getAppointmentNoteByNoteId(long noteId) {
    return salesInfoDao.getAppointmentNoteByNoteId(noteId);
  }

  @Override
  public Task getTask(long taskId) {
    return salesInfoDao.getTask(taskId);
  }

  @Override
  public SalesInfoNote getSalesInfoNote(long salesInfoNoteId) {
    return salesInfoDao.getSalesInfoNote(salesInfoNoteId);
  }

  @Override
  public List<SbsNoteReportRow> getSbsNoteReportData(Date startDate, Date endDate) {
    return salesInfoDao.getSbsNoteReportData(startDate, endDate);
  }

  @Override
  public List<SalesConvNoteReportRow> getSalesConvNoteReportData(Date startDate, Date endDate) {
    return salesInfoDao.getSalesConvNoteReportData(startDate, endDate);
  }

  @Override
  public List<TeamEmailAdminGroup> getTeamEmailAdminGroups() {
    return salesInfoDao.getTeamEmailAdminGroups();
  }

  @Override
  public String saveTeamEmailAdminGroups(List<TeamEmailAdminGroup> teamEmailAdminGroups) {
    String failedUsers = "";
    for (TeamEmailAdminGroup t : teamEmailAdminGroups) {
      salesInfoDao.deleteTeamEmailAdminUsersByTeamEmailId(t.getId());
      if (t.getUserList() != null && !t.getUserList().isEmpty()) {
        for (String login : t.getUserList().split(";")) {
          UserInfo userInfo = userDao.getByUsername(login.trim());
          if (userInfo != null) {
            salesInfoDao.insertTeamEmailAdminUser(t.getId(), userInfo.getId());
          } else {
            failedUsers += login + ";";
          }
        }
      }
      salesInfoDao.updateTeamEmailAdminGroup(t);
    }
    return failedUsers;
  }

  // Changed By Nisha(Added this unimplemented method for removing errors)

  @Override
  public Collection<SBSProductNote> getProductNotesByNoteId(long noteId) {
    // TODO Auto-generated method stub
    return null;
  }

  @Override
  public SalesInfoNote getAppointmentNoteForHistoryByNoteId(Long historyNoteId) {
    return salesInfoDao.getAppointmentNoteForHistoryByNoteId(historyNoteId);
  }

  @Override
  public SalesInfoNote getTaskNoteForHistoryByNoteId(Long historyNoteId) {
    return salesInfoDao.getTaskNoteForHistoryByNoteId(historyNoteId);
  }
}
