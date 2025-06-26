package at.a1ta.cuco.core.service;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.shared.dto.Auth;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;

public interface TeamService {

  public void updateTeam(Team team);

  public void insertTeam(Team team);

  public List<Team> getAllTeams();

  public void deleteTeam(Long teamId);

  public Team getTeam(Long teamId);

  public Team getTeamForUser(Long userId);

  public void save(Team team);

  public void removeTeamMember(Long teamId, Long userId);

  public List<BiteUser> getAllUsers(Auth authority);

  public void addTeamMembers(Long teamId, List<Long> userIds);

  public List<Service> getNotLinkedServices(Long teamId);

  public void addServices(Long teamId, List<Long> serviceIds);

  public void removeService(Long teamId, Long serviceId);

  public List<Service> getService(String service);

  public ArrayList<BiteUser> searchUsers(String name, String user, String orgunit);
}
