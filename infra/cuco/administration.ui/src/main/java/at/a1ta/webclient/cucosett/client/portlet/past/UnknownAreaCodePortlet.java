package at.a1ta.webclient.cucosett.client.portlet.past;

import java.util.ArrayList;

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
import at.a1ta.cuco.admin.ui.common.client.event.AddUnknownAreaCodeEvent;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.admin.ui.common.client.ui.ImageRenderer;
import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;
import at.a1ta.framework.gxt.ui.GridContainer;
import at.a1ta.framework.gxt.ui.LinkCellRenderer;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.EditUnknownAreaCodeDialog;
import at.a1ta.webclient.cucosett.client.portlet.CuCoSettBasePortlet;

public class UnknownAreaCodePortlet extends CuCoSettBasePortlet implements Listener<BaseEvent>, ClickHandler {

  public static final String NAME = "PaST Ungültige Vorwahlen Old";

  private static UnknownAreaCodePortlet _instance = null;

  private GridContainer<ListStore<BaseModelData>, BaseModelData> gridContainer;

  public static UnknownAreaCodePortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new UnknownAreaCodePortlet(def);
    }
    return _instance;
  }

  private UnknownAreaCodePortlet(PortletDefinition def) {
    super(def, false, false);

    add(renderGrid());
  }

  private Widget renderGrid() {

    Button newBtn = new Button(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeNew());
    newBtn.addSelectionListener(new SelectionListener<ButtonEvent>() {

      @Override
      public void componentSelected(ButtonEvent ce) {
        EditUnknownAreaCodeDialog d = EditUnknownAreaCodeDialog.getInstance();
        d.show();
      }
    });

    ToolBar tb = new ToolBar();
    tb.add(newBtn);

    ListStore<BaseModelData> store = new ListStore<BaseModelData>();

    ArrayList<ColumnConfig> configs = new ArrayList<ColumnConfig>();

    ColumnConfig config = new ColumnConfig("areacode", AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeGridColumnName(), 70);
    config.setRenderer(new LinkCellRenderer(this));
    configs.add(config);

    config = new ColumnConfig("description", AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeGridColumnDescription(), 300);
    configs.add(config);

    config = new ColumnConfig("delete", AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeGridColumnDelete(), 120);
    config.setRenderer(new ImageRenderer(ImageRenderer.DELETE, this));
    configs.add(config);

    ColumnModel cm = new ColumnModel(configs);

    gridContainer = new GridContainer<ListStore<BaseModelData>, BaseModelData>(store, cm);
    gridContainer.setTopComponent(tb);
    gridContainer.getGrid().setAutoExpandColumn("description");

    PortletEventManager.addListener(CuCoEventType.UPDATEUNKNOWN_AREACODES, new PortletEventListener<AddUnknownAreaCodeEvent>() {

      @Override
      public void handleEvent(AddUnknownAreaCodeEvent be) {
        gridContainer.getGrid().getStore().getLoader().load();
      }
    });
    return gridContainer;
  }

  @Override
  public void init() {
    gridContainer.getGrid().getStore().removeAll();

    RpcProxy<ArrayList<UnknownAreaCode>> proxy = new RpcProxy<ArrayList<UnknownAreaCode>>() {

      @Override
      protected void load(Object loadConfig, AsyncCallback<ArrayList<UnknownAreaCode>> callback) {
        CommonServiceLocator.getUnknownAreaCodeServlet().getAllUnknownAreaCodes(callback);
      }
    };

    BaseListLoader<ListLoadResult<BaseModelData>> loader = new BaseListLoader<ListLoadResult<BaseModelData>>(proxy, new DataReader<ListLoadResult<BaseModelData>>() {

      @Override
      @SuppressWarnings("unchecked")
      public ListLoadResult<BaseModelData> read(Object loadConfig, Object data) {
        ArrayList<BaseModelData> results = new ArrayList<BaseModelData>();

        ArrayList<UnknownAreaCode> list = (ArrayList<UnknownAreaCode>) data;

        for (UnknownAreaCode code : list) {
          BaseModelData m = new BaseModelData();
          m.set("bean", code);
          m.set("areacode", code.getAreaCode());
          m.set("description", code.getDescription());
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

    if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeDeleteQuestion())) {
      UnknownAreaCode code = md.get("bean");

      final MessageBox wait = MessageBox.wait(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeLabel(), AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeMessageDelete(),
          AdminUI.ADMINCOMMONTEXTPOOL.messageboxDelete());
      wait.show();

      CommonServiceLocator.getUnknownAreaCodeServlet().deleteUnknownAreaCode(code.getId(), new BaseAsyncCallback<RpcStatus>() {

        @Override
        public void onSuccess(RpcStatus result) {
          gridContainer.getGrid().getStore().getLoader().load();
          wait.close();
        }

        @Override
        public void onFailure(Throwable exception) {
          wait.close();
          MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeLabel(), AdminUI.ADMINCOMMONTEXTPOOL.messageboxDeleteError(), null);
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

    EditUnknownAreaCodeDialog d = EditUnknownAreaCodeDialog.getInstance((UnknownAreaCode) md.get("bean"));
    d.show();
  }
}
