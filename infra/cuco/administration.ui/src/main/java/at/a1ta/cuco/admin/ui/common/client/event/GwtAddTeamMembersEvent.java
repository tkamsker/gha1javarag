package at.a1ta.cuco.admin.ui.common.client.event;

import java.util.List;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.framework.ui.client.event.PortletEvent;

public class GwtAddTeamMembersEvent extends PortletEvent {

  private List<ModelData<BiteUser>> teamMembers;

  public GwtAddTeamMembersEvent(List<ModelData<BiteUser>> teamMembers) {
    super(null, CuCoEventType.ADDTEAM_MEMBERS);
    setTeamMembers(teamMembers);
  }

  public List<ModelData<BiteUser>> getTeamMembers() {
    return teamMembers;
  }

  public void setTeamMembers(List<ModelData<BiteUser>> teamMembers) {
    this.teamMembers = teamMembers;
  }
}
