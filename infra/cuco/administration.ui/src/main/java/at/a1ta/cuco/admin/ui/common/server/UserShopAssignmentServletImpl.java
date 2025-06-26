package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.annotation.WebServlet;
import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.ui.server.servlet.AuthenticationServlet;
import at.a1ta.cuco.admin.ui.common.client.service.UserShopAssignmentServlet;
import at.a1ta.cuco.core.service.UserShopAssignmentService;
import at.a1ta.cuco.core.shared.dto.UserShopAssignment;
import at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine;

@WebServlet(name = "userShopAssignment", urlPatterns = {"/admin/cuco/usershopassignment.rpc"})
public class UserShopAssignmentServletImpl extends AuthenticationServlet implements UserShopAssignmentServlet {

  @Autowired
  private UserShopAssignmentService userShopAssignmentService;

  @Override
  public List<UserShopAssignment> getUserShopAssignments() {
    return userShopAssignmentService.getUserShopAssignments();
  }

  @Override
  public List<UserShopAssignmentLogLine> getLogEntries() {
    return userShopAssignmentService.getLogEntries();
  }

  @Override
  public Integer getLogEntriesCount() {
    return userShopAssignmentService.getLogEntriesCount();
  }

  @Override
  public void insertLogEntry(UserShopAssignmentLogLine logline) {
    userShopAssignmentService.insertLogEntry(logline);
  }

  @Override
  public void insertUserShopAssignment(UserShopAssignment assignment) {
    userShopAssignmentService.insertUserShopAssignment(assignment);
  }

  @Override
  public void purgeLogEntries() {
    userShopAssignmentService.purgeLogEntries();
  }

  @Override
  public void purgeUserShopAssignments() {
    userShopAssignmentService.purgeUserShopAssignments();
  }

  @Override
  public HashMap<String, String> getUserShopAssignmentsForUserManagement() {
    return userShopAssignmentService.getUserShopAssignmentsForUserManagement();
  }

  @Override
  public List<String> getUserNamesForAssignments() {
    return userShopAssignmentService.getUserNamesForAssignments();
  }

  @Override
  public List<String> getAssignedShopIDs() {
    return userShopAssignmentService.getAssignedShopIDs();
  }

}
