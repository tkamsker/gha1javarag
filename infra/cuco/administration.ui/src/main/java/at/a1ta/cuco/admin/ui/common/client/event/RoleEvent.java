package at.a1ta.cuco.admin.ui.common.client.event;

import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.framework.ui.client.event.PortletEvent;

public class RoleEvent extends PortletEvent {
  public enum UpdateType {
    insert, update
  }

  private Role role;

  public RoleEvent(Role role) {
    super(null, CuCoEventType.ROLE_UPDATE);
    this.role = role;
  }

  public Role get() {
    return role;
  }

}
