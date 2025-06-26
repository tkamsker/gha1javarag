package at.a1ta.webclient.cucosett.client.portlet.past;

import com.google.gwt.user.client.ui.FlexTable;
import com.google.gwt.user.client.ui.HasHorizontalAlignment;
import com.google.gwt.user.client.ui.HasVerticalAlignment;
import com.google.gwt.user.client.ui.TabPanel;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.framework.ui.client.util.HtmlUtils;
import at.a1ta.webclient.cucosett.client.portlet.CuCoSettBasePortlet;
import at.a1ta.webclient.cucosett.client.portlet.past.widget.TeamMemberPanel;
import at.a1ta.webclient.cucosett.client.portlet.past.widget.TeamPanel;
import at.a1ta.webclient.cucosett.client.portlet.past.widget.TeamServicePanel;

public class TeamPortlet extends CuCoSettBasePortlet {

  public static final String NAME = "PaST TeamsOld";

  private static TeamPortlet _instance;

  private TeamPanel teamPanel;

  private TeamMemberPanel teamMemberPanel;

  private TeamServicePanel teamServicePanel;

  private FlexTable table = new FlexTable();

  public static TeamPortlet create(PortletDefinition portletDefinition) {
    if (_instance == null) {
      _instance = new TeamPortlet(portletDefinition);
    }
    return _instance;
  }

  private TeamPortlet(PortletDefinition def) {
    super(def);
    teamPanel = new TeamPanel();
    teamMemberPanel = new TeamMemberPanel();
    teamServicePanel = new TeamServicePanel();

    table.setWidth("100%");
    table.setWidget(0, 0, teamPanel.getPanel());
    table.getFlexCellFormatter().setAlignment(0, 0, HasHorizontalAlignment.ALIGN_LEFT, HasVerticalAlignment.ALIGN_TOP);
    table.getFlexCellFormatter().setWidth(0, 0, "50%");

    final TabPanel panel = new TabPanel();
    panel.setWidth("500px");

    panel.add(teamMemberPanel, "<div class=\"tab-l\"><div class=\"tab-r\"><div class=\"tab-c\"><div class=\"tab-body\">" + "Teammitglieder" + "</div></div></div></div>", true);
    panel.add(teamServicePanel, "<div class=\"tab-l\"><div class=\"tab-r\"><div class=\"tab-c\"><div class=\"tab-body\">" + "Dienstleistungen" + "</div></div></div></div>", true);
    table.getFlexCellFormatter().setAlignment(0, 1, HasHorizontalAlignment.ALIGN_LEFT, HasVerticalAlignment.ALIGN_TOP);
    table.getFlexCellFormatter().setWidth(0, 1, "50%");

    add(table);
    add(HtmlUtils.createLink("pastExport?what=agents", "Export", true));

    panel.addSelectionHandler(teamMemberPanel);
    panel.addSelectionHandler(teamServicePanel);
    table.setWidget(0, 1, panel);

    panel.selectTab(0);
  }

  @Override
  public void init() {
    showLoading();
    teamPanel.init();
    showContent();

  }

}
