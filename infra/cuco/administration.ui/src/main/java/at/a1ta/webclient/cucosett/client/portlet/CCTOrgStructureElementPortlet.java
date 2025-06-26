package at.a1ta.webclient.cucosett.client.portlet;

import com.google.gwt.core.client.GWT;
import com.google.gwt.dom.client.InputElement;
import com.google.gwt.event.dom.client.ChangeEvent;
import com.google.gwt.event.dom.client.ChangeHandler;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Element;
import com.google.gwt.user.client.Event;
import com.google.gwt.user.client.EventListener;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.ui.FormPanel;
import com.google.gwt.user.client.ui.FormPanel.SubmitCompleteEvent;
import com.google.gwt.user.client.ui.FormPanel.SubmitCompleteHandler;
import com.google.gwt.user.client.ui.HTMLPanel;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.popup.MessagePopup;
import at.a1ta.bite.ui.client.popup.WaitingPopup;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.bite.ui.client.widget.Label;
import at.a1ta.bite.ui.client.widget.Upload;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.ui.common.client.bundle.CuCoUI;

public class CCTOrgStructureElementPortlet extends CuCoSettBasePortlet {
  // @formatter:off
  private final WaitingPopup waitingPopup = new WaitingPopup(AdminUI.ADMINCOMMONTEXTPOOL.portletOrgStructureWaitingMessage(), true, true);

  public static final String NAME = "OrgStructurePortlet";
  private static CCTOrgStructureElementPortlet _instance = null;

  public static synchronized CCTOrgStructureElementPortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new CCTOrgStructureElementPortlet(def);
    }
    return _instance;
  }

  // @formatter:on

  private CCTOrgStructureElementPortlet(PortletDefinition def) {
    super(def);
    initUI();
    showContent();

  }

  private void initUI() {
    HTMLPanel pnl = new HTMLPanel("");
    pnl.setStyleName(UI.STYLES.bite_moduleContent());
    pnl.add(createOrgStructureInfoLabel());
    pnl.add(createRealUploadButton());
    add(pnl);

  }

  private Label createOrgStructureInfoLabel() {
    Label portletInfoLabel = new Label("  " + AdminUI.ADMINCOMMONTEXTPOOL.portletOrgStructureInfo());
    return portletInfoLabel;
  }

  private Upload createRealUploadButton() {
    final Upload upload = new Upload(ButtonSize.Small, AdminUI.ADMINCOMMONTEXTPOOL.importCalcOrgStructure());
    upload.getForm().clear();
    upload.getForm().add(upload.getFileUpload());
    upload.addHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        upload.getForm().reset();
      }
    }, ClickEvent.getType());
    upload.getForm().setAction(GWT.getModuleBaseURL() + "cCTOrgStructureElementUploadServlet");
    upload.getForm().setEncoding(FormPanel.ENCODING_MULTIPART);
    upload.getForm().setMethod(FormPanel.METHOD_POST);
    upload.setAllowedFileTypes(".xlsx"); // multiple files with ".csv,.txt"
    upload.setAllowedFileTypes(".xls"); // multiple files with ".csv,.txt"
    upload.getFileUpload().addChangeHandler(new ChangeHandler() {
      @Override
      public void onChange(ChangeEvent event) {
        if (upload.getFileUpload().getFilename() != null && (upload.getFileUpload().getFilename().trim().endsWith(".xls") || upload.getFileUpload().getFilename().trim().endsWith(".xlsx"))) {
          waitingPopup.show();
          waitingPopup.center();
          upload.submit();
          Timer hideTimer = new Timer() {
            @Override
            public void run() {
              if (waitingPopup.isShowing()) {
                waitingPopup.hide();
                MessagePopup.showError(UI.BITE_TEXTPOOL.hint(), AdminUI.ADMINCOMMONTEXTPOOL.portletOrgStructureFailureReportMessage());
              }
            }
          };
          hideTimer.schedule(15000);
        } else {
          MessagePopup.showError(UI.BITE_TEXTPOOL.hint(), CuCoUI.CUCOCOMMONTEXTPOOL.admin_quoteClearance_err_invalidUserEntries());
        }
      }
    });
    Event.setEventListener(upload.getElement(), new EventListener() {
      @Override
      public void onBrowserEvent(Event event) {
        // work with IE11+ and other modern browsers
        nativeClearFile(upload.getFileUpload().getElement());
        // throw event click
        InputElement.as(upload.getFileUpload().getElement()).click();
      }
    });
    Event.sinkEvents(upload.getElement(), Event.ONCLICK);
    upload.getForm().addSubmitCompleteHandler(new SubmitCompleteHandler() {
      @Override
      public void onSubmitComplete(SubmitCompleteEvent event) {
        waitingPopup.hide();
        if (event.getResults() != null && event.getResults().contains("Success:")) {
          MessagePopup.showInfo(UI.BITE_TEXTPOOL.ok(), AdminUI.ADMINCOMMONTEXTPOOL.portletOrgStructureSuccessMessage());
        } else {
          MessagePopup.showError(UI.BITE_TEXTPOOL.hint(), event.getResults());
        }

      }
    });

    upload.setVisible(true);
    return upload;
  }

  @Override
  public void init() {
    // No Implementation
  }

  private native void nativeClearFile(Element element) /*-{
                                                       element.value = '';
                                                       }-*/;
}