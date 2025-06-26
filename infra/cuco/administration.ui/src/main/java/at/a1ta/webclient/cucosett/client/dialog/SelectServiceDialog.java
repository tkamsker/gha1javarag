package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;
import java.util.List;

import com.extjs.gxt.ui.client.Style.HorizontalAlignment;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.BasePagingLoader;
import com.extjs.gxt.ui.client.data.LoadConfig;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.data.PagingLoadResult;
import com.extjs.gxt.ui.client.event.BaseEvent;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.event.SelectionChangedEvent;
import com.extjs.gxt.ui.client.event.SelectionChangedListener;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.google.gwt.i18n.client.NumberFormat;
import com.google.gwt.user.client.ui.FlexTable;
import com.google.gwt.user.client.ui.HasHorizontalAlignment;
import com.google.gwt.user.client.ui.HasVerticalAlignment;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.dto.ServiceModel;
import at.a1ta.cuco.admin.ui.common.client.event.AddServicesEvent;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.framework.gxt.ui.FilterablePagingMemoryProxy;
import at.a1ta.framework.gxt.ui.GridContainer;
import at.a1ta.framework.gxt.ui.PagingGridContainer;
import at.a1ta.framework.gxt.ui.ProxyFilterField;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class SelectServiceDialog extends Dialog {

  private static SelectServiceDialog _instance = null;

  private PagingGridContainer<ListStore<ServiceModel>, ServiceModel> serviceGridContainer;

  private GridContainer<ListStore<ServiceModel>, ServiceModel> selectionGridContainer;

  private ProxyFilterField<String> namefilter = null;

  private FilterablePagingMemoryProxy proxy = null;

  private Button add;

  private Button remove;

  private Team team = null;

  private static synchronized SelectServiceDialog getInstance() {
    if (_instance == null) {
      _instance = new SelectServiceDialog();
    }
    return _instance;
  }

  public static SelectServiceDialog getInstance(Team team) {
    SelectServiceDialog instance = getInstance();
    instance.team = team;
    return instance;
  }

  public SelectServiceDialog() {
    setSize(600, 650);
    setResizable(false);
    okText = AdminUI.ADMINCOMMONTEXTPOOL.dialogUse();
    cancelText = AdminUI.ADMINCOMMONTEXTPOOL.dialogCancel();
    setButtons(Dialog.OKCANCEL);
    setHeading(AdminUI.ADMINCOMMONTEXTPOOL.teamSelectServiceHeading());
    setModal(true);

    FlexTable filters = new FlexTable();
    filters.setWidth("100%");

    namefilter = new ProxyFilterField<String>() {

      @Override
      public boolean doFilter(ModelData m) {
        return m.get("name").toString().toLowerCase().contains(getValue().toLowerCase());
      }
    };
    namefilter.setWidth(200);
    filters.setWidget(0, 0, namefilter);

    add(filters);
    add(renderGrid());
    add(renderMoveButtons());
    add(renderSelectionGrid());

  }

  private Widget renderSelectionGrid() {
    List<ColumnConfig> configs = new ArrayList<ColumnConfig>();

    ColumnConfig config = new ColumnConfig("name", AdminUI.ADMINCOMMONTEXTPOOL.teamService(), 200);
    configs.add(config);

    config = new ColumnConfig("costs", AdminUI.ADMINCOMMONTEXTPOOL.teamCosts(), 100);
    config.setNumberFormat(NumberFormat.getCurrencyFormat());
    config.setAlignment(HorizontalAlignment.RIGHT);
    configs.add(config);

    ColumnModel cm = new ColumnModel(configs);

    selectionGridContainer = new GridContainer<ListStore<ServiceModel>, ServiceModel>(new ListStore<ServiceModel>(), cm, 250);
    selectionGridContainer.getGrid().setAutoExpandColumn("costs");

    selectionGridContainer.getGrid().getSelectionModel().addSelectionChangedListener(new SelectionChangedListener<ServiceModel>() {

      @Override
      public void selectionChanged(SelectionChangedEvent<ServiceModel> se) {
        if (se.getSelectedItem() != null) {
          remove.enable();
        } else {
          remove.disable();
        }
      }
    });

    selectionGridContainer.getGrid().addListener(Events.CellDoubleClick, new Listener<BaseEvent>() {

      @Override
      @SuppressWarnings("unchecked")
      public void handleEvent(BaseEvent be) {
        ServiceModel model = selectionGridContainer.getGrid().getSelectionModel().getSelectedItem();
        ((List<BaseModelData>) proxy.getData()).add(model);
        selectionGridContainer.getGrid().getStore().remove(model);

        serviceGridContainer.getGrid().getStore().getLoader().load();
        selectionGridContainer.getGrid().getView().refresh(false);
      }
    });

    return selectionGridContainer;
  }

  private Widget renderMoveButtons() {
    FlexTable table = new FlexTable();
    table.setWidth("100%");
    add = new Button(AdminUI.ADMINCOMMONTEXTPOOL.teamButtonAdd());
    add.addSelectionListener(new SelectionListener<ButtonEvent>() {

      @Override
      @SuppressWarnings("unchecked")
      public void componentSelected(ButtonEvent ce) {
        ServiceModel model = serviceGridContainer.getGrid().getSelectionModel().getSelectedItem();
        selectionGridContainer.getGrid().getStore().add(model);
        ((List<BaseModelData>) proxy.getData()).remove(model);
        serviceGridContainer.getGrid().getStore().getLoader().load();
        selectionGridContainer.getGrid().getView().refresh(false);
      }
    });
    add.disable();
    table.setWidget(0, 0, add);

    remove = new Button(AdminUI.ADMINCOMMONTEXTPOOL.teamButtonDelete());
    remove.addSelectionListener(new SelectionListener<ButtonEvent>() {

      @Override
      @SuppressWarnings("unchecked")
      public void componentSelected(ButtonEvent ce) {
        ServiceModel model = selectionGridContainer.getGrid().getSelectionModel().getSelectedItem();
        ((List<BaseModelData>) proxy.getData()).add(model);
        selectionGridContainer.getGrid().getStore().remove(model);

        serviceGridContainer.getGrid().getStore().getLoader().load();
        selectionGridContainer.getGrid().getView().refresh(false);
      }
    });
    remove.disable();
    table.setWidget(0, 1, remove);

    table.getFlexCellFormatter().setAlignment(0, 0, HasHorizontalAlignment.ALIGN_CENTER, HasVerticalAlignment.ALIGN_MIDDLE);
    table.getFlexCellFormatter().setAlignment(0, 1, HasHorizontalAlignment.ALIGN_CENTER, HasVerticalAlignment.ALIGN_MIDDLE);

    return table;
  }

  private Widget renderGrid() {
    List<ColumnConfig> configs = new ArrayList<ColumnConfig>();

    ColumnConfig config = new ColumnConfig("name", AdminUI.ADMINCOMMONTEXTPOOL.teamService(), 200);
    configs.add(config);

    config = new ColumnConfig("costs", AdminUI.ADMINCOMMONTEXTPOOL.teamCosts(), 100);
    config.setNumberFormat(NumberFormat.getCurrencyFormat());
    config.setAlignment(HorizontalAlignment.RIGHT);
    configs.add(config);

    ColumnModel cm = new ColumnModel(configs);

    serviceGridContainer = new PagingGridContainer<ListStore<ServiceModel>, ServiceModel>(new ListStore<ServiceModel>(), cm, 10, 250);
    serviceGridContainer.getGrid().setAutoExpandColumn("costs");

    serviceGridContainer.getGrid().getSelectionModel().addSelectionChangedListener(new SelectionChangedListener<ServiceModel>() {

      @Override
      public void selectionChanged(SelectionChangedEvent<ServiceModel> se) {
        if (se.getSelectedItem() != null) {
          add.enable();
        } else {
          add.disable();
        }
      }
    });

    serviceGridContainer.getGrid().addListener(Events.CellDoubleClick, new Listener<BaseEvent>() {

      @Override
      @SuppressWarnings("unchecked")
      public void handleEvent(BaseEvent be) {
        ServiceModel model = serviceGridContainer.getGrid().getSelectionModel().getSelectedItem();
        selectionGridContainer.getGrid().getStore().add(model);
        ((List<BaseModelData>) proxy.getData()).remove(model);
        serviceGridContainer.getGrid().getStore().getLoader().load();
        selectionGridContainer.getGrid().getView().refresh(false);
      }
    });

    return serviceGridContainer;
  }

  public void init() {
    serviceGridContainer.getGrid().getStore().removeAll();
    selectionGridContainer.getGrid().getStore().removeAll();

    SettingsServiceLocator.getTeamServlet().getNotLinkedServices(team.getId(), new BaseAsyncCallback<ArrayList<Service>>() {

      @Override
      public void onSuccess(ArrayList<Service> result) {
        ArrayList<ServiceModel> results = new ArrayList<ServiceModel>();

        for (Service service : result) {
          ServiceModel model = new ServiceModel(service);
          results.add(model);
        }

        proxy = new FilterablePagingMemoryProxy(results);
        // loader
        BasePagingLoader<PagingLoadResult<LoadConfig>> gridloader = new BasePagingLoader<PagingLoadResult<LoadConfig>>(proxy);
        gridloader.setRemoteSort(true);
        serviceGridContainer.getToolbar().bind(gridloader);

        namefilter.bind(gridloader);

        ListStore<ServiceModel> store = new ListStore<ServiceModel>(gridloader);
        serviceGridContainer.reconfigure(store);
        gridloader.load();
      }
    });
  }

  @Override
  protected void onButtonPressed(Button button) {
    super.onButtonPressed(button);
    if (button != null && button.equals(getButtonById(OK))) {
      List<ServiceModel> services = selectionGridContainer.getGrid().getStore().getModels();

      ArrayList<Long> serviceIds = new ArrayList<Long>();
      for (ServiceModel model : services) {
        Service service = model.getBean();
        serviceIds.add(service.getId());
      }

      SettingsServiceLocator.getTeamServlet().addServices(team.getId(), serviceIds, new BaseAsyncCallback<RpcStatus>() {

        @Override
        @SuppressWarnings("unchecked")
        public void onSuccess(RpcStatus result) {
          PortletEventManager.fireEvent(new AddServicesEvent(selectionGridContainer.getGrid().getStore().getModels()));
          hide();
        }

        @Override
        public void onFailure(Throwable exception) {
          MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.teamTeam(), AdminUI.ADMINCOMMONTEXTPOOL.teamAddServiceError(), null);
        }

      });

    }
    if (button != null && button.equals(getButtonById(CANCEL))) {
      hide();
    }
  }

  @Override
  protected void onHide() {
    namefilter.clear();
    super.onHide();
  }
}
