package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.TeamDao;
import at.a1ta.cuco.core.dao.db.UserShopAssignmentDao;
import at.a1ta.cuco.core.service.UserShopAssignmentService;
import at.a1ta.cuco.core.shared.dto.UserShopAssignment;
import at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine;

@Service
public class UserShopAssignmentServiceImpl implements UserShopAssignmentService {

  private UserShopAssignmentDao userShopAssignmentDao;

  @Autowired
  public void setUserShopAssignmentDao(UserShopAssignmentDao userShopAssignmentDao) {
    this.userShopAssignmentDao = userShopAssignmentDao;
  }
  
  @Override
  public List<UserShopAssignment> getUserShopAssignments() {
    return userShopAssignmentDao.getUserShopAssignments();
  }
  
  @Override
  public HashMap<String,String> getUserShopAssignmentsForUserManagement() {
    HashMap<String,String> preparedData = new HashMap<String,String>();
    ArrayList<UserShopAssignment> data = new ArrayList<UserShopAssignment>(getUserShopAssignments());
    
    for( UserShopAssignment u : data ) {
      if( preparedData.containsKey( u.getUserName().toUpperCase() ) ) {
        String shopids = preparedData.get( u.getUserName().toUpperCase() );
        shopids = shopids + ", " + u.getShopID();
        preparedData.put(u.getUserName().toUpperCase(), shopids);
      }
      else {
        preparedData.put(u.getUserName().toUpperCase(), u.getShopID());
      }
    }
    
    return preparedData;
  }

  @Override
  public List<UserShopAssignmentLogLine> getLogEntries() {
    return userShopAssignmentDao.getLogEntries();
  }

  @Override
  public Integer getLogEntriesCount() {
    return userShopAssignmentDao.getLogEntriesCount();
  }

  @Override
  public void insertLogEntry(UserShopAssignmentLogLine logline) {
    userShopAssignmentDao.insertLogEntry(logline);
  }

  @Override
  public void insertUserShopAssignment(UserShopAssignment assignment) {
    userShopAssignmentDao.insertUserShopAssignment(assignment);
  }

  @Override
  public void purgeLogEntries() {
    userShopAssignmentDao.purgeLogEntries();
  }

  @Override
  public void purgeUserShopAssignments() {
    userShopAssignmentDao.purgeUserShopAssignments();
  }

  @Override
  public List<String> getUserNamesForAssignments() {
    return userShopAssignmentDao.getUserNamesForAssignments();
  }

  @Override
  public List<String> getAssignedShopIDs() {
    return userShopAssignmentDao.getAssignedShopIDs();
  }
  
}
