package at.a1ta.cuco.admin.ui.common.client.event;

import java.util.List;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.framework.ui.client.event.PortletEvent;

public class AddTeamMemberEvent extends PortletEvent {

  private List<ModelData<BiteUser>> teamMember;

  public AddTeamMemberEvent(List<ModelData<BiteUser>> teamMember) {
    super(null, CuCoEventType.ADDTEAM_MEMBERS);
    setTeamMember(teamMember);
  }

  public List<ModelData<BiteUser>> getTeamMember() {
    return teamMember;
  }

  public void setTeamMember(List<ModelData<BiteUser>> teamMember) {
    this.teamMember = teamMember;
  }
}
