package at.a1ta.cuco.admin.ui.common.client.event;

import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.framework.ui.client.event.PortletEvent;

public class AddTeamEvent extends PortletEvent {
  private Team team;

  public Team getTeam() {
    return team;
  }

  public void setTeam(Team team) {
    this.team = team;
  }

  public AddTeamEvent(Team team) {
    super(null, CuCoEventType.UPDATE_TEAMS);
    setTeam(team);
  }

}
