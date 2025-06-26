package at.a1ta.cuco.core.dao.db;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.UserShopAssignment;
import at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine;

public interface UserShopAssignmentDao {
  
  List<UserShopAssignmentLogLine> getLogEntries();
  List<UserShopAssignment> getUserShopAssignments();
  Integer getLogEntriesCount();
  void insertLogEntry(UserShopAssignmentLogLine logline);
  void insertUserShopAssignment(UserShopAssignment assignment);
  void purgeLogEntries();
  void purgeUserShopAssignments();
  List<String> getUserNamesForAssignments();
  List<String> getAssignedShopIDs();
  
}