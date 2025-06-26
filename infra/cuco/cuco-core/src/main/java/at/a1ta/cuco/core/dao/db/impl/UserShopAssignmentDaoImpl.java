package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.UserShopAssignmentDao;
import at.a1ta.cuco.core.shared.dto.UserShopAssignment;
import at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine;

public class UserShopAssignmentDaoImpl extends AbstractDao implements UserShopAssignmentDao {

  @Override
  public List<UserShopAssignmentLogLine> getLogEntries() {
    return performListQuery("ImportUserShopAssignment.getLogEntries");
  }

  @Override
  public Integer getLogEntriesCount() {
    Integer count = 0;
    count = performObjectQuery("ImportUserShopAssignment.getLogEntriesCount", count);
    return count.intValue();
  }

  @Override
  public void insertLogEntry(UserShopAssignmentLogLine logline) {
    executeInsert("ImportUserShopAssignment.insertLogEntry", logline);
  }

  @Override
  public List<UserShopAssignment> getUserShopAssignments() {
    return performListQuery("ImportUserShopAssignment.getUserShopAssignments");
  }

  @Override
  public void insertUserShopAssignment(UserShopAssignment assignment) {
    executeInsert("ImportUserShopAssignment.insertUserShopAssignment", assignment);
  }

  @Override
  public void purgeLogEntries() {
    executeDelete("ImportUserShopAssignment.purgeLogEntries", null);
  }

  @Override
  public void purgeUserShopAssignments() {
    executeDelete("ImportUserShopAssignment.purgeUserShopAssignments", null);
  }

  @Override
  public List<String> getUserNamesForAssignments() {
    return performListQuery("ImportUserShopAssignment.getUserIDs4Assignments", null);
  }
  
  @Override
  public List<String> getAssignedShopIDs() {
    return performListQuery("ImportUserShopAssignment.getAssignedShopIDs", null);
  }
  
}