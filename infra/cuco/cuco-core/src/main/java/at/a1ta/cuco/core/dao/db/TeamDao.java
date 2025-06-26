package at.a1ta.cuco.core.dao.db;

import java.util.List;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.shared.dto.Auth;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;

public interface TeamDao {
  public List<Team> getAllTeams();

  public void removeMember(Long teamId, Long userId);

  public void addMember(Long teamId, Long userId);

  public List<BiteUser> getAllUsers(Auth authority);

  public void deleteTeam(Long teamId);

  public void updateTeam(Team team);

  public void addTeam(Team team);

  public Team getTeam(Long teamId);

  public Team getTeamForUser(Long userId);

  public List<BiteUser> getUsersForTeam(Long teamId);

  public List<Service> getServicesForTeam(Long teamId);

  public void addService(Long teamId, Long serviceId);

  public void removeService(Long teamId, Long serviceId);

  public void removeAllMembers(Long teamId);

  public void removeAllServices(Long teamId);

  public void removeUserFromTeam(Long userId);

  public List<Service> getNotLinkedServices(Long teamId);

  public List<Service> getService(String service);

  public List<BiteUser> searchUsers(String name, String user, String orgunit);
}
