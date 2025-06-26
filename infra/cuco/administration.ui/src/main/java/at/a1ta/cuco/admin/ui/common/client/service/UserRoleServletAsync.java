package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.bite.core.shared.UnknownUsernameException;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.bite.core.shared.dto.security.RoleGroup;
import at.a1ta.bite.core.shared.dto.security.RoleWithGroup;
import at.a1ta.framework.ui.client.dto.RpcStatus;

public interface UserRoleServletAsync {

  public void deleteRoleGroup(Long roleGroupId, AsyncCallback<RpcStatus> callback);

  public void getAllRoleGroups(AsyncCallback<ArrayList<RoleGroup>> callback);

  public void getAllRoles(long[] apps, AsyncCallback<ArrayList<Role>> callback);

  public void getAllRolesForSysMsg(Long userId, AsyncCallback<ArrayList<Role>> callback);

  public void getAllRolesWithGroup(Long groupId, AsyncCallback<ArrayList<RoleWithGroup>> callback);

  public void getRolesInGroupsForUser(Long userId, AsyncCallback<ArrayList<Role>> callback);

  public void getUser(String username, AsyncCallback<UserInfo> callback);

  public void searchUsers(String username, String firstName, String lastName, AsyncCallback<ArrayList<BiteUser>> callback);

  public void getUserWithRoles(String username, AsyncCallback<UserInfo> callback) throws UnknownUsernameException;

  public void saveRoleGroup(RoleGroup roleGroup, AsyncCallback<RoleGroup> callback);

  public void saveUser(UserInfo user, AsyncCallback<UserInfo> callback);

  public void saveUsers(ArrayList<UserInfo> users, AsyncCallback<RpcStatus> callback);

  public void getAllRolesNamesForGroup(String groupName, AsyncCallback<ArrayList<String>> callback);
}
