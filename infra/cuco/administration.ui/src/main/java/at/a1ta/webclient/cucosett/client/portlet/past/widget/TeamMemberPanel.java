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
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.toolbar.ToolBar;
import com.google.gwt.event.logical.shared.SelectionEvent;
import com.google.gwt.event.logical.shared.SelectionHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.SimplePanel;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.AddTeamMembersEvent;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.ui.ImageRenderer;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.cuco.ui.common.shared.AdminAuthorityHelper;
import at.a1ta.framework.gxt.ui.FilterablePagingMemoryProxy;
import at.a1ta.framework.gxt.ui.PagingGridContainer;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.GwtSelectTeamMemberDialog;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class TeamMemberPanel extends SimplePanel implements SelectionHandler<Integer>, Listener<BaseEvent> {

  private PagingGridContainer<ListStore<BaseModelData>, BaseModelData> gridContainer;
  private Team team = null;
  private Button addBtn;
  private FilterablePagingMemoryProxy proxy;
  private boolean rendered;

  public TeamMemberPanel() {
    this.setSize("100%", "100%");
  }

  @Override
  public void onSelection(SelectionEvent<Integer> event) {
    if (!rendered && event.getSelectedItem().intValue() == 0) {
      add(renderTeamMemberGrid());
    }
  }

  public PagingGridContainer<ListStore<BaseModelData>, BaseModelData> getPanel() {
    return gridContainer;
  }

  private PagingGridContainer<ListStore<BaseModelData>, BaseModelData> renderTeamMemberGrid() {
    rendered = true;
    addBtn = new Button(AdminUI.ADMINCOMMONTEXTPOOL.teamAddMember());
    addBtn.addSelectionListener(new SelectionListener<ButtonEvent>() {
      @Override
      public void componentSelected(ButtonEvent ce) {
        GwtSelectTeamMemberDialog d = GwtSelectTeamMemberDialog.getInstance();
        d.init();
        d.show();
      }
    });
    addBtn.disable();

    boolean teamMember = AdminAuthorityHelper.canAddMember(UserManager.getUserInfo());

    ToolBar tb = new ToolBar();
    tb.add(addBtn);
    if (!teamMember) {
      addBtn.setVisible(false);
    }

    List<ColumnConfig> configs = new ArrayList<ColumnConfig>();

    ColumnConfig config = new ColumnConfig("name", AdminUI.ADMINCOMMONTEXTPOOL.teamName(), 100);
    configs.add(config);

    config = new ColumnConfig("user", AdminUI.ADMINCOMMONTEXTPOOL.teamNtAccount(), 80);
    configs.add(config);

    config = new ColumnConfig("orgunit", AdminUI.ADMINCOMMONTEXTPOOL.teamOe(), 40);
    configs.add(config);

    config = new ColumnConfig("delete", AdminUI.ADMINCOMMONTEXTPOOL.teamDelete(), 40);
    if (teamMember) {
      config.setRenderer(new ImageRenderer(ImageRenderer.DELETE, this));
    }
    configs.add(config);

    ColumnModel cm = new ColumnModel(configs);

    gridContainer = new PagingGridContainer<ListStore<BaseModelData>, BaseModelData>(new ListStore<BaseModelData>(), cm, 10);
    gridContainer.setTopComponent(tb);

    gridContainer.getGrid().setAutoExpandColumn("delete");

    PortletEventManager.addListener(CuCoEventType.ACTIVATE_TEAM, new PortletEventListener<PortletEvent>() {
      @Override
      public void handleEvent(PortletEvent be) {
        team = (Team) be.getSource();
        init();
      }
    });

    PortletEventManager.addListener(CuCoEventType.ADDTEAM_MEMBERS, new PortletEventListener<AddTeamMembersEvent>() {
      @Override
      public void handleEvent(final AddTeamMembersEvent be) {
        ArrayList<Long> userIds = new ArrayList<Long>();
        for (BaseModelData model : be.getTeamMembers()) {
          BiteUser user = model.get("bean");
          userIds.add(user.getId());
        }

        SettingsServiceLocator.getTeamServlet().addTeamMembers(team.getId(), userIds, new BaseAsyncCallback<RpcStatus>() {
          @Override
          @SuppressWarnings("unchecked")
          public void onSuccess(RpcStatus result) {
            ((ArrayList<BaseModelData>) proxy.getData()).addAll(be.getTeamMembers());
            gridContainer.getGrid().getStore().getLoader().load();
            for (BaseModelData model : be.getTeamMembers()) {
              BiteUser user = model.get("bean");
              team.getMembers().add(user);
            }
          }

          @Override
          public void onFailure(Throwable exception) {
            MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.teamTeam(), AdminUI.ADMINCOMMONTEXTPOOL.teamAddMemberError(), null);
          }
        });
      }
    });
    return gridContainer;
  }

  private void init() {
    gridContainer.getGrid().getStore().removeAll();

    if (team == null) {
      addBtn.disable();
      return;
    }

    SettingsServiceLocator.getTeamServlet().getTeam(team.getId(), new BaseAsyncCallback<Team>() {
      @Override
      public void onSuccess(Team result) {
        addBtn.enable();

        List<BaseModelData> results = new ArrayList<BaseModelData>();

        List<BiteUser> list = result.getMembers();
        for (BiteUser user : list) {
          BaseModelData model = new BaseModelData();
          model.set("bean", user);
          model.set("name", user.getName());
          model.set("user", user.getUsername());
          model.set("orgunit", user.getManagementLevel1OrgUnitShort());
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

    if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteMemberQuestion())) {
      final UserInfo info = md.get("bean");

      final MessageBox wait = MessageBox.wait(AdminUI.ADMINCOMMONTEXTPOOL.teamTeam(), AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteTeammember(), AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteText());
      wait.show();

      SettingsServiceLocator.getTeamServlet().removeTeamMember(team.getId(), info.getId(), new BaseAsyncCallback<RpcStatus>() {
        @Override
        @SuppressWarnings("unchecked")
        public void onSuccess(RpcStatus result) {
          ((List<BaseModelData>) proxy.getData()).remove(md);
          team.getMembers().remove(info);
          gridContainer.getGrid().getStore().getLoader().load();
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
}
