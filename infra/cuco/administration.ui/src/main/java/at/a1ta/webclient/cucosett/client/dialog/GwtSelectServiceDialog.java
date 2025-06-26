package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;
import java.util.List;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.ui.client.PopupFrame;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.WaitingWidget;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.dto.ServiceModel;
import at.a1ta.cuco.admin.ui.common.client.event.AddServicesEvent;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.cuco.ui.common.client.ui.ClickListener;
import at.a1ta.cuco.ui.common.client.ui.DoubleClickListener;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class GwtSelectServiceDialog extends Composite {

  private static GwtSelectServiceDialogUiBinder uiBinder = GWT.create(GwtSelectServiceDialogUiBinder.class);

  interface GwtSelectServiceDialogUiBinder extends UiBinder<Widget, GwtSelectServiceDialog> {}

  private static GwtSelectServiceDialog _instance = null;

  @UiField(provided = true)
  DataTable<ServiceModel> table;
  @UiField
  InputBox service;
  @UiField
  Button add;
  @UiField
  Button remove;
  @UiField
  Button bSave;
  @UiField
  Button bCancel;
  private Team team = null;
  @UiField
  Button bSearch;

  @UiField(provided = true)
  DataTable<ServiceModel> table2;

  private ModelData<ServiceModel> modeldata;
  private PopupFrame popupFrame;
  private WaitingWidget waitingWidget;

  public static synchronized GwtSelectServiceDialog getInstance() {
    if (_instance == null) {
      _instance = new GwtSelectServiceDialog();
    }
    return _instance;
  }

  public static GwtSelectServiceDialog getInstance(Team team) {
    GwtSelectServiceDialog instance = getInstance();
    instance.team = team;
    return instance;
  }

  public GwtSelectServiceDialog() {
    initTable();
    initWidget(uiBinder.createAndBindUi(this));
    renderSelectionGrid();
    renderTeamGrid();
    renderMoveButtons();
    bSave.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        save();
      }
    });

    bCancel.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        cancel();
      }

      private void cancel() {
        popupFrame.close();
      }
    });

    bSearch.addClickHandler(new ClickHandler() {

      @Override
      public void onClick(ClickEvent event) {
        search();
      }
    });

    popupFrame = new PopupFrame(this, 600, 570);
  }

  private void initTable() {
    waitingWidget = new WaitingWidget();
    table = new DataTable<ServiceModel>(createColumns());
    table.enablePaging(10);
    table.setWidth("550px");
    table.setVisible(true);
    table2 = new DataTable<ServiceModel>(createColumns());
    table2.enablePaging(10);
    table2.setWidth("550px");
    table2.setVisible(true);
  }

  private ArrayList<Column<ServiceModel>> createColumns() {
    ArrayList<Column<ServiceModel>> columns = new ArrayList<Column<ServiceModel>>();
    columns.add(new Column<ServiceModel>("service", AdminUI.ADMINCOMMONTEXTPOOL.teamService(), "70%"));
    columns.add(new Column<ServiceModel>("costs", AdminUI.ADMINCOMMONTEXTPOOL.teamCosts(), "30%"));
    return columns;
  }

  public void renderSelectionGrid() {
    table.addClickListener(new ClickListener<ServiceModel>() {

      @Override
      public void onClick(ModelData<ServiceModel> data) {
        if (data != null) {
          modeldata = data;
          add.enable();
        } else {
          add.disable();
        }
      }
    });

    table.addDoubleClickListener(new DoubleClickListener<ServiceModel>() {

      @Override
      public void onDoubleClick(ModelData<ServiceModel> data) {
        add.disable();
        table2.getStore().add(data);
        ArrayList<ModelData<ServiceModel>> changed = new ArrayList<ModelData<ServiceModel>>();
        changed.addAll(table.getStore().getAll());
        table.getStore().clear();
        changed.remove(data);
        table.getStore().add(changed);
        table2.setVisible(true);
      }
    });
  }

  public void renderTeamGrid() {
    table2.addClickListener(new ClickListener<ServiceModel>() {

      @Override
      public void onClick(ModelData<ServiceModel> data) {
        if (data != null) {
          modeldata = data;
          remove.enable();
        } else {
          remove.disable();
        }
      }
    });

    table2.addDoubleClickListener(new DoubleClickListener<ServiceModel>() {

      @Override
      public void onDoubleClick(ModelData<ServiceModel> data) {
        remove.disable();
        ArrayList<ModelData<ServiceModel>> changed = new ArrayList<ModelData<ServiceModel>>();
        changed.addAll(table2.getStore().getAll());
        table2.getStore().clear();
        changed.remove(data);
        table2.getStore().add(changed);
      }
    });
  }

  public void init() {
    waitingWidget.setVisible(true);
    table.setVisible(false);
    table.getStore().clear();
    table2.getStore().clear();
    SettingsServiceLocator.getTeamServlet().getNotLinkedServices(team.getId(), new BaseAsyncCallback<ArrayList<Service>>() {
      @Override
      public void onSuccess(ArrayList<Service> result) {
        ArrayList<ModelData<ServiceModel>> results = new ArrayList<ModelData<ServiceModel>>();
        for (Service service : result) {
          ServiceModel sm = new ServiceModel(service);
          ModelData<ServiceModel> model = new ModelData<ServiceModel>(sm);
          model.put("bean", service);
          model.put("service", service.getName());
          model.put("costs", service.getCosts());
          results.add(model);
        }
        table.getStore().add(results);
        waitingWidget.setVisible(false);
        table.setVisible(true);
      }
    });
  }

  public void search() {
    String str = "%" + service.getText() + "%";
    SettingsServiceLocator.getTeamServlet().getService(str, new BaseAsyncCallback<ArrayList<Service>>() {

      @Override
      public void onSuccess(ArrayList<Service> result) {
        table.getStore().clear();
        ArrayList<ModelData<ServiceModel>> results = new ArrayList<ModelData<ServiceModel>>();
        for (Service service : result) {
          ServiceModel sm = new ServiceModel(service);
          ModelData<ServiceModel> model = new ModelData<ServiceModel>(sm);
          model.put("bean", service);
          model.put("service", service.getName());
          model.put("costs", service.getCosts());
          results.add(model);
        }
        table.getStore().add(results);
        waitingWidget.setVisible(false);
        table.setVisible(true);
      }
    });
  }

  public void show() {
    popupFrame.hideMessageBar();
    popupFrame.showContent();
  }

  public void renderMoveButtons() {

    add.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        if (modeldata == null) {
          return;
        }
        table2.getStore().add(modeldata);
        table2.update();
        modeldata = null;
        add.disable();
      }
    });
    add.disable();
    remove.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        if (modeldata == null) {
          return;
        }
        ArrayList<ModelData<ServiceModel>> changed = new ArrayList<ModelData<ServiceModel>>();
        changed.addAll(table2.getStore().getAll());
        table2.getStore().clear();
        changed.remove(modeldata);
        table2.getStore().add(changed);
        remove.disable();
      }
    });
    remove.disable();
  }

  public void save() {
    ArrayList<Long> serviceIds = new ArrayList<Long>();
    List<ServiceModel> services = table2.getStore().getBeans();
    for (ServiceModel model : services) {
      Service service = model.getBean();
      serviceIds.add(service.getId());
    }

    SettingsServiceLocator.getTeamServlet().addServices(team.getId(), serviceIds, new BaseAsyncCallback<RpcStatus>() {
      @Override
      @SuppressWarnings("unchecked")
      public void onSuccess(RpcStatus result) {
        PortletEventManager.fireEvent(new AddServicesEvent(table2.getStore().getBeans()));
        popupFrame.close();
      }

      @Override
      public void onFailure(Throwable exception) {
        Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.teamAddServiceError());
      }
    });

  }
}
