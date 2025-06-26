package at.a1ta.webclient.cucosett.client.portlet;

import java.util.ArrayList;
import java.util.List;

import com.extjs.gxt.ui.client.Style.HorizontalAlignment;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.event.BaseEvent;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ChangeEvent;
import com.google.gwt.event.dom.client.ChangeHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.FormPanel.SubmitCompleteEvent;
import com.google.gwt.user.client.ui.FormPanel.SubmitCompleteHandler;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.bite.ui.client.widget.Upload;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.admin.ui.common.client.ui.ImageRenderer;
import at.a1ta.framework.gxt.ui.GridContainer;
import at.a1ta.framework.ui.client.event.PortletEvent;
import at.a1ta.framework.ui.client.event.PortletEventManager;

public class UserShopAssignmentPortlet extends CuCoSettBasePortlet {

  public static final String NAME = "Import Shop - Mitarbeiterzuordnung";
  private GridContainer<ListStore<BaseModelData>, BaseModelData> grid;
  private static UserShopAssignmentPortlet _instance = null;
  private ListStore<BaseModelData> store = new ListStore<BaseModelData>();
  private List<ColumnConfig> configs = new ArrayList<ColumnConfig>();
  private ColumnModel cm;

  public static UserShopAssignmentPortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new UserShopAssignmentPortlet(def);
    }
    return _instance;
  }

  private UserShopAssignmentPortlet(PortletDefinition def) {
    super(def);

    initUI();
    updateGrid();
    showContent();
  }

  private void initUI() {

    add(createRealUploadButton()); // upload button

    ColumnConfig column1 = new ColumnConfig("filename", AdminUI.ADMINCOMMONTEXTPOOL.importusershopdata_logfilename(), 40);
    ColumnConfig column2 = new ColumnConfig("amount", AdminUI.ADMINCOMMONTEXTPOOL.importusershopdata_logentries(), 40);
    ColumnConfig column3 = new ColumnConfig("download", AdminUI.ADMINCOMMONTEXTPOOL.importusershopdata_logdownload(), 10);
    ColumnConfig column4 = new ColumnConfig("delete", AdminUI.ADMINCOMMONTEXTPOOL.importusershopdata_logerase(), 10);

    column3.setToolTip("Logdaten herunterladen");
    column3.setAlignment(HorizontalAlignment.CENTER);
    column3.setRenderer(new ImageRenderer(ImageRenderer.DOWNLOAD, new Listener<BaseEvent>() {
      @Override
      public void handleEvent(BaseEvent be) {
        download();
      }
    }));

    column3.setToolTip("Logdaten löschen");
    column4.setAlignment(HorizontalAlignment.CENTER);
    column4.setRenderer(new ImageRenderer(ImageRenderer.ERASE, new Listener<BaseEvent>() {
      @Override
      public void handleEvent(BaseEvent be) {
        erase();
      }
    }));

    configs.add(column1);
    configs.add(column2);
    configs.add(column3);
    configs.add(column4);

    cm = new ColumnModel(configs);
    store.removeAll();

    grid = new GridContainer<ListStore<BaseModelData>, BaseModelData>(store, cm, 75);
    add(grid);

  }

  private void setLogDataCount(BaseModelData m, String count) {
    m.set("amount", count);
  }

  @Override
  public void init() {}

  private void updateGrid() {
    store.removeAll();

    CommonServiceLocator.getUserShopAssignmentServlet().getLogEntriesCount(new AsyncCallback<Integer>() {

      @Override
      public void onSuccess(Integer result) {
        final BaseModelData m = new BaseModelData();
        m.set("filename", "logdata.csv");

        if (result == 0) {
          return;
        } else if (result == 1) {
          setLogDataCount(m, result.toString() + " Eintrag");
        } else {
          setLogDataCount(m, result.toString() + " Einträge");
        }

        store.add(m);
      }

      @Override
      public void onFailure(Throwable caught) {
        return;
      }

    });
  }

  private Upload createRealUploadButton() {
    final Upload upload = new Upload(ButtonSize.Small, AdminUI.ADMINCOMMONTEXTPOOL.importusershopdata_selectimportfile());
    upload.getForm().setAction(GWT.getModuleBaseURL() + "userShopAssignmentUploadServlet");
    upload.getForm().setEncoding(FormPanel.ENCODING_MULTIPART);
    upload.getForm().setMethod(FormPanel.METHOD_POST);
    upload.setAllowedFileTypes(".csv"); // multiple files with ".csv,.txt"
    upload.getFileUpload().addChangeHandler(new ChangeHandler() {
      @Override
      public void onChange(ChangeEvent event) {
        upload.submit();
      }
    });
    upload.getForm().addSubmitCompleteHandler(new SubmitCompleteHandler() {
      @Override
      public void onSubmitComplete(SubmitCompleteEvent event) {
        updateGrid();
        PortletEventManager.fireEvent(new PortletEvent(this, CuCoEventType.UPDATE_USERS));
      }
    });
    upload.setVisible(true);
    return upload;
  }

  private void download() {
    Window.open(GWT.getModuleBaseURL() + "userShopAssignmentDownloadServlet", null, null);
  }

  private void erase() {
    CommonServiceLocator.getUserShopAssignmentServlet().purgeLogEntries(new AsyncCallback<Void>() {
      @Override
      public void onSuccess(Void result) {
        updateGrid();
      }

      @Override
      public void onFailure(Throwable caught) {
        Window.alert("Beim Löschvorgang ist ein Fehler aufgetreten!");
        updateGrid();
      }
    });
  }

}
