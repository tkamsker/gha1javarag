package at.a1ta.webclient.cucosett.client.portlet;

import java.util.Date;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.i18n.shared.DateTimeFormat;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.bite.ui.client.widget.DateBox;
import at.a1ta.bite.ui.client.widget.DateBox.DateBoxSize;
import at.a1ta.bite.ui.client.widget.Label;

public class CheckUsagePortlet extends CuCoSettBasePortlet {

  public static final String NAME = "Check Usage";

  private static CheckUsagePortlet _instance;
  private DateBox startDateBox;
  private DateBox endDateBox;

  public static CheckUsagePortlet create(PortletDefinition portletDefinition) {
    if (_instance == null) {
      _instance = new CheckUsagePortlet(portletDefinition);
    }
    return _instance;
  }

  private CheckUsagePortlet(PortletDefinition def) {
    super(def);
  }

  private void printSelectBox() {
    getContentPanel().clear();

    HTMLPanel pnlHeight = new HTMLPanel("");
    pnlHeight.setStyleName(UI.STYLES.bite_heightPlaceHolder());
    add(pnlHeight);

    HTMLPanel pnl = new HTMLPanel("");
    pnl.setWidth("100%");
    pnl.setStyleName(UI.STYLES.bite_moduleContent());

    HorizontalPanel hpanel = new HorizontalPanel();
    hpanel.add(pnlHeight);

    startDateBox = new DateBox(DateBoxSize.Short);
    startDateBox.setCaption("Start Date");
    startDateBox.setValue(new Date(new Date().getYear(), 0, 1), true);
    hpanel.add(new Label("Von: "));
    hpanel.add(startDateBox);

    endDateBox = new DateBox(DateBoxSize.Short);
    endDateBox.setCaption("End Date");
    endDateBox.setValue(new Date(), true);
    hpanel.add(new Label("Bis: "));
    hpanel.add(endDateBox);

    Button submitButton = new Button("Report Anfordern", ButtonSize.Small);
    submitButton.addClickHandler(new ClickHandler() {

      @Override
      public void onClick(ClickEvent event) {
        DateTimeFormat formatter = DateTimeFormat.getFormat("MM-yyyy");
        Window.open(GWT.getModuleBaseURL() + "../app/stats/usage.view?start=" + formatter.format(startDateBox.getValue()) + "&end=" + formatter.format(endDateBox.getValue()), "_blank", "menubar=no,location=false,resizable=false,scrollbars=false,status=true,dependent=true");
      }
    });

    pnl.add(hpanel);
    pnl.add(submitButton);

    add(pnl);
  }

  @Override
  public void init() {
    showLoading();
    printSelectBox();
    showContent();
  }

}
