package at.a1ta.webclient.cucosett.client.portlet.past;

import java.util.ArrayList;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.dom.client.KeyCodes;
import com.google.gwt.event.dom.client.KeyPressEvent;
import com.google.gwt.event.dom.client.KeyPressHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Anchor;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.bite.ui.client.Delegate;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.bite.ui.client.widget.ClickableIcon;
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.InputBox.InputBoxSize;
import at.a1ta.bite.ui.client.widget.WaitingWidget;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.framework.ui.client.util.HtmlUtils;
import at.a1ta.webclient.cucosett.client.dialog.GwtEditServiceDialog;
import at.a1ta.webclient.cucosett.client.portlet.CuCoSettBasePortlet;

public class GwtServicePortlet extends CuCoSettBasePortlet {

  public static final String NAME = "PaST Services";

  private static GwtServicePortlet _instance;

  private DataTable<Service> table;
  private InputBox userFilter;
  private GwtEditServiceDialog gwtEditServiceDialog;
  private WaitingWidget waitingWidget;
  private Delegate<Service> deleteRoleGroupDelegate;

  public static GwtServicePortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new GwtServicePortlet(def);
    }
    return _instance;
  }

  private GwtServicePortlet(PortletDefinition def) {
    super(def, false, false);

    initTable();
    initUI();

    registerUpdateServiceListener();

    loadService();

    showContent();

    add(HtmlUtils.createLink("pastExport?what=services", "Export", true));
  }

  private void initTable() {
    table = new DataTable<Service>(createColumns());
    table.enablePaging(10);
    table.setWidth("1000px");
    table.setVisible(false);
  }

  private void initUI() {
    waitingWidget = new WaitingWidget();
    HTMLPanel pnl = new HTMLPanel("");
    pnl.setStyleName(UI.STYLES.bite_moduleContent());
    HorizontalPanel newService = createNewServiceRow();
    HorizontalPanel filters = createFilterRow();
    pnl.add(filters);
    pnl.add(newService);
    pnl.add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    pnl.add(waitingWidget);
    pnl.add(table);
    add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    add(pnl);
    deleteRoleGroupDelegate = new Delegate<Service>() {
      @Override
      public void execute(final Service service) {
        CommonServiceLocator.getServiceServlet().deleteService(service.getId(), new BaseAsyncCallback<RpcStatus>() {
          @Override
          public void onSuccess(RpcStatus result) {
            if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.serviceDeleteQuestion())) {
              ModelData<Service> m = new ModelData<Service>(service);
              waitingWidget.setText(AdminUI.ADMINCOMMONTEXTPOOL.serviceMessageDelete());
              waitingWidget.show();
              m.remove(service);
              waitingWidget.hide();
              loadService();
            }
          }

          @Override
          public void onFailure(Throwable caught) {
            waitingWidget.hide();
            Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.messageboxDeleteError());
            loadService();
          }
        });

      }
    };
  }

  private void registerUpdateServiceListener() {
    PortletEventManager.addListener(CuCoEventType.UPDATE_SERVICES, new PortletEventListener<PortletEvent>() {

      @Override
      public void handleEvent(PortletEvent event) {
        loadService();
      }
    });
  }

  private void loadDataInTable(ArrayList<Service> result) {

    ArrayList<ModelData<Service>> results = new ArrayList<ModelData<Service>>();

    for (Service service : result) {
      ModelData<Service> m = new ModelData<Service>(service);
      m.put("bean", service);
      m.put("name", service.getName());
      m.put("from", service.getValidity().getValidFrom());
      m.put("to", service.getValidity().getValidUntil());
      m.put("costs", service.getCosts());
      results.add(m);
    }

    table.getStore().add(results);
    waitingWidget.setVisible(false);
    table.setVisible(true);
  }

  public void loadService() {
    waitingWidget.setVisible(true);
    table.setVisible(false);

    table.getStore().clear();

    CommonServiceLocator.getServiceServlet().getAllServices(new BaseAsyncCallback<ArrayList<Service>>(this) {

      @Override
      public void onSuccess(ArrayList<Service> result) {
        loadDataInTable(result);
      }
    });
  }

  private HorizontalPanel createNewServiceRow() {
    HorizontalPanel newCredit = new HorizontalPanel();
    newCredit.add(createNewServiceButton());
    return newCredit;
  }

  private Widget createNewServiceButton() {
    Button btnCreateSevice = new Button(AdminUI.ADMINCOMMONTEXTPOOL.serviceNew(), ButtonSize.Small);
    gwtEditServiceDialog = new GwtEditServiceDialog();

    btnCreateSevice.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        gwtEditServiceDialog.show(null);
      }
    });
    return btnCreateSevice;
  }

  private ArrayList<Column<Service>> createColumns() {
    ArrayList<Column<Service>> columns = new ArrayList<Column<Service>>();
    columns.add(new Column<Service>("name", AdminUI.ADMINCOMMONTEXTPOOL.serviceGridColumnName(), "30%", createServiceCellRenderer()));
    columns.add(new Column<Service>("from", AdminUI.ADMINCOMMONTEXTPOOL.serviceGridColumnFrom(), "20%"));
    columns.add(new Column<Service>("to", AdminUI.ADMINCOMMONTEXTPOOL.serviceGridColumnTo(), "20%"));
    columns.add(new Column<Service>("costs", AdminUI.ADMINCOMMONTEXTPOOL.serviceGridColumnCosts(), "20%"));
    columns.add(new Column<Service>("delete", AdminUI.ADMINCOMMONTEXTPOOL.serviceGridColumnDelete(), "10%", createDeleteCellRenderer()));
    return columns;
  }

  private CellRenderer<Service> createServiceCellRenderer() {
    return new CellRenderer<Service>() {

      @Override
      public IsWidget render(final ModelData<Service> model, String columnId, int rowId) {
        Anchor link = new Anchor(model.getBean().getName());
        link.addClickHandler(new ClickHandler() {
          @Override
          public void onClick(ClickEvent event) {
            CommonServiceLocator.getServiceServlet().getAllServices(new BaseAsyncCallback<ArrayList<Service>>() {

              @Override
              public void onSuccess(ArrayList<Service> result) {
                gwtEditServiceDialog.show(model.getBean());
              }
            });

          }
        });
        return link;
      }
    };
  }

  private CellRenderer<Service> createDeleteCellRenderer() {
    return new CellRenderer<Service>() {
      @Override
      public IsWidget render(final ModelData<Service> model, String columnId, int rowId) {
        return new ClickableIcon<Service>(model.getBean(), deleteRoleGroupDelegate, UI.IMAGES.iconDelete(), null);
      }
    };
  }

  public void loadUsers() {
    waitingWidget.setVisible(true);
    table.setVisible(false);
    table.getStore().clear();
    String service = '%' + userFilter.getValue() + '%';
    CommonServiceLocator.getServiceServlet().searchService(service, new BaseAsyncCallback<ArrayList<Service>>() {
      @Override
      public void onSuccess(ArrayList<Service> result) {
        loadDataInTable(result);
      }

    });
  }

  private HorizontalPanel createFilterRow() {
    HorizontalPanel filters = new HorizontalPanel();
    filters.add(new HTML("<div class='" + UI.STYLES.bite_widthPlaceHolder() + "'/>"));
    filters.add(createUserSearch());
    filters.add(createSearchButton());
    filters.add(new HTML("<hr/>"));
    return filters;
  }

  private Widget createSearchButton() {

    Button btnSearch = new Button("Suchen", ButtonSize.Small);
    btnSearch.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        loadUsers();
      }
    });
    return btnSearch;
  }

  private Widget createUserSearch() {
    userFilter = new InputBox(InputBoxSize.Medium);
    userFilter.addKeyPressHandler(createKeyPressHandler());
    return userFilter;
  }

  private KeyPressHandler createKeyPressHandler() {
    return new KeyPressHandler() {
      @Override
      public void onKeyPress(KeyPressEvent event) {
        if (event.getNativeEvent().getKeyCode() == KeyCodes.KEY_ENTER) {
          loadUsers();
        }
      }
    };
  }

  @Override
  public void init() {
    // Do Nothing
  }

}
