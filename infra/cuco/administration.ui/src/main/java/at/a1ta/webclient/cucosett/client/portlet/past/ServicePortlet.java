package at.a1ta.webclient.cucosett.client.portlet.past;

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
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.toolbar.ToolBar;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.i18n.client.DateTimeFormat;
import com.google.gwt.i18n.client.NumberFormat;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.admin.ui.common.client.ui.ImageRenderer;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.framework.gxt.ui.FilterablePagingMemoryProxy;
import at.a1ta.framework.gxt.ui.LinkCellRenderer;
import at.a1ta.framework.gxt.ui.PagingGridContainer;
import at.a1ta.framework.gxt.ui.ProxyFilterField;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.framework.ui.client.util.HtmlUtils;
import at.a1ta.webclient.cucosett.client.dialog.EditServiceDialog;
import at.a1ta.webclient.cucosett.client.portlet.CuCoSettBasePortlet;
import at.a1ta.webclient.cucosett.client.ui.ServiceImageRenderer;

public class ServicePortlet extends CuCoSettBasePortlet implements Listener<BaseEvent>, ClickHandler {

  public static final String NAME = "PaST ServicesOld";

  private static ServicePortlet _instance = null;

  private ProxyFilterField<String> namefilter = null;

  private PagingGridContainer<ListStore<BaseModelData>, BaseModelData> gridContainer;

  public static ServicePortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new ServicePortlet(def);
    }
    return _instance;
  }

  private ServicePortlet(PortletDefinition def) {
    super(def, false, false);

    namefilter = new ProxyFilterField<String>() {

      @Override
      public boolean doFilter(ModelData m) {
        return m.get("name").toString().toLowerCase().contains(getValue().toLowerCase());
      }
    };

    namefilter.setWidth(250);
    add(namefilter);
    add(renderGrid());
    add(HtmlUtils.createLink("pastExport?what=services", "Export", true));
  }

  private Widget renderGrid() {

    Button newBtn = new Button(AdminUI.ADMINCOMMONTEXTPOOL.serviceNew());
    newBtn.addSelectionListener(new SelectionListener<ButtonEvent>() {

      @Override
      public void componentSelected(ButtonEvent ce) {
        EditServiceDialog d = EditServiceDialog.getInstance();
        d.show();
      }
    });

    ToolBar tb = new ToolBar();
    tb.add(newBtn);

    ListStore<BaseModelData> store = new ListStore<BaseModelData>();

    List<ColumnConfig> configs = new ArrayList<ColumnConfig>();

    ColumnConfig config = new ColumnConfig("name", AdminUI.ADMINCOMMONTEXTPOOL.serviceGridColumnName(), 200);
    config.setRenderer(new LinkCellRenderer(this));
    configs.add(config);

    config = new ColumnConfig("from", AdminUI.ADMINCOMMONTEXTPOOL.serviceGridColumnFrom(), 100);
    config.setDateTimeFormat(DateTimeFormat.getMediumDateFormat());
    configs.add(config);

    config = new ColumnConfig("to", AdminUI.ADMINCOMMONTEXTPOOL.serviceGridColumnTo(), 100);
    config.setDateTimeFormat(DateTimeFormat.getMediumDateFormat());
    configs.add(config);

    config = new ColumnConfig("costs", AdminUI.ADMINCOMMONTEXTPOOL.serviceGridColumnCosts(), 100);
    config.setNumberFormat(NumberFormat.getCurrencyFormat());
    config.setAlignment(HorizontalAlignment.RIGHT);
    configs.add(config);

    config = new ColumnConfig("delete", AdminUI.ADMINCOMMONTEXTPOOL.serviceGridColumnDelete(), 120);
    config.setRenderer(new ServiceImageRenderer(ImageRenderer.DELETE, this));
    configs.add(config);

    ColumnModel cm = new ColumnModel(configs);

    gridContainer = new PagingGridContainer<ListStore<BaseModelData>, BaseModelData>(store, cm, 10);
    gridContainer.setTopComponent(tb);
    gridContainer.getGrid().setAutoExpandColumn("billnumber");

    PortletEventManager.addListener(CuCoEventType.UPDATE_SERVICES, new PortletEventListener<PortletEvent>() {

      @Override
      public void handleEvent(PortletEvent be) {
        init();
      }
    });
    return gridContainer;
  }

  @Override
  public void init() {
    gridContainer.getGrid().getStore().removeAll();
    CommonServiceLocator.getServiceServlet().getAllServices(new BaseAsyncCallback<ArrayList<Service>>() {

      @Override
      public void onSuccess(ArrayList<Service> result) {
        ArrayList<BaseModelData> results = new ArrayList<BaseModelData>();

        for (Service service : result) {
          BaseModelData m = new BaseModelData();
          m.set("bean", service);
          m.set("name", service.getName());
          m.set("from", service.getValidity().getValidFrom());
          m.set("to", service.getValidity().getValidUntil());
          m.set("costs", service.getCosts());
          results.add(m);
        }

        FilterablePagingMemoryProxy proxy = new FilterablePagingMemoryProxy(results);
        // loader
        BasePagingLoader<PagingLoadResult<LoadConfig>> gridloader = new BasePagingLoader<PagingLoadResult<LoadConfig>>(proxy);
        gridloader.setRemoteSort(true);
        gridContainer.getToolbar().bind(gridloader);

        namefilter.bind(gridloader);

        ListStore<BaseModelData> store = new ListStore<BaseModelData>(gridloader);
        gridContainer.reconfigure(store);
        gridloader.load();
        showContent();
      }
    });
  }

  @Override
  public void handleEvent(BaseEvent be) {
    BaseModelData md = gridContainer.getGrid().getSelectionModel().getSelectedItem();

    if (md == null) {
      return;
    }

    if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.serviceDeleteQuestion())) {
      Service service = md.get("bean");

      final MessageBox wait = MessageBox.wait(AdminUI.ADMINCOMMONTEXTPOOL.serviceLabel(), AdminUI.ADMINCOMMONTEXTPOOL.serviceMessageDelete(), AdminUI.ADMINCOMMONTEXTPOOL.messageboxDelete());
      wait.show();

      CommonServiceLocator.getServiceServlet().deleteService(service.getId(), new BaseAsyncCallback<RpcStatus>() {

        @Override
        public void onSuccess(RpcStatus result) {
          init();
          wait.close();
        }

        @Override
        public void onFailure(Throwable exception) {
          wait.close();
          MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.serviceLabel(), AdminUI.ADMINCOMMONTEXTPOOL.messageboxDeleteError(), null);
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

    EditServiceDialog d = EditServiceDialog.getInstance((Service) md.get("bean"));
    d.show();
  }
}
