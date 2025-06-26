package at.a1ta.webclient.cucosett.client.portlet;

import java.util.ArrayList;
import java.util.List;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.google.gwt.user.client.Window;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.framework.gxt.ui.ButtonRenderer;
import at.a1ta.framework.gxt.ui.GridContainer;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class IbatisPortlet extends CuCoSettBasePortlet {

  public static final String NAME = "Ibatis";

  private static IbatisPortlet _instance = null;

  private Button clearAll = new Button(AdminUI.ADMINCOMMONTEXTPOOL.administrationIbatisClearall());

  private ListStore<BaseModelData> store = new ListStore<BaseModelData>();

  private GridContainer<ListStore<BaseModelData>, BaseModelData> grid;

  private ColumnModel cm;

  public static IbatisPortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new IbatisPortlet(def);
    }
    return _instance;
  }

  private IbatisPortlet(PortletDefinition def) {
    super(def);
    add(clearAll);
    clearAll.addSelectionListener(new SelectionListener<ButtonEvent>() {

      @Override
      public void componentSelected(ButtonEvent ce) {
        SettingsServiceLocator.getIbatisServlet().flushAll(new BaseAsyncCallback<RpcStatus>() {

          @Override
          public void onSuccess(RpcStatus result) {
            Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.administrationIbatisClearallDone());
          }
        });
      }
    });

    List<ColumnConfig> configs = new ArrayList<ColumnConfig>();

    ColumnConfig config = new ColumnConfig("name", AdminUI.ADMINCOMMONTEXTPOOL.administrationIbatisColumnName(), 200);
    configs.add(config);

    config = new ColumnConfig("flush", AdminUI.ADMINCOMMONTEXTPOOL.administrationIbatisFlush(), 40);
    config.setRenderer(new ButtonRenderer(new SelectionListener<ButtonEvent>() {

      @Override
      public void componentSelected(ButtonEvent ce) {
        int col = Integer.parseInt(ce.getButton().getId());
        String name = grid.getGrid().getStore().getAt(col).get("name");
        SettingsServiceLocator.getIbatisServlet().flushDao(name, new BaseAsyncCallback<RpcStatus>() {

          @Override
          public void onSuccess(RpcStatus result) {
            Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.administrationIbatisClearDone());
          }
        });
      }
    }, AdminUI.ADMINCOMMONTEXTPOOL.administrationIbatisFlush()));
    configs.add(config);
    cm = new ColumnModel(configs);

    grid = new GridContainer<ListStore<BaseModelData>, BaseModelData>(store, cm, 600);

    add(grid);

  }

  @Override
  public void init() {

    store.removeAll();
    SettingsServiceLocator.getIbatisServlet().getDaos(new BaseAsyncCallback<ArrayList<String>>() {

      @Override
      public void onSuccess(ArrayList<String> result) {
        for (String s : result) {
          BaseModelData model = new BaseModelData();
          model.set("name", s);
          store.add(model);
        }

        grid.getGrid().reconfigure(store, cm);
        showContent();
      }
    });
  }

}
