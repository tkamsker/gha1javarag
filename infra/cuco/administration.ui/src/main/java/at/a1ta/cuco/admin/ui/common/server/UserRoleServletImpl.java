package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.annotation.WebServlet;
import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.core.server.service.RoleGroupService;
import at.a1ta.bite.core.server.service.RoleService;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.server.service.UserService;
import at.a1ta.bite.core.shared.UnknownUsernameException;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.bite.core.shared.dto.security.RoleGroup;
import at.a1ta.bite.core.shared.dto.security.RoleWithGroup;
import at.a1ta.bite.ui.server.servlet.AuthenticationServlet;
import at.a1ta.cuco.admin.ui.common.client.service.UserRoleServlet;
import at.a1ta.framework.ui.client.dto.RpcStatus;

@WebServlet(name = "userRole", urlPatterns = {"/admin/cuco/role.rpc"})
public class UserRoleServletImpl extends AuthenticationServlet implements UserRoleServlet {
  // @formatter:off
  @Autowired
  private SettingService settingService;
  @Autowired
  private RoleGroupService roleGroupService;
  @Autowired
  private RoleService roleService;
  @Autowired
  private UserService userService;

  // @formatter:on

  @Override
  public RpcStatus deleteRoleGroup(Long roleGroupId) {
    roleGroupService.deleteRoleGroup(roleGroupId);
    return RpcStatus.OK;
  }

  @Override
  public ArrayList<RoleGroup> getAllRoleGroups() {
    return (ArrayList<RoleGroup>) roleGroupService.getAllRoleGroups();
  }

  @Override
  public ArrayList<Role> getAllRoles(long[] apps) {
    ArrayList<Role> all = new ArrayList<Role>(roleService.getAllRoles());
    return all;
  }

  @Override
  public ArrayList<Role> getAllRolesForSysMsg(Long userId) {
    return (ArrayList<Role>) roleService.getAllRolesForSysMsg(userId, settingService.getValue("SYSMSG_GROUPS"));
  }

  @Override
  public ArrayList<RoleWithGroup> getAllRolesWithGroup(Long groupId) {
    return (ArrayList<RoleWithGroup>) roleService.getAllRolesWithGroup(groupId);
  }

  @Override
  public ArrayList<Role> getRolesInGroupsForUser(Long userId) {
    return (ArrayList<Role>) roleService.getAllRolesWithGroupForUser(userId, settingService.getValue("ROLE_GROUPS"));
  }

  @Override
  public UserInfo getUser(String username) {
    return userService.getByUsername(username);
  }

  @Override
  public ArrayList<BiteUser> searchUsers(String username, String firstName, String lastName) {
    ArrayList<BiteUser> ret = new ArrayList<BiteUser>(userService.searchUsers(username, firstName, lastName));
    return ret;
  }

  @Override
  public UserInfo getUserWithRoles(String username) throws UnknownUsernameException {
    return userService.getUserWithRoles(username);
  }

  @Override
  public RoleGroup saveRoleGroup(RoleGroup rg) {
    roleGroupService.saveRoleGroup(rg);
    roleGroupService.updateRolesForRoleGroup(rg);
    roleService.updateAuthForRole(rg);
    return rg;
  }

  @Override
  public UserInfo saveUser(UserInfo user) {
    userService.saveUser(user, getAuthenticatedUser());

    return user;
  }

  @Override
  public RpcStatus saveUsers(ArrayList<UserInfo> users) {
    userService.saveUsers(users, getAuthenticatedUser());

    return RpcStatus.OK;
  }

  @Override
  public ArrayList<String> getAllRolesNamesForGroup(String groupName) {
    return roleService.getAllRolesNamesForGroup(groupName);
  }

}
