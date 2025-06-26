package at.a1ta.webclient.cucosett.client.portlet;

import com.google.gwt.event.logical.shared.SelectionEvent;
import com.google.gwt.event.logical.shared.SelectionHandler;
import com.google.gwt.user.client.ui.TabPanel;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.webclient.cucosett.client.ui.SystemMessagesGrid;

public class AllMessagesPortlet extends CuCoSettBasePortlet {

  public static final String NAME = "System Messages";

  private static AllMessagesPortlet _instance;

  private SystemMessagesGrid activeGrid = new SystemMessagesGrid(0, true);

  private SystemMessagesGrid inActiveGrid = new SystemMessagesGrid(1, false);

  public static AllMessagesPortlet create(PortletDefinition portletDefinition) {
    if (_instance == null) {
      _instance = new AllMessagesPortlet(portletDefinition);
    }
    return _instance;
  }

  private AllMessagesPortlet(PortletDefinition portletDefinition) {
    super(portletDefinition);

    TabPanel tabPanel = createTabPanel();
    add(tabPanel);
    tabPanel.addSelectionHandler(new SelectionHandler<Integer>() {

      @Override
      public void onSelection(SelectionEvent<Integer> event) {
        if (event.getSelectedItem() == 0) {
          boolean dirty = inActiveGrid.isDirty();
          activeGrid.setDirty(dirty);
          inActiveGrid.setDirty(false);
        } else {
          boolean dirty = activeGrid.isDirty();
          inActiveGrid.setDirty(dirty);
          activeGrid.setDirty(false);
        }
      }
    });

    tabPanel.addSelectionHandler(activeGrid);
    tabPanel.addSelectionHandler(inActiveGrid);
    tabPanel.selectTab(0);
  }

  private TabPanel createTabPanel() {
    TabPanel tabPanel = new TabPanel();
    tabPanel.setSize("100%", "100%");
    tabPanel.add(activeGrid, "<div class=\"tab-l\"><div class=\"tab-r\"><div class=\"tab-c\"><div class=\"tab-body\">" + AdminUI.ADMINCOMMONTEXTPOOL.smActive() + "</div></div></div></div>", true);
    tabPanel.add(inActiveGrid, "<div class=\"tab-l\"><div class=\"tab-r\"><div class=\"tab-c\"><div class=\"tab-body\">" + AdminUI.ADMINCOMMONTEXTPOOL.smInactive() + "</div></div></div></div>", true);
    return tabPanel;
  }

  @Override
  public void init() {
    showLoading();
    showContent();
  }

}
