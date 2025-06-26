package at.a1ta.webclient.cucosett.client.portlet.vip;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.i18n.client.DateTimeFormat;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.uibinder.client.UiHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.ui.client.util.DateUtils;
import at.a1ta.bite.ui.client.widget.DateBox;
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.ListBox;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.core.shared.dto.VIPHistoryEntry;
import at.a1ta.cuco.core.shared.dto.VipExport;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.cuco.ui.common.client.ui.table.TableDataStore;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;

public class VipSearchComponent extends Composite {
  //@formatter:off
  private static final String EQUALS = "=";
  private static final String AMP = "&";
  private static final int PAGING_SIZE = 20;
  private static final DateTimeFormat SERIALIZATION_DATETIME_FORMAT = DateTimeFormat.getFormat(VipExport.SERIALIZATION_DATE_PATTERN);
  private static VipSearchComponentUiBinder uiBinder = GWT.create(VipSearchComponentUiBinder.class);

  @UiField(provided = true) DataTable<VIPHistoryEntry> vipHistoryTable;
  @UiField DateBox dateFrom;
  @UiField DateBox dateTo;
  @UiField InputBox txtSearch;
  @UiField ListBox comboVipStatus;

  interface VipSearchComponentUiBinder extends UiBinder<Widget, VipSearchComponent> {}
  //@formatter:on

  public VipSearchComponent() {
    createVipHistoryTable();
    initWidget(uiBinder.createAndBindUi(this));

    comboVipStatus.addItem("Alle", "ALL");
    comboVipStatus.addItem("Kein", (String) null);
    comboVipStatus.addItem("1", "1");
    comboVipStatus.addItem("2", "2");
    comboVipStatus.addItem("3", "3");
    comboVipStatus.addItem("4", "4");

    // dateFrom.setFormat(new DateBox.DefaultFormat(DateUtils.getDefaultDateTimeFormat()));
    // dateTo.setFormat(new DateBox.DefaultFormat(DateUtils.getDefaultDateTimeFormat()));
  }

  @UiHandler("btnSearch")
  protected void searchVipHistoryEntries(ClickEvent e) {
    vipHistoryTable.getStore().clear();
    vipHistoryTable.update();

    CommonServiceLocator.getVIPHistoryServlet().getVIPHistory(dateFrom.getValue(), dateTo.getValue(), txtSearch.getValue(), comboVipStatus.getValue(comboVipStatus.getSelectedIndex()), new BaseAsyncCallback<List<VIPHistoryEntry>>() {

      @Override
      public void onSuccess(List<VIPHistoryEntry> result) {
        ArrayList<ModelData<VIPHistoryEntry>> models = new ArrayList<ModelData<VIPHistoryEntry>>();
        for (VIPHistoryEntry vipHistoryEntry : result) {
          ModelData<VIPHistoryEntry> model = new ModelData<VIPHistoryEntry>(vipHistoryEntry);
          model.put("created", vipHistoryEntry.getCreated());
          model.put("customerId", vipHistoryEntry.getCustomerId());
          model.put("name", vipHistoryEntry.getName());
          model.put("reported", vipHistoryEntry.getReported());
          model.put("status", (vipHistoryEntry.getNewStatus() == null ? "kein" : vipHistoryEntry.getNewStatus()));
          models.add(model);
        }
        vipHistoryTable.getStore().add(models);
        vipHistoryTable.update();
      }
    });
  }

  private void createVipHistoryTable() {
    ArrayList<Column<VIPHistoryEntry>> cData = new ArrayList<Column<VIPHistoryEntry>>();
    cData.add(new Column<VIPHistoryEntry>("created", AdminUI.ADMINCOMMONTEXTPOOL.vipCreated(), "20%", new CellRenderer<VIPHistoryEntry>() {

      @Override
      public Widget render(ModelData<VIPHistoryEntry> model, String columnId, int rowId) {
        return new HTML(DateUtils.getDefaultDateTimeFormat().format((Date) model.get(columnId)));
      }
    }));
    cData.add(new Column<VIPHistoryEntry>("customerId", AdminUI.ADMINCOMMONTEXTPOOL.vipCustomerID(), "20%"));
    cData.add(new Column<VIPHistoryEntry>("name", AdminUI.ADMINCOMMONTEXTPOOL.vipName(), "20%"));
    cData.add(new Column<VIPHistoryEntry>("reported", AdminUI.ADMINCOMMONTEXTPOOL.vipReporter(), "20%"));
    cData.add(new Column<VIPHistoryEntry>("status", AdminUI.ADMINCOMMONTEXTPOOL.vipAdminStatus(), "20%"));

    vipHistoryTable = new DataTable<VIPHistoryEntry>(cData, new TableDataStore<VIPHistoryEntry>());
    vipHistoryTable.enablePaging(PAGING_SIZE);
    vipHistoryTable.update();
  }

  @UiHandler("btnExport")
  void export(ClickEvent event) {
    vipHistoryTable.getStore().clear();
    vipHistoryTable.update();

    Window.open(createExportLink(), "Exportieren", "");
  }

  private String createExportLink() {
    String link = GWT.getModuleBaseURL() + "cuco/vipHistory.rpc?action=" + VipExport.EXPORT_ACTION_CSV_BY_SEARCH;

    if (dateFrom.getValue() != null) {
      link += AMP + VipExport.SEARCH_FROM + EQUALS + SERIALIZATION_DATETIME_FORMAT.format(dateFrom.getValue());
    }
    if (dateTo.getValue() != null) {
      link += AMP + VipExport.SEARCH_TO + EQUALS + SERIALIZATION_DATETIME_FORMAT.format(dateTo.getValue());
    }
    if (txtSearch.getValue() != null && !txtSearch.getValue().isEmpty()) {
      link += AMP + VipExport.SEARCH_REPORTER + EQUALS + txtSearch.getValue();
    }
    if (!comboVipStatus.getValue(comboVipStatus.getSelectedIndex()).isEmpty()) {
      link += AMP + VipExport.SEARCH_VIP_STATUS + EQUALS + comboVipStatus.getValue(comboVipStatus.getSelectedIndex());
    }
    return link;
  }
}
