package at.a1ta.webclient.cucosett.client.portlet.past;

import java.util.ArrayList;
import java.util.List;

import com.extjs.gxt.ui.client.data.BaseListLoadResult;
import com.extjs.gxt.ui.client.data.BaseListLoader;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.DataReader;
import com.extjs.gxt.ui.client.data.ListLoadResult;
import com.extjs.gxt.ui.client.data.RpcProxy;
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
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.AddCreditTypeEvent;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.ui.BooleanRenderer;
import at.a1ta.cuco.admin.ui.common.client.ui.ImageRenderer;
import at.a1ta.cuco.core.shared.dto.CreditType;
import at.a1ta.framework.gxt.ui.GridContainer;
import at.a1ta.framework.gxt.ui.LinkCellRenderer;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.EditCreditTypeDialog;
import at.a1ta.webclient.cucosett.client.portlet.CuCoSettBasePortlet;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class CreditTypePortlet extends CuCoSettBasePortlet implements Listener<BaseEvent>, ClickHandler {

  public static final String NAME = "PaST GutschriftenOld";

  private static CreditTypePortlet _instance = null;

  public static CreditTypePortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new CreditTypePortlet(def, false);
    }
    return _instance;
  }

  private GridContainer<ListStore<BaseModelData>, BaseModelData> gridContainer;

  private CreditTypePortlet(PortletDefinition def, boolean isDetails) {
    super(def, isDetails, false, false);

    add(renderGrid());
  }

  private Widget renderGrid() {

    Button newBtn = new Button(AdminUI.ADMINCOMMONTEXTPOOL.credittypeNew());
    newBtn.addSelectionListener(new SelectionListener<ButtonEvent>() {

      @Override
      public void componentSelected(ButtonEvent ce) {
        EditCreditTypeDialog d = EditCreditTypeDialog.getInstance();
        d.show();
      }
    });

    ToolBar tb = new ToolBar();
    tb.add(newBtn);

    ListStore<BaseModelData> store = new ListStore<BaseModelData>();

    List<ColumnConfig> configs = new ArrayList<ColumnConfig>();

    ColumnConfig config = new ColumnConfig("name", AdminUI.ADMINCOMMONTEXTPOOL.credittypeGridColumnName(), 140);
    config.setRenderer(new LinkCellRenderer(this));
    configs.add(config);

    config = new ColumnConfig("description", AdminUI.ADMINCOMMONTEXTPOOL.credittypeGridColumnDescription(), 300);
    configs.add(config);

    config = new ColumnConfig("active", AdminUI.ADMINCOMMONTEXTPOOL.credittypeGridColumnActive(), 120);
    config.setRenderer(new BooleanRenderer());
    configs.add(config);

    config = new ColumnConfig("delete", AdminUI.ADMINCOMMONTEXTPOOL.credittypeGridColumnDelete(), 120);
    config.setRenderer(new ImageRenderer(ImageRenderer.DELETE, this));
    configs.add(config);

    ColumnModel cm = new ColumnModel(configs);

    gridContainer = new GridContainer<ListStore<BaseModelData>, BaseModelData>(store, cm);
    gridContainer.setTopComponent(tb);
    gridContainer.getGrid().setAutoExpandColumn("billnumber");

    PortletEventManager.addListener(CuCoEventType.UPDATECREDIT_TYPES, new PortletEventListener<AddCreditTypeEvent>() {

      @Override
      public void handleEvent(AddCreditTypeEvent be) {
        gridContainer.getGrid().getStore().getLoader().load();
      }
    });
    return gridContainer;
  }

  @Override
  public void init() {
    gridContainer.getGrid().getStore().removeAll();

    RpcProxy<ArrayList<CreditType>> proxy = new RpcProxy<ArrayList<CreditType>>() {

      @Override
      protected void load(Object loadConfig, AsyncCallback<ArrayList<CreditType>> callback) {
        SettingsServiceLocator.getCreditTypeServlet().getAllCreditTypes(callback);
      }
    };

    BaseListLoader<ListLoadResult<BaseModelData>> loader = new BaseListLoader<ListLoadResult<BaseModelData>>(proxy, new DataReader<ListLoadResult<BaseModelData>>() {

      @Override
      @SuppressWarnings("unchecked")
      public ListLoadResult<BaseModelData> read(Object loadConfig, Object data) {
        List<BaseModelData> results = new ArrayList<BaseModelData>();

        List<CreditType> list = (List<CreditType>) data;

        for (CreditType ct : list) {
          BaseModelData m = new BaseModelData();
          m.set("bean", ct);
          m.set("name", ct.getName());
          m.set("description", ct.getDescription());
          m.set("active", ct.getActive());
          results.add(m);
        }
        return new BaseListLoadResult<BaseModelData>(results);
      }
    });
    ListStore<BaseModelData> store = new ListStore<BaseModelData>(loader);
    gridContainer.reconfigure(store);
    loader.load();
    showContent();
  }

  @Override
  public void handleEvent(BaseEvent be) {
    BaseModelData md = gridContainer.getGrid().getSelectionModel().getSelectedItem();

    if (md == null) {
      return;
    }

    if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.credittypeDeleteQuestion())) {
      CreditType ct = md.get("bean");

      final MessageBox wait = MessageBox.wait(AdminUI.ADMINCOMMONTEXTPOOL.credittypeLabel(), AdminUI.ADMINCOMMONTEXTPOOL.credittypeMessageDelete(), AdminUI.ADMINCOMMONTEXTPOOL.messageboxDelete());
      wait.show();

      SettingsServiceLocator.getCreditTypeServlet().deleteCreditType(ct.getId(), new BaseAsyncCallback<RpcStatus>() {

        @Override
        public void onSuccess(RpcStatus result) {
          gridContainer.getGrid().getStore().getLoader().load();
          wait.close();
        }

        @Override
        public void onFailure(Throwable exception) {
          wait.close();
          MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.credittypeLabel(), AdminUI.ADMINCOMMONTEXTPOOL.messageboxDeleteError(), null);
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

    EditCreditTypeDialog d = EditCreditTypeDialog.getInstance((CreditType) md.get("bean"));
    d.show();
  }
}
