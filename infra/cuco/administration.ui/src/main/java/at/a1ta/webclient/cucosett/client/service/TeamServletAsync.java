package at.a1ta.webclient.cucosett.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.framework.ui.client.dto.RpcStatus;

public interface TeamServletAsync {
  public void getTeam(Long id, AsyncCallback<Team> callback);

  public void getAllTeams(AsyncCallback<ArrayList<Team>> callback);

  public void saveTeam(Team team, AsyncCallback<Team> callback);

  public void deleteTeam(Long teamId, AsyncCallback<RpcStatus> callback);

  public void removeTeamMember(Long teamId, Long userId, AsyncCallback<RpcStatus> callback);

  public void getAllUsers(AsyncCallback<ArrayList<BiteUser>> callback);

  public void addTeamMembers(Long teamId, ArrayList<Long> userIds, AsyncCallback<RpcStatus> callback);

  public void getNotLinkedServices(Long teamId, AsyncCallback<ArrayList<Service>> callback);

  public void addServices(Long teamId, ArrayList<Long> serviceIds, AsyncCallback<RpcStatus> callback);

  public void removeService(Long teamId, Long serviceId, AsyncCallback<RpcStatus> callback);

  public void getService(String text, AsyncCallback<ArrayList<Service>> callback);

  public void searchUsers(String name, String user, String orgunit, AsyncCallback<ArrayList<BiteUser>> callback);

}
