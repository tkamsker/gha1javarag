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
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.TextArea;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.AddUnknownAreaCodeEvent;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.PortletEventManager;

public class EditUnknownAreasCodeDialog extends Composite {

  // @formatter:off
  private static EditUnknownAreasCodeDialogUiBinder uiBinder = GWT.create(EditUnknownAreasCodeDialogUiBinder.class);

  private static Logger logger = Logger.getLogger(EditUnknownAreasCodeDialog.class.getName());

  interface EditUnknownAreasCodeDialogUiBinder extends UiBinder<Widget, EditUnknownAreasCodeDialog> {}

  private static EditUnknownAreasCodeDialog _instance = null;

  private UnknownAreaCode code;

  private PopupFrame popupFrame;

  @UiField
  InputBox areaCode;
  @UiField
  TextArea txtDescription;
  @UiField
  Button bSave;
  @UiField
  Button bCancel;

  public static EditUnknownAreasCodeDialog getInstance() {
    if (_instance == null) {
      _instance = new EditUnknownAreasCodeDialog();
    }
    _instance.areaCode.setValue("");
    _instance.txtDescription.setValue("");
    return _instance;
  }

  public static EditUnknownAreasCodeDialog getInstance(UnknownAreaCode code) {
    EditUnknownAreasCodeDialog instance = getInstance();
    instance.setUnknownAreaCode(code);
    return instance;
  }

  private void setUnknownAreaCode(UnknownAreaCode code) {
    this.code = code;
    areaCode.setValue(code.getAreaCode());
    txtDescription.setValue(code.getDescription());
  }

  public EditUnknownAreasCodeDialog() {
    initWidget(uiBinder.createAndBindUi(this));
    popupFrame = new PopupFrame(this, 365, 200);
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
    if (!areaCode.validate() || !txtDescription.validate()) {
      Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeDialogValidation());
      return;
    }
    Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeMessageSave());

    if (code == null) {
      code = new UnknownAreaCode(areaCode.getValue(), txtDescription.getValue());
    } else {
      code.setAreaCode(areaCode.getValue());
      code.setDescription(txtDescription.getValue());
    }
    CommonServiceLocator.getUnknownAreaCodeServlet().saveUnknownAreaCode(code, new BaseAsyncCallback<UnknownAreaCode>() {

      @Override
      public void onSuccess(UnknownAreaCode result) {
        PortletEventManager.fireEvent(new AddUnknownAreaCodeEvent(code));
        popupFrame.close();
      }

      @Override
      public void onFailure(Throwable exception) {
        Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.messageboxSaveError());
      }
    });
  }

  public void show(UnknownAreaCode cd) {
    if (cd == null) {
      areaCode.clear();
      txtDescription.clear();
    } else {
      code = cd;
      areaCode.setText(code.getAreaCode());
      txtDescription.setText(code.getDescription());
    }
    popupFrame.hideMessageBar();
    popupFrame.showContent();
  }

  public void hide() {
    popupFrame.hide();
  }
}
