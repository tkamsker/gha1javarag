package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.dao.db.TeamDao;
import at.a1ta.cuco.core.shared.dto.Auth;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;

public class TeamDaoImpl extends AbstractDao implements TeamDao {

  @Override
  public void addMember(Long teamId, Long userId) {
    Map<String, Long> params = new HashMap<String, Long>();
    params.put("teamId", teamId);
    params.put("userId", userId);

    executeInsert("Team.AddMember", params);
  }

  @Override
  public void addTeam(Team team) {
    executeInsert("Team.AddTeam", team);
  }

  @Override
  public void deleteTeam(Long teamId) {
    executeDelete("Team.DeleteTeam", teamId);
  }

  @Override
  public List<Team> getAllTeams() {
    return performListQuery("Team.GetAllTeams");
  }

  @Override
  public List<Service> getServicesForTeam(Long teamId) {
    return performListQuery("Team.GetServicesForTeam", teamId);
  }

  @Override
  public Team getTeam(Long teamId) {
    return performObjectQuery("Team.GetTeam", teamId);
  }

  @Override
  public List<BiteUser> getAllUsers(Auth authority) {
    return performListQuery("User.GetAllUsers", authority.getName());
  }

  @Override
  public List<BiteUser> getUsersForTeam(Long teamId) {
    return performListQuery("User.GetUsersForTeam", teamId);
  }

  @Override
  public void removeMember(Long teamId, Long userId) {
    Map<String, Long> params = new HashMap<String, Long>();
    params.put("teamId", teamId);
    params.put("userId", userId);

    executeDelete("Team.RemoveMember", params);
  }

  @Override
  public void addService(Long teamId, Long serviceId) {
    Map<String, Long> params = new HashMap<String, Long>();
    params.put("teamId", teamId);
    params.put("serviceId", serviceId);

    executeInsert("Team.AddService", params);
  }

  @Override
  public void removeService(Long teamId, Long serviceId) {
    Map<String, Long> params = new HashMap<String, Long>();
    params.put("teamId", teamId);
    params.put("serviceId", serviceId);

    executeDelete("Team.RemoveService", params);
  }

  @Override
  public void updateTeam(Team team) {
    executeUpdate("Team.UpdateTeam", team);
  }

  @Override
  public void removeAllMembers(Long teamId) {
    executeDelete("Team.RemoveAllMembers", teamId);
  }

  @Override
  public void removeAllServices(Long teamId) {
    executeDelete("Team.RemoveAllServices", teamId);
  }

  @Override
  public List<Service> getNotLinkedServices(Long teamId) {
    return performListQuery("Team.GetNotLinkedServices", teamId);
  }

  @Override
  public void removeUserFromTeam(Long userId) {
    executeDelete("Team.removeUserFromTeam", userId);
  }

  @Override
  public Team getTeamForUser(Long userId) {
    return (Team) performObjectQuery("Team.GetTeamForUser", userId);
  }

  @Override
  public List<Service> getService(String service) {
    return performListQuery("Team.getService", service);
  }

  @Override
  public List<BiteUser> searchUsers(String name, String user, String orgunit) {
    Map<String, String> params = new HashMap<String, String>();
    params.put("name", name);
    params.put("usr", user);
    params.put("orgunit", orgunit);
    return performListQuery("User.searchAll", params);
  }
}
