package at.a1ta.webclient.cucosett.client.portlet.past.widget;

import java.util.ArrayList;
import java.util.List;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.logical.shared.SelectionEvent;
import com.google.gwt.event.logical.shared.SelectionHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.SimplePanel;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.ui.client.Delegate;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.bite.ui.client.widget.ClickableIcon;
import at.a1ta.bite.ui.client.widget.WaitingWidget;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.event.GwtAddTeamMembersEvent;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.cuco.ui.common.shared.AdminAuthorityHelper;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.GwtSelectTeamMemberDialog;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class TeamMemberManagementPanel extends SimplePanel implements SelectionHandler<Integer> {

  private DataTable<BiteUser> table;

  private Widget panel = null;

  private Team team = null;

  private Button btnMember;

  private WaitingWidget waitingWidget;

  private Delegate<BiteUser> deleteMemberDelegate;

  private boolean rendered;
  private GwtSelectTeamMemberDialog obj;

  public TeamMemberManagementPanel() {
    this.setSize("100%", "100%");
    // panel = initUI();
  }

  @Override
  public void onSelection(SelectionEvent<Integer> event) {
    if (!rendered && event.getSelectedItem().intValue() == 0) {
      add(initUI());
    }
  }

  public Widget getPanel() {
    return panel;
  }

  public Widget initUI() {
    initTable();
    rendered = true;
    waitingWidget = new WaitingWidget();
    HTMLPanel pnl = new HTMLPanel("");
    pnl.setStyleName(UI.STYLES.bite_moduleContent());
    HorizontalPanel newMember = createNewMemberRow();
    pnl.add(newMember);
    pnl.add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    pnl.add(waitingWidget);
    pnl.add(table);
    deleteMemberDelegate = new Delegate<BiteUser>() {

      @Override
      public void execute(final BiteUser BiteUser) {
        final ModelData<BiteUser> m = new ModelData<BiteUser>(BiteUser);
        final BiteUser info = m.getBean();
        SettingsServiceLocator.getTeamServlet().removeTeamMember(team.getId(), info.getId(), new BaseAsyncCallback<RpcStatus>() {
          @Override
          public void onSuccess(RpcStatus result) {
            if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteMemberQuestion())) {
              waitingWidget.setText(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteTeammember());
              waitingWidget.show();
              team.getMembers().remove(info);
              waitingWidget.hide();
              loadMember();
            }
          }

          @Override
          public void onFailure(Throwable caught) {
            waitingWidget.hide();
            Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteError());
          }
        });

      }
    };

    registerUpdateMemberListener();
    registerUpdateMembersListener();
    loadMember();
    return pnl;
  }

  public void initTable() {
    table = new DataTable<BiteUser>(createColumns());
    table.enablePaging(10);
    table.setWidth("500px");
    table.setVisible(false);
  }

  private void registerUpdateMembersListener() {
    PortletEventManager.addListener(CuCoEventType.ACTIVATE_TEAM, new PortletEventListener<PortletEvent>() {
      @Override
      public void handleEvent(PortletEvent be) {
        team = (Team) be.getSource();
        loadMember();
      }
    });
  }

  public void loadMember() {
    waitingWidget.setVisible(true);
    table.setVisible(false);

    table.getStore().clear();

    if (team == null) {
      btnMember.disable();
      waitingWidget.setVisible(false);
      table.setVisible(true);
      return;
    }

    SettingsServiceLocator.getTeamServlet().getTeam(team.getId(), new BaseAsyncCallback<Team>() {
      @Override
      public void onSuccess(Team result) {
        btnMember.enable();

        ArrayList<ModelData<BiteUser>> results = new ArrayList<ModelData<BiteUser>>();

        List<BiteUser> list = result.getMembers();
        for (BiteUser user : list) {
          ModelData<BiteUser> m = new ModelData<BiteUser>(user);
          m.put("bean", user);
          m.put("name", user.getName());
          m.put("user", user.getUsername());
          m.put("orgunit", user.getManagementLevel1OrgUnitShort());
          results.add(m);
        }
        table.getStore().add(results);
        waitingWidget.setVisible(false);
        table.setVisible(true);
      }
    });
  }

  private void registerUpdateMemberListener() {

    PortletEventManager.addListener(CuCoEventType.ADDTEAM_MEMBERS, new PortletEventListener<GwtAddTeamMembersEvent>() {
      @Override
      public void handleEvent(final GwtAddTeamMembersEvent be) {
        ArrayList<Long> userIds = new ArrayList<Long>();
        for (ModelData<BiteUser> model : be.getTeamMembers()) {
          BiteUser user = model.getBean();
          userIds.add(user.getId());
        }

        SettingsServiceLocator.getTeamServlet().addTeamMembers(team.getId(), userIds, new BaseAsyncCallback<RpcStatus>() {
          @Override
          @SuppressWarnings("unchecked")
          public void onSuccess(RpcStatus result) {
            ArrayList<ModelData<BiteUser>> results = new ArrayList<ModelData<BiteUser>>();
            ArrayList<BiteUser> users = new ArrayList<BiteUser>();
            for (ModelData<BiteUser> model : be.getTeamMembers()) {
              team.getMembers().add(model.getBean());
              users.add(model.getBean());
            }
            for (BiteUser user : users) {
              ModelData<BiteUser> m = new ModelData<BiteUser>(user);
              m.put("bean", user);
              m.put("name", user.getName());
              m.put("user", user.getUsername());
              m.put("orgunit", user.getManagementLevel1OrgUnitShort());
              results.add(m);
            }
            table.getStore().add(results);
          }

          @Override
          public void onFailure(Throwable exception) {
            Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.teamAddMemberError());
          }
        });
      }
    });
  }

  private HorizontalPanel createNewMemberRow() {
    HorizontalPanel newMember = new HorizontalPanel();
    newMember.add(createMemberButton());
    return newMember;
  }

  private Widget createMemberButton() {
    rendered = true;
    btnMember = new Button(AdminUI.ADMINCOMMONTEXTPOOL.teamAddMember(), ButtonSize.Small);
    obj = new GwtSelectTeamMemberDialog();
    btnMember.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        obj.init();
        obj.show();

      }
    });
    btnMember.disable();
    if (!AdminAuthorityHelper.canAddMember(UserManager.getUserInfo())) {
      btnMember.setVisible(false);
    }
    return btnMember;
  }

  private ArrayList<Column<BiteUser>> createColumns() {
    ArrayList<Column<BiteUser>> columns = new ArrayList<Column<BiteUser>>();
    columns.add(new Column<BiteUser>("name", AdminUI.ADMINCOMMONTEXTPOOL.teamName(), "40%"));
    columns.add(new Column<BiteUser>("user", AdminUI.ADMINCOMMONTEXTPOOL.teamNtAccount(), "30%"));
    columns.add(new Column<BiteUser>("orgunit", AdminUI.ADMINCOMMONTEXTPOOL.teamOe(), "20%"));
    columns.add(new Column<BiteUser>("delete", AdminUI.ADMINCOMMONTEXTPOOL.teamDelete(), "10%", createDeleteCellRenderer()));
    return columns;
  }

  private CellRenderer<BiteUser> createDeleteCellRenderer() {
    return new CellRenderer<BiteUser>() {
      @Override
      public IsWidget render(final ModelData<BiteUser> model, String columnId, int rowId) {
        return new ClickableIcon<BiteUser>(model.getBean(), deleteMemberDelegate, UI.IMAGES.iconDelete(), null);
      }
    };
  }

}