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
import at.a1ta.cuco.admin.ui.common.client.event.AddCreditTypeEvent;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.core.shared.dto.CreditType;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.EditCreditTypesDialog;
import at.a1ta.webclient.cucosett.client.portlet.CuCoSettBasePortlet;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class CreditTypesPortlet extends CuCoSettBasePortlet {

  public static final String NAME = "PaST Gutschriften";

  private static CreditTypesPortlet _instance;
  private DataTable<CreditType> table;
  private WaitingWidget waitingWidget;
  private EditCreditTypesDialog editCreditTypesDialog;
  private Delegate<CreditType> deleteRoleGroupDelegate;

  public static CreditTypesPortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new CreditTypesPortlet(def, false);
    }
    return _instance;
  }

  private CreditTypesPortlet(PortletDefinition def, boolean isDetails) {
    super(def, isDetails, false, false);

    initTable();
    initUI();

    registerUpdateCreditListener();
    registerUpdateCreditsListener();

    loadCredits();

    showContent();
  }

  private void initUI() {
    waitingWidget = new WaitingWidget();
    HTMLPanel pnl = new HTMLPanel("");
    pnl.setStyleName(UI.STYLES.bite_moduleContent());
    HorizontalPanel newCreditType = createNewCreditTypeRow();
    pnl.add(newCreditType);
    pnl.add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    pnl.add(waitingWidget);
    pnl.add(table);
    add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    add(pnl);
    deleteRoleGroupDelegate = new Delegate<CreditType>() {
      @Override
      public void execute(final CreditType credit) {
        SettingsServiceLocator.getCreditTypeServlet().deleteCreditType(credit.getId(), new BaseAsyncCallback<RpcStatus>() {
          @Override
          public void onSuccess(RpcStatus result) {
            if (Window.confirm(AdminUI.ADMINCOMMONTEXTPOOL.credittypeDeleteQuestion())) {
              ModelData<CreditType> m = new ModelData<CreditType>(credit);
              waitingWidget.setText(AdminUI.ADMINCOMMONTEXTPOOL.credittypeMessageDelete());
              waitingWidget.show();
              m.remove(credit);
              waitingWidget.hide();
              loadCredits();
            }
          }

          @Override
          public void onFailure(Throwable caught) {
            waitingWidget.hide();
            Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.messageboxDeleteError());
            loadCredits();
          }
        });

      }
    };
  }

  private void initTable() {
    table = new DataTable<CreditType>(createColumns());
    table.enablePaging(10);
    table.setWidth("1000px");
    table.setVisible(false);
  }

  private void registerUpdateCreditsListener() {
    PortletEventManager.addListener(CuCoEventType.UPDATECREDIT_TYPES, new PortletEventListener<AddCreditTypeEvent>() {

      @Override
      public void handleEvent(AddCreditTypeEvent be) {
        init();
        loadCredits();
      }
    });
  }

  public void loadCredits() {
    waitingWidget.setVisible(true);
    table.setVisible(false);

    table.getStore().clear();

    SettingsServiceLocator.getCreditTypeServlet().getAllCreditTypes(new BaseAsyncCallback<ArrayList<CreditType>>(this) {

      @Override
      public void onSuccess(ArrayList<CreditType> result) {
        ArrayList<ModelData<CreditType>> results = new ArrayList<ModelData<CreditType>>();

        for (CreditType credit : result) {
          ModelData<CreditType> m = new ModelData<CreditType>(credit);
          m.put("bean", credit);
          m.put("name", credit.getName());
          m.put("description", credit.getDescription());
          m.put("active", credit.getActive());
          results.add(m);
        }

        table.getStore().add(results);
        waitingWidget.setVisible(false);
        table.setVisible(true);
      }
    });
  }

  private void registerUpdateCreditListener() {
    PortletEventManager.addListener(CuCoEventType.UPDATECREDIT_TYPES, new PortletEventListener<AddCreditTypeEvent>() {

      @Override
      public void handleEvent(AddCreditTypeEvent event) {
        CreditType credit = event.getCredit();
        ModelData<CreditType> model = table.getStore().get(credit);
        if (model != null) {
          model.setBean(credit);
        } else {
          model = new ModelData<CreditType>(credit);
          model.put("bean", credit);
          model.put("name", credit.getName());
          model.put("description", credit.getDescription());
          model.put("active", credit.getActive());
          table.getStore().add(model);
        }
      }
    });
  }

  private HorizontalPanel createNewCreditTypeRow() {
    HorizontalPanel newCredit = new HorizontalPanel();
    newCredit.add(createNewCreditTypeButton());
    return newCredit;
  }

  private Widget createNewCreditTypeButton() {
    Button btnCreateCreditType = new Button(AdminUI.ADMINCOMMONTEXTPOOL.credittypeNew(), ButtonSize.Small);
    editCreditTypesDialog = new EditCreditTypesDialog();

    btnCreateCreditType.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        // editCreditTypeDialog = new EditCreditTypeDialog();
        editCreditTypesDialog.show(null);
      }
    });
    return btnCreateCreditType;
  }

  private ArrayList<Column<CreditType>> createColumns() {
    ArrayList<Column<CreditType>> columns = new ArrayList<Column<CreditType>>();
    columns.add(new Column<CreditType>("name", AdminUI.ADMINCOMMONTEXTPOOL.credittypeGridColumnName(), "20%", createCreditTypeCellRenderer()));
    columns.add(new Column<CreditType>("description", AdminUI.ADMINCOMMONTEXTPOOL.credittypeGridColumnDescription(), "30%"));
    columns.add(new Column<CreditType>("active", AdminUI.ADMINCOMMONTEXTPOOL.credittypeGridColumnActive(), "25%"));
    columns.add(new Column<CreditType>("delete", AdminUI.ADMINCOMMONTEXTPOOL.credittypeGridColumnDelete(), "25%", createDeleteCellRenderer()));
    return columns;
  }

  private CellRenderer<CreditType> createCreditTypeCellRenderer() {
    return new CellRenderer<CreditType>() {
      @Override
      public Widget render(final ModelData<CreditType> model, String columnId, int rowId) {
        Anchor link = new Anchor(model.getBean().getName());
        link.addClickHandler(new ClickHandler() {
          @Override
          public void onClick(ClickEvent event) {
            SettingsServiceLocator.getCreditTypeServlet().getAllCreditTypes(new BaseAsyncCallback<ArrayList<CreditType>>() {

              @Override
              public void onSuccess(ArrayList<CreditType> result) {
                editCreditTypesDialog.show(model.getBean());
              }
            });

          }
        });
        return link;
      }
    };
  }

  private CellRenderer<CreditType> createDeleteCellRenderer() {
    return new CellRenderer<CreditType>() {
      @Override
      public IsWidget render(final ModelData<CreditType> model, String columnId, int rowId) {
        return new ClickableIcon<CreditType>(model.getBean(), deleteRoleGroupDelegate, UI.IMAGES.iconDelete(), null);
      }
    };
  }

  @Override
  public void init() {}
}
