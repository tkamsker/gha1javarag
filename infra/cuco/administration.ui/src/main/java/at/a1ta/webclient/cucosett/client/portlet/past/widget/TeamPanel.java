package at.a1ta.webclient.cucosett.client.portlet.past.widget;

import java.util.ArrayList;
import java.util.List;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.BasePagingLoader;
import com.extjs.gxt.ui.client.data.LoadConfig;
import com.extjs.gxt.ui.client.data.PagingLoadResult;
import com.extjs.gxt.ui.client.event.BaseEvent;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.event.SelectionChangedEvent;
import com.extjs.gxt.ui.client.event.SelectionChangedListener;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.toolbar.ToolBar;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.bite.ui.client.util.DateUtils;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.ui.ImageRenderer;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.cuco.ui.common.shared.AdminAuthorityHelper;
import at.a1ta.framework.gxt.ui.FilterablePagingMemoryProxy;
import at.a1ta.framework.gxt.ui.LinkCellRenderer;
import at.a1ta.framework.gxt.ui.PagingGridContainer;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.EditTeamDialog;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class TeamPanel implements Listener<BaseEvent>, ClickHandler {

  private PagingGridContainer<ListStore<BaseModelData>, BaseModelData> gridContainer;

  private Widget panel = null;

  private FilterablePagingMemoryProxy proxy;

  public TeamPanel() {
    panel = renderTeamGrid();
  }

  public Widget getPanel() {
    return panel;
  }

  private Widget renderTeamGrid() {
    Button newBtn = new Button(AdminUI.ADMINCOMMONTEXTPOOL.teamAdd());
    newBtn.addSelectionListener(new SelectionListener<ButtonEvent>() {

      @Override
      public void componentSelected(ButtonEvent ce) {
        EditTeamDialog d = EditTeamDialog.getInstance();
        d.show();
      }
    });

    ToolBar tb = new ToolBar();
    tb.add(newBtn);

    boolean teamCRUD = AdminAuthorityHelper.canCRUDTeam(UserManager.getUserInfo());
    if (!teamCRUD) {
      newBtn.setVisible(false);
    }

    ListStore<BaseModelData> store = new ListStore<BaseModelData>();

    List<ColumnConfig> configs = new ArrayList<ColumnConfig>();

    ColumnConfig config = new ColumnConfig("name", AdminUI.ADMINCOMMONTEXTPOOL.teamName(), 100);
    if (teamCRUD) {
      config.setRenderer(new LinkCellRenderer(this));
    }
    configs.add(config);

    config = new ColumnConfig("description", AdminUI.ADMINCOMMONTEXTPOOL.teamDesc(), 100);
    configs.add(config);

    config = new ColumnConfig("creator", AdminUI.ADMINCOMMONTEXTPOOL.teamCreation(), 100);
    configs.add(config);

    config = new ColumnConfig("createDate", AdminUI.ADMINCOMMONTEXTPOOL.teamCreateDate(), 100);
    config.setDateTimeFormat(DateUtils.getDefaultDateFormat());
    configs.add(config);

    config = new ColumnConfig("delete", AdminUI.ADMINCOMMONTEXTPOOL.teamDelete(), 80);
    if (teamCRUD) {
      config.setRenderer(new ImageRenderer(ImageRenderer.DELETE, this));
    }
    configs.add(config);

    ColumnModel cm = new ColumnModel(configs);

    gridContainer = new PagingGridContainer<ListStore<BaseModelData>, BaseModelData>(store, cm, 10);
    gridContainer.setTopComponent(tb);

    gridContainer.getGrid().setAutoExpandColumn("delete");

    gridContainer.getGrid().getSelectionModel().addSelectionChangedListener(new SelectionChangedListener<BaseModelData>() {

      @Override
      public void selectionChanged(SelectionChangedEvent<BaseModelData> se) {
        Team team = null;
        if (se.getSelectedItem() != null) {
          team = (Team) se.getSelectedItem().get("bean");
        }
        GenericEvent<Void> event = new GenericEvent<Void>(team, CuCoEventType.ACTIVATE_TEAM);
        PortletEventManager.fireEvent(event);
      }
    });

    PortletEventManager.addListener(CuCoEventType.UPDATE_TEAMS, new PortletEventListener<PortletEvent>() {

      @Override
      public void handleEvent(PortletEvent be) {
        init();
      }
    });
    return gridContainer;
  }

  public void init() {
    gridContainer.getGrid().getStore().removeAll();

    SettingsServiceLocator.getTeamServlet().getAllTeams(new BaseAsyncCallback<ArrayList<Team>>() {

      @Override
      public void onSuccess(ArrayList<Team> result) {
        ArrayList<BaseModelData> results = new ArrayList<BaseModelData>();

        for (Team team : result) {
          BaseModelData model = new BaseModelData();
          model.set("bean", team);
          model.set("id", team.getId());
          model.set("name", team.getName());
          model.set("description", team.getDescription());
          model.set("creator", team.getCreator().getUsername());
          model.set("createDate", team.getCreateDate());
          results.add(model);
        }
        proxy = new FilterablePagingMemoryProxy(results);
        // loader
        BasePagingLoader<PagingLoadResult<LoadConfig>> gridloader = new BasePagingLoader<PagingLoadResult<LoadConfig>>(proxy);
        gridloader.setRemoteSort(true);
        gridContainer.getToolbar().bind(gridloader);

        ListStore<BaseModelData> store = new ListStore<BaseModelData>(gridloader);
        gridContainer.reconfigure(store);
        gridloader.load();
      }
    });

  }

  @Override
  public void handleEvent(BaseEvent be) {
    final BaseModelData md = gridContainer.getGrid().getSelectionModel().getSelectedItem();

    if (md == null) {
      return;
    }

    if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteTeamQuestion())) {
      Team team = md.get("bean");

      final MessageBox wait = MessageBox.wait(AdminUI.ADMINCOMMONTEXTPOOL.teamTeam(), AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteTeam(), AdminUI.ADMINCOMMONTEXTPOOL.teamDelete());
      wait.show();

      SettingsServiceLocator.getTeamServlet().deleteTeam(team.getId(), new BaseAsyncCallback<RpcStatus>() {

        @Override
        public void onSuccess(RpcStatus result) {
          init();
          wait.close();
        }

        @Override
        public void onFailure(Throwable exception) {
          wait.close();
          MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.teamTeam(), AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteError(), null);
        }

      });
    }

  }

  @Override
  public void onClick(ClickEvent event) {
    BaseModelData md = gridContainer.getGrid().getSelectionModel().getSelectedItem();

    if (md == null) {
      return;
    }

    EditTeamDialog d = EditTeamDialog.getInstance((Team) md.get("bean"));
    d.show();
  }
}
