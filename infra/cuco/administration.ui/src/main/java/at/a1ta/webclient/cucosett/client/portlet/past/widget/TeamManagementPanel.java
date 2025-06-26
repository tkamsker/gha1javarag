package at.a1ta.webclient.cucosett.client.portlet.past.widget;

import java.util.ArrayList;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Anchor;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.ui.client.Delegate;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.bite.ui.client.widget.ClickableIcon;
import at.a1ta.bite.ui.client.widget.WaitingWidget;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.AddTeamEvent;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.cuco.ui.common.client.ui.ClickListener;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.EditTeamsDialog;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class TeamManagementPanel {

  private DataTable<Team> table;

  private Widget panel = null;

  private WaitingWidget waitingWidget;

  private Delegate<Team> deleteTeamDelegate;

  private EditTeamsDialog editTeamDialog;

  public TeamManagementPanel() {
    panel = initUI();
    table.addClickListener(new ClickListener<Team>() {
      @Override
      public void onClick(ModelData<Team> data) {
        Team team = null;
        if (data.getBean().getId() != null) {
          team = data.getBean();
        }
        GenericEvent<Void> event = new GenericEvent<Void>(team, CuCoEventType.ACTIVATE_TEAM);
        PortletEventManager.fireEvent(event);
      }
    });
  }

  public Widget getPanel() {
    return panel;
  }

  public Widget initUI() {
    initTable();
    waitingWidget = new WaitingWidget();
    HTMLPanel pnl = new HTMLPanel("");
    pnl.setStyleName(UI.STYLES.bite_moduleContent());
    HorizontalPanel newTeam = createNewTeamRow();
    pnl.add(newTeam);
    pnl.add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    pnl.add(waitingWidget);
    pnl.add(table);
    deleteTeamDelegate = new Delegate<Team>() {
      @Override
      public void execute(final Team team) {
        SettingsServiceLocator.getTeamServlet().deleteTeam(team.getId(), new BaseAsyncCallback<RpcStatus>() {
          @Override
          public void onSuccess(RpcStatus result) {
            if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteTeamQuestion())) {
              ModelData<Team> m = new ModelData<Team>(team);
              waitingWidget.setText(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteTeam());
              waitingWidget.show();
              m.remove(team);
              waitingWidget.hide();
              loadTeam();
            }
          }

          @Override
          public void onFailure(Throwable caught) {
            waitingWidget.hide();
            Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.messageboxDeleteError());
          }
        });

      }
    };
    registerUpdateTeamListener();
    registerUpdateTeamsListener();

    // loadTeam();
    return pnl;
    // showContent();
  }

  public void initTable() {
    table = new DataTable<Team>(createColumns());
    table.enablePaging(10);
    table.setWidth("700px");
    table.setVisible(false);
  }

  private void registerUpdateTeamsListener() {
    PortletEventManager.addListener(CuCoEventType.UPDATE_TEAMS, new PortletEventListener<AddTeamEvent>() {

      @Override
      public void handleEvent(AddTeamEvent be) {
        loadTeam();
      }
    });
  }

  public void loadTeam() {
    waitingWidget.setVisible(true);
    table.setVisible(false);

    table.getStore().clear();

    SettingsServiceLocator.getTeamServlet().getAllTeams(new BaseAsyncCallback<ArrayList<Team>>() {

      @Override
      public void onSuccess(ArrayList<Team> result) {
        ArrayList<ModelData<Team>> results = new ArrayList<ModelData<Team>>();

        for (Team team : result) {
          ModelData<Team> m = new ModelData<Team>(team);
          m.put("bean", team);
          m.put("id", team.getId());
          m.put("name", team.getName());
          m.put("description", team.getDescription());
          m.put("creator", team.getCreator().getUsername());
          m.put("createDate", team.getCreateDate());
          results.add(m);
        }

        table.getStore().add(results);
        waitingWidget.setVisible(false);
        table.setVisible(true);
      }
    });
  }

  private void registerUpdateTeamListener() {
    PortletEventManager.addListener(CuCoEventType.UPDATE_TEAMS, new PortletEventListener<AddTeamEvent>() {

      @Override
      public void handleEvent(AddTeamEvent event) {
        Team team = event.getTeam();
        ModelData<Team> model = table.getStore().get(team);
        if (model != null) {
          model.setBean(team);
        } else {
          model = new ModelData<Team>(team);
          model.put("bean", team);
          model.put("id", team.getId());
          model.put("name", team.getName());
          model.put("description", team.getDescription());
          model.put("creator", team.getCreator().getUsername());
          model.put("createDate", team.getCreateDate());
          table.getStore().add(model);
        }
      }
    });
  }

  private HorizontalPanel createNewTeamRow() {
    HorizontalPanel newTeam = new HorizontalPanel();
    newTeam.add(createTeamButton());
    return newTeam;
  }

  private Widget createTeamButton() {
    Button btnTeam = new Button(AdminUI.ADMINCOMMONTEXTPOOL.teamAdd(), ButtonSize.Small);
    editTeamDialog = new EditTeamsDialog();

    btnTeam.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        editTeamDialog.show(null);
      }
    });
    return btnTeam;
  }

  private ArrayList<Column<Team>> createColumns() {
    ArrayList<Column<Team>> columns = new ArrayList<Column<Team>>();
    columns.add(new Column<Team>("name", AdminUI.ADMINCOMMONTEXTPOOL.teamName(), "20%", createTeamCellRenderer()));
    columns.add(new Column<Team>("description", AdminUI.ADMINCOMMONTEXTPOOL.teamDesc(), "30%"));
    columns.add(new Column<Team>("creator", AdminUI.ADMINCOMMONTEXTPOOL.teamCreation(), "20%"));
    columns.add(new Column<Team>("createDate", AdminUI.ADMINCOMMONTEXTPOOL.teamCreateDate(), "20%"));
    columns.add(new Column<Team>("delete", AdminUI.ADMINCOMMONTEXTPOOL.teamDelete(), "10%", createDeleteCellRenderer()));
    return columns;
  }

  private CellRenderer<Team> createTeamCellRenderer() {
    return new CellRenderer<Team>() {
      @Override
      public Widget render(final ModelData<Team> model, String columnId, int rowId) {
        Anchor link = new Anchor(model.getBean().getName());
        link.addClickHandler(new ClickHandler() {
          @Override
          public void onClick(ClickEvent event) {
            editTeamDialog.show(model.getBean());

          }
        });
        return link;
      }
    };
  }

  private CellRenderer<Team> createDeleteCellRenderer() {
    return new CellRenderer<Team>() {
      @Override
      public IsWidget render(final ModelData<Team> model, String columnId, int rowId) {
        return new ClickableIcon<Team>(model.getBean(), deleteTeamDelegate, UI.IMAGES.iconDelete(), null);
      }
    };
  }

  // @Override
  // public void init() {}
}
