package at.a1ta.webclient.cucosett.client.portlet.past.widget;

import java.util.ArrayList;
import java.util.List;

import com.extjs.gxt.ui.client.Style.HorizontalAlignment;
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
import com.google.gwt.i18n.client.NumberFormat;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.SimplePanel;

import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.dto.ServiceModel;
import at.a1ta.cuco.admin.ui.common.client.event.AddServicesEvent;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.event.RemoveServicesEvent;
import at.a1ta.cuco.admin.ui.common.client.ui.ImageRenderer;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.cuco.ui.common.shared.AdminAuthorityHelper;
import at.a1ta.framework.gxt.ui.FilterablePagingMemoryProxy;
import at.a1ta.framework.gxt.ui.PagingGridContainer;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.SelectServiceDialog;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class TeamServicePanel extends SimplePanel implements SelectionHandler<Integer>, Listener<BaseEvent> {

  private PagingGridContainer<ListStore<ServiceModel>, ServiceModel> gridContainer;

  private Team team = null;

  private Button addBtn;

  private FilterablePagingMemoryProxy proxy;

  private boolean rendered;

  public TeamServicePanel() {
    this.setSize("100%", "100%");

    PortletEventManager.addListener(CuCoEventType.ACTIVATE_TEAM, new PortletEventListener<PortletEvent>() {

      @Override
      public void handleEvent(PortletEvent be) {
        team = (Team) be.getSource();
        if (rendered) {
          init();
        }
      }
    });
  }

  @Override
  public void onSelection(SelectionEvent<Integer> event) {
    if (!rendered && event.getSelectedItem().intValue() == 1) {
      add(renderTeamMemberGrid());
      init();
    }
  }

  public PagingGridContainer<ListStore<ServiceModel>, ServiceModel> getPanel() {
    return gridContainer;
  }

  private PagingGridContainer<ListStore<ServiceModel>, ServiceModel> renderTeamMemberGrid() {
    rendered = true;
    addBtn = new Button(AdminUI.ADMINCOMMONTEXTPOOL.teamAddService());
    addBtn.addSelectionListener(new SelectionListener<ButtonEvent>() {

      @Override
      public void componentSelected(ButtonEvent ce) {
        SelectServiceDialog d = SelectServiceDialog.getInstance(team);
        d.init();
        d.show();
      }
    });
    addBtn.disable();

    ToolBar tb = new ToolBar();
    tb.add(addBtn);

    boolean service = AdminAuthorityHelper.canAddService(UserManager.getUserInfo());

    if (!service) {
      addBtn.setVisible(false);
    }

    List<ColumnConfig> configs = new ArrayList<ColumnConfig>();

    ColumnConfig config = new ColumnConfig("name", AdminUI.ADMINCOMMONTEXTPOOL.teamService(), 200);
    configs.add(config);

    config = new ColumnConfig("costs", AdminUI.ADMINCOMMONTEXTPOOL.teamCosts(), 100);
    config.setNumberFormat(NumberFormat.getCurrencyFormat());
    config.setAlignment(HorizontalAlignment.RIGHT);
    configs.add(config);

    config = new ColumnConfig("delete", AdminUI.ADMINCOMMONTEXTPOOL.teamDelete(), 40);
    if (service) {
      config.setRenderer(new ImageRenderer(ImageRenderer.DELETE, this));
    }
    configs.add(config);

    ColumnModel cm = new ColumnModel(configs);

    gridContainer = new PagingGridContainer<ListStore<ServiceModel>, ServiceModel>(new ListStore<ServiceModel>(), cm, 10);
    gridContainer.setTopComponent(tb);
    gridContainer.getGrid().setAutoExpandColumn("delete");

    PortletEventManager.addListener(CuCoEventType.ADD_SERVICES, new PortletEventListener<AddServicesEvent>() {

      @Override
      public void handleEvent(final AddServicesEvent be) {
        ((ArrayList<ServiceModel>) proxy.getData()).addAll(be.getServices());
        gridContainer.getGrid().getStore().getLoader().load();
        for (ServiceModel model : be.getServices()) {
          team.getServices().add(model.getBean());
        }
      }
    });

    PortletEventManager.addListener(CuCoEventType.REMOVE_SERVICES, new PortletEventListener<RemoveServicesEvent>() {

      @Override
      public void handleEvent(RemoveServicesEvent event) {
        ((List<ServiceModel>) proxy.getData()).remove(new ServiceModel(event.getService()));
        team.getServices().remove(event.getService());
        gridContainer.getGrid().getStore().getLoader().load();
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

    addBtn.enable();

    List<ServiceModel> results = new ArrayList<ServiceModel>();

    for (Service service : team.getServices()) {
      ServiceModel model = new ServiceModel(service);
      results.add(model);
    }

    proxy = new FilterablePagingMemoryProxy(results);
    // loader
    BasePagingLoader<PagingLoadResult<LoadConfig>> gridloader = new BasePagingLoader<PagingLoadResult<LoadConfig>>(proxy);
    gridloader.setRemoteSort(true);
    gridContainer.getToolbar().bind(gridloader);

    ListStore<ServiceModel> store = new ListStore<ServiceModel>(gridloader);
    gridContainer.reconfigure(store);
    gridloader.load();
  }

  @Override
  public void handleEvent(BaseEvent be) {
    final ServiceModel md = gridContainer.getGrid().getSelectionModel().getSelectedItem();

    if (md == null) {
      return;
    }

    if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteServiceQuestion())) {
      final Service service = md.getBean();

      final MessageBox wait = MessageBox.wait(AdminUI.ADMINCOMMONTEXTPOOL.teamTeam(), AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteService(), AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteText());
      wait.show();

      SettingsServiceLocator.getTeamServlet().removeService(team.getId(), service.getId(), new BaseAsyncCallback<RpcStatus>() {

        @Override
        @SuppressWarnings("unchecked")
        public void onSuccess(RpcStatus result) {
          ((List<ServiceModel>) proxy.getData()).remove(md);
          team.getServices().remove(service);
          gridContainer.getGrid().getStore().getLoader().load();
          wait.close();

          PortletEventManager.fireEvent(new RemoveServicesEvent(service));
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
