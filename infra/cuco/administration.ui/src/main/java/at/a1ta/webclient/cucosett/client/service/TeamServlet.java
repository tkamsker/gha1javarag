package at.a1ta.webclient.cucosett.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.framework.ui.client.dto.RpcStatus;

@RemoteServiceRelativePath("cuco/team.rpc")
public interface TeamServlet extends RemoteService {
  public Team getTeam(Long id);

  public ArrayList<Team> getAllTeams();

  public Team saveTeam(Team team);

  public RpcStatus deleteTeam(Long teamId);

  public RpcStatus removeTeamMember(Long teamId, Long userId);

  public RpcStatus removeService(Long teamId, Long serviceId);

  public ArrayList<BiteUser> getAllUsers();

  public RpcStatus addTeamMembers(Long teamId, ArrayList<Long> userIds);

  public ArrayList<Service> getNotLinkedServices(Long teamId);

  public RpcStatus addServices(Long teamId, ArrayList<Long> serviceIds);

  public ArrayList<Service> getService(String service);

  public ArrayList<BiteUser> searchUsers(String name, String user, String orgunit);
}
