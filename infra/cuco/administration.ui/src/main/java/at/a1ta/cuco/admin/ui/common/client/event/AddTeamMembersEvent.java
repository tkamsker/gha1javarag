package at.a1ta.cuco.admin.ui.common.client.event;

import java.util.List;

import com.extjs.gxt.ui.client.data.BaseModelData;

import at.a1ta.framework.ui.client.event.PortletEvent;

public class AddTeamMembersEvent extends PortletEvent {
  private List<BaseModelData> teamMembers;

  public AddTeamMembersEvent(List<BaseModelData> teamMembers) {
    super(null, CuCoEventType.ADDTEAM_MEMBERS);
    setTeamMembers(teamMembers);
  }

  public List<BaseModelData> getTeamMembers() {
    return teamMembers;
  }

  public void setTeamMembers(List<BaseModelData> teamMembers) {
    this.teamMembers = teamMembers;
  }
}
