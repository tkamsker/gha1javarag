package at.a1ta.cuco.admin.ui.common.client.event;

import java.util.List;

import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.framework.ui.client.event.PortletEvent;

public class SelectRolesEvent extends PortletEvent {
  private List<Role> roles;

  public SelectRolesEvent(List<Role> roles) {
    super(null, CuCoEventType.SELECT_ROLES);
    this.roles = roles;
  }

  public List<Role> getRoles() {
    return roles;
  }

}
