package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.HashMap;
import java.util.List;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.cuco.core.shared.dto.UserShopAssignment;
import at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine;

@RemoteServiceRelativePath("cuco/usershopassignment.rpc")
public interface UserShopAssignmentServlet extends RemoteService {

  // select
  public List<UserShopAssignment> getUserShopAssignments();

  public HashMap<String, String> getUserShopAssignmentsForUserManagement();

  public List<UserShopAssignmentLogLine> getLogEntries();

  public Integer getLogEntriesCount();

  public List<String> getUserNamesForAssignments();

  public List<String> getAssignedShopIDs();

  // insert
  public void insertLogEntry(UserShopAssignmentLogLine logline);

  public void insertUserShopAssignment(UserShopAssignment assignment);

  // delete
  public void purgeLogEntries();

  public void purgeUserShopAssignments();

}