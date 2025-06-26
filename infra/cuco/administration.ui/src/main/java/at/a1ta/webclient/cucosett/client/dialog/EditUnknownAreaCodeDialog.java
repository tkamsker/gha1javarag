package at.a1ta.webclient.cucosett.client.dialog;

import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.TextArea;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.google.gwt.user.client.ui.FlexTable;
import com.google.gwt.user.client.ui.HTML;

import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventManager;

public class EditUnknownAreaCodeDialog extends Dialog {

  private static EditUnknownAreaCodeDialog _instance = null;

  private UnknownAreaCode code = null;

  private TextField<String> areaCode = new TextField<String>();

  private TextArea description = new TextArea();

  public static EditUnknownAreaCodeDialog getInstance() {
    if (_instance == null) {
      _instance = new EditUnknownAreaCodeDialog();
    }
    _instance.areaCode.setValue("");
    _instance.description.setValue("");
    return _instance;
  }

  public static EditUnknownAreaCodeDialog getInstance(UnknownAreaCode code) {
    EditUnknownAreaCodeDialog instance = getInstance();
    instance.setUnknownAreaCode(code);
    return instance;
  }

  private void setUnknownAreaCode(UnknownAreaCode code) {
    this.code = code;
    areaCode.setValue(code.getAreaCode());
    description.setValue(code.getDescription());
  }

  public EditUnknownAreaCodeDialog() {
    setSize(400, 180);
    setResizable(false);
    okText = AdminUI.ADMINCOMMONTEXTPOOL.dialogSave();
    cancelText = AdminUI.ADMINCOMMONTEXTPOOL.dialogCancel();
    setButtons(Dialog.OKCANCEL);
    setHeading(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeDialogHeading());

    areaCode.addStyleName("field-necessary");
    areaCode.setWidth(300);
    areaCode.setAllowBlank(false);
    description.setWidth(300);
    description.setHeight(80);
    description.setMaxLength(1000);

    FlexTable table = new FlexTable();
    table.setWidget(0, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeDialogNameLabel()));
    table.setWidget(0, 1, areaCode);
    table.setWidget(1, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeDialogDescriptionLabel()));
    table.setWidget(1, 1, description);

    setLayout(new FitLayout());
    add(table);
  }

  @Override
  protected void onButtonPressed(Button button) {
    super.onButtonPressed(button);
    if (button == getButtonById(OK)) {

      if (!areaCode.validate() || !description.validate()) {
        MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeLabel(), AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeDialogValidation(), null);
        return;
      }

      final MessageBox wait = MessageBox.wait(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeLabel(), AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeMessageSave(),
          AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeMessageSave());
      wait.show();

      if (code == null) {
        code = new UnknownAreaCode(areaCode.getValue(), description.getValue());
      } else {
        code.setAreaCode(areaCode.getValue());
        code.setDescription(description.getValue());
      }

      CommonServiceLocator.getUnknownAreaCodeServlet().saveUnknownAreaCode(code, new BaseAsyncCallback<UnknownAreaCode>() {

        @Override
        public void onSuccess(UnknownAreaCode result) {
          wait.close();
          PortletEventManager.fireEvent(new GenericEvent<Void>(CuCoEventType.UPDATEUNKNOWN_AREACODES));
          hide();
        }

        @Override
        public void onFailure(Throwable exception) {
          wait.close();
          MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.unknownareacodeLabel(), AdminUI.ADMINCOMMONTEXTPOOL.messageboxSaveError(), null);
          hide();
        }

      });
    }
    if (button == getButtonById(CANCEL)) {
      hide();
    }
  }

  @Override
  protected void onHide() {
    super.onHide();
    code = null;
  }
}
