package at.a1ta.webclient.cucosett.server;

import javax.servlet.annotation.WebServlet;
import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.ui.server.servlet.SpringRemoteServiceServlet;
import at.a1ta.cuco.core.service.TeamService;
import at.a1ta.cuco.core.shared.dto.Auth;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.webclient.cucosett.client.service.TeamServlet;

@WebServlet(name = "team", urlPatterns = {"/admin/cuco/team.rpc"})
public class TeamServletImpl extends SpringRemoteServiceServlet implements TeamServlet {

  private static final long serialVersionUID = 1L;
  @Autowired
  private TeamService teamService;

  @Override
  public ArrayList<Team> getAllTeams() {
    return (ArrayList<Team>) teamService.getAllTeams();
  }

  @Override
  public Team saveTeam(Team team) {
    teamService.save(team);
    return team;
  }

  @Override
  public RpcStatus deleteTeam(Long teamId) {
    teamService.deleteTeam(teamId);
    return RpcStatus.OK;
  }

  @Override
  public RpcStatus removeTeamMember(Long teamId, Long userId) {
    teamService.removeTeamMember(teamId, userId);
    return RpcStatus.OK;
  }

  @Override
  public RpcStatus addTeamMembers(Long teamId, ArrayList<Long> userIds) {
    teamService.addTeamMembers(teamId, userIds);
    return RpcStatus.OK;
  }

  @Override
  public ArrayList<Service> getNotLinkedServices(Long teamId) {
    return (ArrayList<Service>) teamService.getNotLinkedServices(teamId);
  }

  @Override
  public RpcStatus addServices(Long teamId, ArrayList<Long> serviceIds) {
    teamService.addServices(teamId, serviceIds);
    return RpcStatus.OK;
  }

  @Override
  public RpcStatus removeService(Long teamId, Long serviceId) {
    teamService.removeService(teamId, serviceId);
    return RpcStatus.OK;
  }

  @Override
  public ArrayList<BiteUser> getAllUsers() {
    return (ArrayList<BiteUser>) teamService.getAllUsers(Auth.PAST_GULA_CREATE);
  }

  @Override
  public Team getTeam(Long id) {
    return teamService.getTeam(id);
  }

  @Override
  public ArrayList<Service> getService(String service) {

    return (ArrayList<Service>) teamService.getService(service);
  }

  @Override
  public ArrayList<BiteUser> searchUsers(String name, String user, String orgunit) {
    return (ArrayList<BiteUser>) teamService.searchUsers(name, user, orgunit);
  }
}
