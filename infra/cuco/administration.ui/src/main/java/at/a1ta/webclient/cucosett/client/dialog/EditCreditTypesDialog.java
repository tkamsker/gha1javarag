package at.a1ta.webclient.cucosett.client.dialog;

import java.util.logging.Logger;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.ui.client.PopupFrame;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.CheckBox;
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.TextArea;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.AddCreditTypeEvent;
import at.a1ta.cuco.core.shared.dto.CreditType;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class EditCreditTypesDialog extends Composite {

  // @formatter:off
  private static EditCreditTypesDialogUiBinder uiBinder = GWT.create(EditCreditTypesDialogUiBinder.class);

  private static Logger logger = Logger.getLogger(EditCreditTypesDialog.class.getName());

  interface EditCreditTypesDialogUiBinder extends UiBinder<Widget, EditCreditTypesDialog> {}

  private static EditCreditTypesDialog _instance = null;

  private CreditType ct;

  private PopupFrame popupFrame;

  @UiField
  InputBox name;
  @UiField
  TextArea txtDescription;
  @UiField
  CheckBox checkBoxActive;
  @UiField
  Button bSave;
  @UiField
  Button bCancel;

  public static EditCreditTypesDialog getInstance() {
    if (_instance == null) {
      _instance = new EditCreditTypesDialog();
    }
    _instance.name.setValue("");
    _instance.txtDescription.setValue("");
    _instance.checkBoxActive.setValue(true);
    return _instance;
  }

  public static EditCreditTypesDialog getInstance(CreditType ct) {
    EditCreditTypesDialog instance = getInstance();
    instance.setCreditType(ct);
    return instance;
  }

  private void setCreditType(CreditType ct) {
    this.ct = ct;
    name.setValue(ct.getName());
    txtDescription.setValue(ct.getDescription());
    checkBoxActive.setValue(ct.getActive());
  }

  public EditCreditTypesDialog() {
    initWidget(uiBinder.createAndBindUi(this));
    popupFrame = new PopupFrame(this, 370, 220);
    bSave.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        save();
      }
    });

    bCancel.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        cancel();
      }

      private void cancel() {
        popupFrame.close();
      }
    });

  }

  protected void save() {
    if (!name.validate() || !txtDescription.validate()) {
      Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.credittypeDialogValidation());
      return;
    }
    Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.credittypeMessageSave());
    Window.setStatus(AdminUI.ADMINCOMMONTEXTPOOL.credittypeMessageSave());

    if (ct == null) {
      ct = new CreditType(name.getValue(), txtDescription.getValue(), checkBoxActive.getValue());
    } else {
      ct.setName(name.getValue());
      ct.setDescription(txtDescription.getValue());
      ct.setActive(checkBoxActive.getValue());
    }
    SettingsServiceLocator.getCreditTypeServlet().saveCreditType(ct, new BaseAsyncCallback<CreditType>() {

      @Override
      public void onSuccess(CreditType result) {
        PortletEventManager.fireEvent(new AddCreditTypeEvent(ct));
        popupFrame.close();
      }

      @Override
      public void onFailure(Throwable exception) {
        Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.messageboxSaveError());
      }
    });
  }

  public void show(CreditType credit) {
    if (credit == null) {
      name.clear();
      txtDescription.clear();
    } else {
      ct = credit;
      name.setText(credit.getName());
      txtDescription.setText(credit.getDescription());
      checkBoxActive.setValue(credit.getActive());
    }
    popupFrame.hideMessageBar();
    popupFrame.showContent();
  }

  public void hide() {
    popupFrame.hide();
  }
}
