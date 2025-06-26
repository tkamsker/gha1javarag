package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.HashMap;
import java.util.List;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.cuco.core.shared.dto.UserShopAssignment;
import at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine;

public interface UserShopAssignmentServletAsync {

  // select
  void getUserShopAssignments(AsyncCallback<List<UserShopAssignment>> callback);

  void getUserShopAssignmentsForUserManagement(AsyncCallback<HashMap<String, String>> callback);

  void getLogEntries(AsyncCallback<List<UserShopAssignmentLogLine>> callback);

  void getLogEntriesCount(AsyncCallback<Integer> callback);

  void getUserNamesForAssignments(AsyncCallback<List<String>> callback);

  void getAssignedShopIDs(AsyncCallback<List<String>> callback);

  // insert
  void insertLogEntry(UserShopAssignmentLogLine logline, AsyncCallback<Void> callback);

  void insertUserShopAssignment(UserShopAssignment assignment, AsyncCallback<Void> callback);

  // delete
  void purgeLogEntries(AsyncCallback<Void> callback);

  void purgeUserShopAssignments(AsyncCallback<Void> callback);

}
