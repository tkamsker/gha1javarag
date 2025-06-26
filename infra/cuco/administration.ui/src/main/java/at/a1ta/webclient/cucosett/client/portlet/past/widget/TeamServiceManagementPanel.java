package at.a1ta.webclient.cucosett.client.portlet.past.widget;

import java.util.ArrayList;

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

import at.a1ta.bite.ui.client.Delegate;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.bite.ui.client.widget.ClickableIcon;
import at.a1ta.bite.ui.client.widget.WaitingWidget;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.dto.ServiceModel;
import at.a1ta.cuco.admin.ui.common.client.event.AddServicesEvent;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.event.RemoveServicesEvent;
import at.a1ta.cuco.core.shared.dto.Service;
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
import at.a1ta.webclient.cucosett.client.dialog.GwtSelectServiceDialog;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class TeamServiceManagementPanel extends SimplePanel implements SelectionHandler<Integer> {

  private DataTable<Service> table;

  private Widget panel = null;

  private Team team = null;

  private Button btnService;

  private WaitingWidget waitingWidget;

  private Delegate<Service> deleteServiceDelegate;

  private boolean rendered;

  public TeamServiceManagementPanel() {
    this.setSize("100%", "100%");
  }

  @Override
  public void onSelection(SelectionEvent<Integer> event) {
    if (!rendered && event.getSelectedItem().intValue() == 1) {
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
    HorizontalPanel newService = createNewServiceRow();
    pnl.add(newService);
    pnl.add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    pnl.add(waitingWidget);
    pnl.add(table);
    deleteServiceDelegate = new Delegate<Service>() {

      @Override
      public void execute(final Service service) {
        final ModelData<Service> m = new ModelData<Service>(service);
        final Service svc = m.getBean();
        if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteServiceQuestion())) {
          waitingWidget.setText(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteService());
          waitingWidget.show();
          SettingsServiceLocator.getTeamServlet().removeService(team.getId(), svc.getId(), new BaseAsyncCallback<RpcStatus>() {
            @Override
            public void onSuccess(RpcStatus result) {
              team.getServices().remove(service);
              waitingWidget.hide();

              PortletEventManager.fireEvent(new RemoveServicesEvent(service));
            }

            @Override
            public void onFailure(Throwable caught) {
              waitingWidget.hide();
              Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.teamDeleteError());
            }
          });
        }

      }
    };

    registerListeners();
    loadService();
    return pnl;
  }

  public void initTable() {
    table = new DataTable<Service>(createColumns());
    table.enablePaging(10);
    table.setWidth("500px");
    table.setVisible(false);
  }

  public void loadService() {
    waitingWidget.setVisible(true);
    table.setVisible(false);

    table.getStore().clear();

    if (team == null) {
      btnService.disable();
      waitingWidget.setVisible(false);
      table.setVisible(true);
      return;
    }
    btnService.enable();
    if (!AdminAuthorityHelper.canAddService(UserManager.getUserInfo())) {
      btnService.setVisible(false);
    }

    updateServicesInTable();
    waitingWidget.setVisible(false);
    table.setVisible(true);

  }

  private void registerListeners() {
    PortletEventManager.addListener(CuCoEventType.ACTIVATE_TEAM, new PortletEventListener<PortletEvent>() {

      @Override
      public void handleEvent(PortletEvent be) {
        team = (Team) be.getSource();
        if (rendered) {
          loadService();
        }
      }
    });
    PortletEventManager.addListener(CuCoEventType.ADD_SERVICES, new PortletEventListener<AddServicesEvent>() {

      @Override
      public void handleEvent(AddServicesEvent be) {
        for (ServiceModel model : be.getServices()) {
          team.getServices().add(model.getBean());
        }
        updateServicesInTable();
      }
    });

    PortletEventManager.addListener(CuCoEventType.REMOVE_SERVICES, new PortletEventListener<RemoveServicesEvent>() {

      @Override
      public void handleEvent(RemoveServicesEvent event) {
        if (team != null) {
          team.getServices().remove(event.getService());
        }
        updateServicesInTable();
      }
    });
  }

  private HorizontalPanel createNewServiceRow() {
    HorizontalPanel newMember = new HorizontalPanel();
    newMember.add(createServiceButton());
    return newMember;
  }

  private Widget createServiceButton() {
    btnService = new Button(AdminUI.ADMINCOMMONTEXTPOOL.teamAddService(), ButtonSize.Small);
    btnService.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        GwtSelectServiceDialog d = GwtSelectServiceDialog.getInstance(team);
        d.init();
        d.show();
      }
    });
    return btnService;
  }

  private ArrayList<Column<Service>> createColumns() {
    ArrayList<Column<Service>> columns = new ArrayList<Column<Service>>();
    columns.add(new Column<Service>("name", AdminUI.ADMINCOMMONTEXTPOOL.teamService(), "40%"));
    columns.add(new Column<Service>("costs", AdminUI.ADMINCOMMONTEXTPOOL.teamCosts(), "30%"));
    columns.add(new Column<Service>("delete", AdminUI.ADMINCOMMONTEXTPOOL.teamDelete(), "10%", createDeleteCellRenderer()));
    return columns;
  }

  private CellRenderer<Service> createDeleteCellRenderer() {
    return new CellRenderer<Service>() {
      @Override
      public IsWidget render(final ModelData<Service> model, String columnId, int rowId) {
        return new ClickableIcon<Service>(model.getBean(), deleteServiceDelegate, UI.IMAGES.iconDelete(), null);
      }
    };
  }

  private void updateServicesInTable() {
    table.getStore().clear();
    ArrayList<ModelData<Service>> results = new ArrayList<ModelData<Service>>();
    for (Service sm : team.getServices()) {
      ModelData<Service> m = new ModelData<Service>(sm);
      m.put("bean", sm);
      m.put("name", sm.getName());
      m.put("costs", sm.getCosts());
      results.add(m);
    }
    table.getStore().add(results);
  }

}
