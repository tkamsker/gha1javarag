package at.a1ta.cuco.admin.ui.common.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.bite.core.shared.UnknownUsernameException;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.bite.core.shared.dto.security.RoleGroup;
import at.a1ta.bite.core.shared.dto.security.RoleWithGroup;
import at.a1ta.framework.ui.client.dto.RpcStatus;

@RemoteServiceRelativePath("cuco/role.rpc")
public interface UserRoleServlet extends RemoteService {

  public RpcStatus deleteRoleGroup(Long roleGroupId);

  public ArrayList<RoleGroup> getAllRoleGroups();

  public ArrayList<Role> getAllRoles(long[] apps);

  public ArrayList<Role> getAllRolesForSysMsg(Long userId);

  public ArrayList<RoleWithGroup> getAllRolesWithGroup(Long groupId);

  public ArrayList<String> getAllRolesNamesForGroup(String groupName);

  public ArrayList<Role> getRolesInGroupsForUser(Long userId);

  public UserInfo getUser(String username);

  public ArrayList<BiteUser> searchUsers(String username, String firstName, String lastName);

  public UserInfo getUserWithRoles(String username) throws UnknownUsernameException;

  public RoleGroup saveRoleGroup(RoleGroup roleGroup);

  public UserInfo saveUser(UserInfo user);

  public RpcStatus saveUsers(ArrayList<UserInfo> users);
}
