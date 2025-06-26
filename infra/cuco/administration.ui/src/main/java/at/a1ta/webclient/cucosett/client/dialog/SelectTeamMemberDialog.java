package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;
import java.util.List;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.BasePagingLoader;
import com.extjs.gxt.ui.client.data.LoadConfig;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.data.PagingLoadResult;
import com.extjs.gxt.ui.client.event.BaseEvent;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.GridEvent;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.event.SelectionChangedEvent;
import com.extjs.gxt.ui.client.event.SelectionChangedListener;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.google.gwt.user.client.ui.FlexTable;
import com.google.gwt.user.client.ui.HasHorizontalAlignment;
import com.google.gwt.user.client.ui.HasVerticalAlignment;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.AddTeamMembersEvent;
import at.a1ta.framework.gxt.ui.FilterablePagingMemoryProxy;
import at.a1ta.framework.gxt.ui.GridContainer;
import at.a1ta.framework.gxt.ui.PagingGridContainer;
import at.a1ta.framework.gxt.ui.ProxyFilterField;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class SelectTeamMemberDialog extends Dialog {

  private static SelectTeamMemberDialog _instance = null;
  private PagingGridContainer<ListStore<BaseModelData>, BaseModelData> teamGridContainer;
  private GridContainer<ListStore<BaseModelData>, BaseModelData> selectionGridContainer;
  private ProxyFilterField<String> namefilter = null;
  private ProxyFilterField<String> userfilter = null;
  private ProxyFilterField<String> oefilter = null;
  private FilterablePagingMemoryProxy proxy = null;
  private Button add;
  private Button remove;

  public static synchronized SelectTeamMemberDialog getInstance() {
    if (_instance == null) {
      _instance = new SelectTeamMemberDialog();
    }
    return _instance;
  }

  public SelectTeamMemberDialog() {
    setSize(600, 650);
    setResizable(false);
    okText = AdminUI.ADMINCOMMONTEXTPOOL.dialogUse();
    cancelText = AdminUI.ADMINCOMMONTEXTPOOL.dialogCancel();
    setButtons(Dialog.OKCANCEL);
    setHeading(AdminUI.ADMINCOMMONTEXTPOOL.teamSelectMemberDialog());
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

    userfilter = new ProxyFilterField<String>() {

      @Override
      public boolean doFilter(ModelData m) {
        return m.get("user").toString().toLowerCase().contains(getValue().toLowerCase());
      }
    };
    userfilter.setWidth(150);
    filters.setWidget(0, 1, userfilter);

    oefilter = new ProxyFilterField<String>() {

      @Override
      public boolean doFilter(ModelData m) {
        if (m.get("orgunit") == null) {
          return false;
        }
        return m.get("orgunit").toString().toLowerCase().contains(getValue().toLowerCase());
      }
    };
    oefilter.setWidth(150);
    filters.setWidget(0, 2, oefilter);

    add(filters);
    add(renderGrid());
    add(renderMoveButtons());
    add(renderSelectionGrid());

  }

  private Widget renderSelectionGrid() {
    List<ColumnConfig> configs = new ArrayList<ColumnConfig>();

    ColumnConfig config = new ColumnConfig("name", AdminUI.ADMINCOMMONTEXTPOOL.teamName(), 100);
    configs.add(config);

    config = new ColumnConfig("user", AdminUI.ADMINCOMMONTEXTPOOL.teamNtAccount(), 80);
    configs.add(config);

    config = new ColumnConfig("orgunit", AdminUI.ADMINCOMMONTEXTPOOL.teamOe(), 40);
    configs.add(config);

    ColumnModel cm = new ColumnModel(configs);

    selectionGridContainer = new GridContainer<ListStore<BaseModelData>, BaseModelData>(new ListStore<BaseModelData>(), cm, 250);
    selectionGridContainer.getGrid().setAutoExpandColumn("orgunit");

    selectionGridContainer.getGrid().getSelectionModel().addSelectionChangedListener(new SelectionChangedListener<BaseModelData>() {
      @Override
      public void selectionChanged(SelectionChangedEvent<BaseModelData> se) {
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
        if (!(be instanceof GridEvent)) {
          return;
        }
        GridEvent<BaseModelData> ge = (GridEvent<BaseModelData>) be;

        BaseModelData model = ge.getModel();
        ((List<BaseModelData>) proxy.getData()).add(model);
        selectionGridContainer.getGrid().getStore().remove(model);

        teamGridContainer.getGrid().getStore().getLoader().load();
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
        BaseModelData model = teamGridContainer.getGrid().getSelectionModel().getSelectedItem();
        selectionGridContainer.getGrid().getStore().add(model);
        ((List<BaseModelData>) proxy.getData()).remove(model);
        teamGridContainer.getGrid().getStore().getLoader().load();
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
        BaseModelData model = selectionGridContainer.getGrid().getSelectionModel().getSelectedItem();
        ((List<BaseModelData>) proxy.getData()).add(model);
        selectionGridContainer.getGrid().getStore().remove(model);

        teamGridContainer.getGrid().getStore().getLoader().load();
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

    ColumnConfig config = new ColumnConfig("name", AdminUI.ADMINCOMMONTEXTPOOL.teamName(), 100);
    configs.add(config);

    config = new ColumnConfig("user", AdminUI.ADMINCOMMONTEXTPOOL.teamNtAccount(), 80);
    configs.add(config);

    config = new ColumnConfig("orgunit", AdminUI.ADMINCOMMONTEXTPOOL.teamOe(), 40);
    configs.add(config);

    ColumnModel cm = new ColumnModel(configs);

    teamGridContainer = new PagingGridContainer<ListStore<BaseModelData>, BaseModelData>(new ListStore<BaseModelData>(), cm, 10, 250);
    teamGridContainer.getGrid().setAutoExpandColumn("orgunit");

    teamGridContainer.getGrid().getSelectionModel().addSelectionChangedListener(new SelectionChangedListener<BaseModelData>() {
      @Override
      public void selectionChanged(SelectionChangedEvent<BaseModelData> se) {
        if (se.getSelectedItem() != null) {
          add.enable();
        } else {
          add.disable();
        }
      }
    });

    teamGridContainer.getGrid().addListener(Events.CellDoubleClick, new Listener<BaseEvent>() {
      @Override
      @SuppressWarnings("unchecked")
      public void handleEvent(BaseEvent be) {
        if (!(be instanceof GridEvent)) {
          return;
        }
        GridEvent<BaseModelData> ge = (GridEvent<BaseModelData>) be;

        BaseModelData model = ge.getModel();
        selectionGridContainer.getGrid().getStore().add(model);
        ((List<BaseModelData>) proxy.getData()).remove(model);
        teamGridContainer.getGrid().getStore().getLoader().load();
        selectionGridContainer.getGrid().getView().refresh(false);

      }
    });
    return teamGridContainer;
  }

  public void init() {
    teamGridContainer.getGrid().getStore().removeAll();
    selectionGridContainer.getGrid().getStore().removeAll();

    SettingsServiceLocator.getTeamServlet().getAllUsers(new BaseAsyncCallback<ArrayList<BiteUser>>() {
      @Override
      public void onSuccess(ArrayList<BiteUser> result) {
        ArrayList<BaseModelData> results = new ArrayList<BaseModelData>();

        for (BiteUser user : result) {
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
        teamGridContainer.getToolbar().bind(gridloader);

        namefilter.bind(gridloader);
        userfilter.bind(gridloader);
        oefilter.bind(gridloader);

        ListStore<BaseModelData> store = new ListStore<BaseModelData>(gridloader);
        teamGridContainer.reconfigure(store);
        gridloader.load();
      }
    });
  }

  @Override
  protected void onButtonPressed(Button button) {
    super.onButtonPressed(button);
    if (button != null && button.equals(getButtonById(OK))) {
      PortletEventManager.fireEvent(new AddTeamMembersEvent(selectionGridContainer.getGrid().getStore().getModels()));
      hide();
    }
    if (button != null && button.equals(getButtonById(CANCEL))) {
      hide();
    }
  }
}
