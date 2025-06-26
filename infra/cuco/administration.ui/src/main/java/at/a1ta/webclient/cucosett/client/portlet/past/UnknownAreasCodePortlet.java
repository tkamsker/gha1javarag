package at.a1ta.webclient.cucosett.client.portlet.past;

import java.util.ArrayList;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
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
import at.a1ta.bite.ui.client.widget.WaitingWidget;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.AddUnknownAreaCodeEvent;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.EditUnknownAreasCodeDialog;
import at.a1ta.webclient.cucosett.client.portlet.CuCoSettBasePortlet;

public class UnknownAreasCodePortlet extends CuCoSettBasePortlet {

  public static final String NAME = "PaST Ungültige Vorwahlen";

  private static UnknownAreasCodePortlet _instance = null;

  private DataTable<UnknownAreaCode> table;

  private WaitingWidget waitingWidget;

  private EditUnknownAreasCodeDialog editUnknownAreasCodeDialog;

  private Delegate<UnknownAreaCode> deleteRoleGroupDelegate;

  public static UnknownAreasCodePortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new UnknownAreasCodePortlet(def);
    }
    return _instance;
  }

  private UnknownAreasCodePortlet(PortletDefinition def) {
    super(def, false, false);

    initTable();
    initUI();

    registerUpdateAreaCodeListener();
    registerUpdateAreaCodesListener();

    loadAreaCode();

    showContent();
  }

  private void initUI() {
    waitingWidget = new WaitingWidget();
    HTMLPanel pnl = new HTMLPanel("");
    pnl.setStyleName(UI.STYLES.bite_moduleContent());
    HorizontalPanel newAreaCode = createNewAreaCodeRow();
    pnl.add(newAreaCode);
    pnl.add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    pnl.add(waitingWidget);
    pnl.add(table);
    add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    add(pnl);

    deleteRoleGroupDelegate = new Delegate<UnknownAreaCode>() {
      @Override
      public void execute(final UnknownAreaCode areaCode) {
        CommonServiceLocator.getUnknownAreaCodeServlet().deleteUnknownAreaCode(areaCode.getId(), new BaseAsyncCallback<RpcStatus>() {
          @Override
          public void onSuccess(RpcStatus result) {
            if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeDeleteQuestion())) {
              waitingWidget.setText(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeMessageDelete());
              waitingWidget.show();
              ModelData<UnknownAreaCode> m = new ModelData<UnknownAreaCode>(areaCode);
              m.remove(areaCode);
              waitingWidget.hide();
              loadAreaCode();
            }
          }

          @Override
          public void onFailure(Throwable caught) {
            waitingWidget.hide();
            Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.messageboxDeleteError());
            loadAreaCode();
          }
        });

      }
    };
  }

  private void initTable() {
    table = new DataTable<UnknownAreaCode>(createColumns());
    table.enablePaging(10);
    table.setWidth("1000px");
    table.setVisible(false);
  }

  private void registerUpdateAreaCodesListener() {
    PortletEventManager.addListener(CuCoEventType.UPDATEUNKNOWN_AREACODES, new PortletEventListener<AddUnknownAreaCodeEvent>() {

      @Override
      public void handleEvent(AddUnknownAreaCodeEvent be) {
        init();
        loadAreaCode();
      }
    });
  }

  public void loadAreaCode() {
    waitingWidget.setVisible(true);
    table.setVisible(false);

    table.getStore().clear();

    CommonServiceLocator.getUnknownAreaCodeServlet().getAllUnknownAreaCodes(new BaseAsyncCallback<ArrayList<UnknownAreaCode>>(this) {

      @Override
      public void onSuccess(ArrayList<UnknownAreaCode> result) {
        ArrayList<ModelData<UnknownAreaCode>> results = new ArrayList<ModelData<UnknownAreaCode>>();

        for (UnknownAreaCode code : result) {
          ModelData<UnknownAreaCode> m = new ModelData<UnknownAreaCode>(code);
          m.put("bean", code);
          m.put("areacode", code.getAreaCode());
          m.put("description", code.getDescription());
          results.add(m);
        }

        table.getStore().add(results);
        waitingWidget.setVisible(false);
        table.setVisible(true);
      }
    });
  }

  private void registerUpdateAreaCodeListener() {
    PortletEventManager.addListener(CuCoEventType.UPDATEUNKNOWN_AREACODES, new PortletEventListener<AddUnknownAreaCodeEvent>() {

      @Override
      public void handleEvent(AddUnknownAreaCodeEvent event) {
        UnknownAreaCode code = event.getCode();
        ModelData<UnknownAreaCode> model = table.getStore().get(code);
        if (model != null) {
          model.setBean(code);
        } else {
          model = new ModelData<UnknownAreaCode>(code);
          model.put("bean", code);
          model.put("areacode", code.getAreaCode());
          model.put("description", code.getDescription());
          table.getStore().add(model);
        }
      }
    });
  }

  private HorizontalPanel createNewAreaCodeRow() {
    HorizontalPanel newAreaCode = new HorizontalPanel();
    newAreaCode.add(createNewAreaCodeButton());
    return newAreaCode;
  }

  private Widget createNewAreaCodeButton() {
    Button btnAreaCode = new Button(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeNew(), ButtonSize.Small);
    editUnknownAreasCodeDialog = new EditUnknownAreasCodeDialog();

    btnAreaCode.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        editUnknownAreasCodeDialog.show(null);
      }
    });
    return btnAreaCode;
  }

  private ArrayList<Column<UnknownAreaCode>> createColumns() {
    ArrayList<Column<UnknownAreaCode>> columns = new ArrayList<Column<UnknownAreaCode>>();
    columns.add(new Column<UnknownAreaCode>("areacode", AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeGridColumnName(), "20%", createAreaCodeCellRenderer()));
    columns.add(new Column<UnknownAreaCode>("description", AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeGridColumnDescription(), "30%"));
    columns.add(new Column<UnknownAreaCode>("delete", AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeGridColumnDelete(), "25%", createDeleteCellRenderer()));
    return columns;
  }

  private CellRenderer<UnknownAreaCode> createAreaCodeCellRenderer() {
    return new CellRenderer<UnknownAreaCode>() {
      @Override
      public Widget render(final ModelData<UnknownAreaCode> model, String columnId, int rowId) {
        Anchor link = new Anchor(model.getBean().getAreaCode());
        link.addClickHandler(new ClickHandler() {
          @Override
          public void onClick(ClickEvent event) {
            CommonServiceLocator.getUnknownAreaCodeServlet().getAllUnknownAreaCodes(new BaseAsyncCallback<ArrayList<UnknownAreaCode>>() {

              @Override
              public void onSuccess(ArrayList<UnknownAreaCode> result) {
                editUnknownAreasCodeDialog.show(model.getBean());
              }
            });

          }
        });
        return link;
      }
    };
  }

  private CellRenderer<UnknownAreaCode> createDeleteCellRenderer() {
    return new CellRenderer<UnknownAreaCode>() {
      @Override
      public IsWidget render(final ModelData<UnknownAreaCode> model, String columnId, int rowId) {
        return new ClickableIcon<UnknownAreaCode>(model.getBean(), deleteRoleGroupDelegate, UI.IMAGES.iconDelete(), null);
      }
    };
  }

  @Override
  public void init() {}

}
