package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.dao.db.TeamDao;
import at.a1ta.cuco.core.service.TeamService;
import at.a1ta.cuco.core.shared.dto.Auth;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;

@org.springframework.stereotype.Service
public class TeamServiceImpl implements TeamService {

  private TeamDao teamDao;

  @Override
  public List<Team> getAllTeams() {
    List<Team> teams = teamDao.getAllTeams();
    for (Team team : teams) {
      team.setMembers(teamDao.getUsersForTeam(team.getId()));
      team.setServices(teamDao.getServicesForTeam(team.getId()));
    }

    return teams;
  }

  @Override
  @Transactional(value = "transactionManager")
  public void updateTeam(Team team) {
    teamDao.updateTeam(team);

    teamDao.removeAllMembers(team.getId());
    for (BiteUser user : team.getMembers()) {
      teamDao.addMember(team.getId(), user.getId());
    }

    teamDao.removeAllServices(team.getId());
    for (Service service : team.getServices()) {
      teamDao.addService(team.getId(), service.getId());
    }
  }

  @Override
  @Transactional(value = "transactionManager")
  public void deleteTeam(Long teamId) {
    teamDao.removeAllMembers(teamId);
    teamDao.removeAllServices(teamId);
    teamDao.deleteTeam(teamId);
  }

  @Override
  public Team getTeam(Long teamId) {
    Team team = teamDao.getTeam(teamId);
    team.setMembers(teamDao.getUsersForTeam(teamId));
    team.setServices(teamDao.getServicesForTeam(teamId));
    return team;
  }

  @Override
  public void save(Team team) {
    if (team.getId() == null || team.getId().equals(0L)) {
      insertTeam(team);
    } else {
      updateTeam(team);
    }
  }

  @Override
  @Transactional(value = "transactionManager")
  public void insertTeam(Team team) {
    teamDao.addTeam(team);
    for (BiteUser user : team.getMembers()) {
      teamDao.addMember(team.getId(), user.getId());
    }
    for (Service service : team.getServices()) {
      teamDao.addService(team.getId(), service.getId());
    }
  }

  @Override
  public void removeTeamMember(Long teamId, Long userId) {
    teamDao.removeMember(teamId, userId);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void addTeamMembers(Long teamId, List<Long> userIds) {
    for (Long userId : userIds) {
      teamDao.removeUserFromTeam(userId);
      teamDao.addMember(teamId, userId);
    }
  }

  @Override
  public List<Service> getNotLinkedServices(Long teamId) {
    return teamDao.getNotLinkedServices(teamId);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void addServices(Long teamId, List<Long> serviceIds) {
    for (Long serviceId : serviceIds) {
      teamDao.addService(teamId, serviceId);
    }
  }

  @Override
  public void removeService(Long teamId, Long serviceId) {
    teamDao.removeService(teamId, serviceId);
  }

  @Override
  public List<BiteUser> getAllUsers(Auth authority) {
    return teamDao.getAllUsers(authority);
  }

  @Override
  public Team getTeamForUser(Long userId) {
    return teamDao.getTeamForUser(userId);
  }

  @Autowired
  public void setTeamDao(TeamDao teamDao) {
    this.teamDao = teamDao;
  }

  @Override
  public List<Service> getService(String service) {
    return teamDao.getService(service);
  }

  @Override
  public ArrayList<BiteUser> searchUsers(String name, String user, String orgunit) {
    return (ArrayList<BiteUser>) teamDao.searchUsers(name, user, orgunit);
  }
}
