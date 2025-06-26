package at.a1ta.webclient.cucosett.client.portlet;

import java.util.ArrayList;
import java.util.HashMap;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.ScrollPanel;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.popup.WaitingPopup;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.core.bean.Reporting;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.cuco.ui.common.client.ui.table.TableDataStore;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;
import at.a1ta.webclient.cucosett.client.ui.ReportingWidget;

public class ReportingPortlet extends CuCoSettBasePortlet {
  // @formatter:off
  private final WaitingPopup waitingPopup = new WaitingPopup("Das Erstellen des Reports kann einige Minuten dauern.", false, true);

  public static final String NAME = "Reporting";
  private static ReportingPortlet _instance = null;
  private DataTable<Reporting> tblReportings;
  private VerticalPanel tablesPanel;
  private VerticalPanel errorsPanel;

  public static ReportingPortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new ReportingPortlet(def);
    }
    return _instance;
  }

  // @formatter:on

  private ReportingPortlet(PortletDefinition def) {
    super(def);

    CellRenderer<Reporting> loadRenderer = new CellRenderer<Reporting>() {
      @Override
      public Widget render(final ModelData<Reporting> model, String columnId, int rowId) {
        Button button = new Button(AdminUI.ADMINCOMMONTEXTPOOL.reportingButtonLoad(), ButtonSize.Small);
        button.addClickHandler(new ClickHandler() {
          @Override
          public void onClick(ClickEvent event) {
            loadReporting(model.getBean());
          }
        });
        return button;
      }
    };

    CellRenderer<Reporting> excelExportRenderer = new CellRenderer<Reporting>() {
      @Override
      public Widget render(final ModelData<Reporting> model, String columnId, int rowId) {
        Button button = new Button("Excel", ButtonSize.Small);
        button.addClickHandler(new ClickHandler() {
          @Override
          public void onClick(ClickEvent event) {
            loadExcelReport(model.getBean());
          }
        });
        return button;
      }
    };

    CellRenderer<Reporting> nameRenderer = new CellRenderer<Reporting>() {
      @Override
      public Widget render(final ModelData<Reporting> model, String columnId, int rowId) {
        return new Label(model.get(columnId).toString());
      }
    };

    CellRenderer<Reporting> queryRenderer = new CellRenderer<Reporting>() {
      @Override
      public Widget render(final ModelData<Reporting> model, String columnId, int rowId) {
        String origQuery = model.get(columnId).toString();
        String query = origQuery;
        if (query.length() > 80) {
          query = query.replaceAll("<br/>", " ").substring(0, 80) + " ...";
        } else {
          query = query.replaceAll("<br/>", " ");
        }

        Label label = new Label(query);
        label.setTitle(origQuery);

        return label;
      }
    };

    ArrayList<Column<Reporting>> columnData = new ArrayList<Column<Reporting>>();
    columnData.add(new Column<Reporting>("id", AdminUI.ADMINCOMMONTEXTPOOL.reportingGridHeadId(), "5%"));
    columnData.add(new Column<Reporting>("name", AdminUI.ADMINCOMMONTEXTPOOL.reportingGridHeadName(), "30%", nameRenderer));
    columnData.add(new Column<Reporting>("query", AdminUI.ADMINCOMMONTEXTPOOL.reportingGridHeadQuery(), "45%", queryRenderer));
    columnData.add(new Column<Reporting>("longrunning", AdminUI.ADMINCOMMONTEXTPOOL.reportingGridHeadLongrunning(), "8%"));
    columnData.add(new Column<Reporting>("load", "", "7%", loadRenderer));
    columnData.add(new Column<Reporting>("load", "", "5%", excelExportRenderer));

    tblReportings = new DataTable<Reporting>(columnData, new TableDataStore<Reporting>());
    tblReportings.setWidth("100%");
    ScrollPanel pnl1 = new ScrollPanel();
    HTMLPanel pnl = new HTMLPanel("");
    pnl1.add(pnl);
    pnl.setStyleName(UI.STYLES.bite_moduleContent());
    ScrollPanel pnl2 = new ScrollPanel();
    ScrollPanel pnl3 = new ScrollPanel();

    tablesPanel = new VerticalPanel();
    errorsPanel = new VerticalPanel();
    pnl.add(tblReportings);
    pnl.add(new HTML("<hr/>"));
    pnl.add(pnl3);
    pnl.add(new HTML("<hr/>"));
    pnl.add(pnl2);
    pnl2.add(tablesPanel);
    pnl3.add(errorsPanel);
    pnl2.setWidth("100%");
    pnl3.setWidth("100%");
    add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    add(pnl1);

    showContent();
  }

  @Override
  public void init() {
    tblReportings.getStore().clear();

    SettingsServiceLocator.getReportingServlet().getAllReportings(new BaseAsyncCallback<ArrayList<Reporting>>() {

      @Override
      public void onSuccess(ArrayList<Reporting> result) {
        ArrayList<ModelData<Reporting>> models = new ArrayList<ModelData<Reporting>>(result.size());
        for (Reporting report : result) {
          ModelData<Reporting> model = new ModelData<Reporting>(report);
          model.put("id", report.getId());
          model.put("name", report.getName());
          model.put("query", report.getQuery());
          model.put("longrunning", report.isLongRunning());
          models.add(model);
        }
        tblReportings.getStore().add(models);
      }
    });
  }

  private void loadReporting(final Reporting report) {
    clearErrorArea();
    waitingPopup.center();
    SettingsServiceLocator.getReportingServlet().executeReporting(report.getId(), new BaseAsyncCallback<ArrayList<HashMap<String, Object>>>() {
      @Override
      public void onSuccess(ArrayList<HashMap<String, Object>> result) {
        waitingPopup.hide();
        if (result.size() > 0) {
          ArrayList<Column<HashMap<String, Object>>> columnData = new ArrayList<Column<HashMap<String, Object>>>();
          for (String col : result.get(0).keySet()) {
            columnData.add(new Column<HashMap<String, Object>>(col, col, null));
          }
          ArrayList<ModelData<HashMap<String, Object>>> models = new ArrayList<ModelData<HashMap<String, Object>>>(result.size());
          for (HashMap<String, Object> row : result) {
            ModelData<HashMap<String, Object>> model = new ModelData<HashMap<String, Object>>(row);
            for (String col : row.keySet()) {
              model.put(col, row.get(col));
            }
            models.add(model);
          }
          DataTable<HashMap<String, Object>> table = new DataTable<HashMap<String, Object>>(columnData, new TableDataStore<HashMap<String, Object>>());
          table.getStore().add(models);
          ReportingWidget rwidget = new ReportingWidget(table, report.getId());
          rwidget.setHeight("400px");
          addTableToPanel(rwidget);
        } else {
          int position = getPositionForTableId(report.getId());
          if (position > -1) {
            tablesPanel.remove(position);
          }
        }
      }

      @Override
      public void onFailure(Throwable exception) {
        waitingPopup.hide();
        updateErrorArea(exception, report.getQuery());
      }

    });
  }

  private void loadExcelReport(final Reporting report) {
    waitingPopup.center();
    clearErrorArea();
    SettingsServiceLocator.getReportingServlet().exportReportAsExcel(report.getId(), new BaseAsyncCallback<String>() {
      @Override
      public void onSuccess(String result) {
        waitingPopup.hide();
        Window.open(GWT.getModuleBaseURL() + "file.view?id=" + result, "_self", null);
      }

      @Override
      public void onFailure(Throwable exception) {
        waitingPopup.hide();
        updateErrorArea(exception, report.getQuery());
      }

    });
  }

  private void updateErrorArea(Throwable exception, String query) {
    clearErrorArea();
    Label label = new Label("Fehler beim Ausführen der Query: \n" + query + "\n\nEs ist ein Fehler aufgetreten:\n" + exception.getMessage());
    label.getElement().getStyle().setProperty("whiteSpace", "pre");
    label.getElement().getStyle().setColor("red");
    errorsPanel.add(label);
  }

  private void clearErrorArea() {
    for (int i = 0; i < errorsPanel.getWidgetCount(); i++) {
      errorsPanel.remove(i);
    }
  }

  private int getPositionForTableId(long id) {
    for (int i = 0; i < tablesPanel.getWidgetCount(); i++) {
      ReportingWidget help = (ReportingWidget) tablesPanel.getWidget(i);
      if (help.getId() == id) {
        return i;
      }
    }
    return -1;
  }

  private void addTableToPanel(ReportingWidget rwidget) {
    int position = getPositionForTableId(rwidget.getId());
    if (position > -1) {
      tablesPanel.remove(position);
      tablesPanel.insert(rwidget, position);
    } else {
      tablesPanel.add(rwidget);
    }
  }
}
