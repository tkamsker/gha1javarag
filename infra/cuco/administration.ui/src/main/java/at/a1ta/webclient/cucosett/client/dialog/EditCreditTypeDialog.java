package at.a1ta.webclient.cucosett.client.dialog;

import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.TextArea;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.google.gwt.user.client.ui.CheckBox;
import com.google.gwt.user.client.ui.FlexTable;
import com.google.gwt.user.client.ui.HTML;

import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.core.shared.dto.CreditType;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class EditCreditTypeDialog extends Dialog {

  private static EditCreditTypeDialog _instance = null;

  private CreditType ct = null;

  private TextField<String> name = new TextField<String>();

  private TextArea description = new TextArea();

  private CheckBox active = new CheckBox();

  public static EditCreditTypeDialog getInstance() {
    if (_instance == null) {
      _instance = new EditCreditTypeDialog();
    }
    _instance.name.setValue("");
    _instance.description.setValue("");
    _instance.active.setValue(true);
    return _instance;
  }

  public static EditCreditTypeDialog getInstance(CreditType ct) {
    EditCreditTypeDialog instance = getInstance();
    instance.setCreditType(ct);
    return instance;
  }

  private void setCreditType(CreditType ct) {
    this.ct = ct;
    name.setValue(ct.getName());
    description.setValue(ct.getDescription());
    active.setValue(ct.getActive());
  }

  public EditCreditTypeDialog() {
    setSize(400, 200);
    okText = AdminUI.ADMINCOMMONTEXTPOOL.dialogSave();
    cancelText = AdminUI.ADMINCOMMONTEXTPOOL.dialogCancel();
    setButtons(Dialog.OKCANCEL);
    setHeading(AdminUI.ADMINCOMMONTEXTPOOL.credittypeDialogHeading());
    setResizable(false);

    name.addStyleName("field-necessary");
    name.setWidth(300);
    name.setMaxLength(64);
    name.setAllowBlank(false);
    description.setWidth(300);
    description.setHeight(80);
    description.setMaxLength(1000);

    FlexTable table = new FlexTable();
    table.setWidget(0, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.credittypeDialogNameLabel()));
    table.setWidget(0, 1, name);
    table.setWidget(1, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.credittypeDialogDescriptionLabel()));
    table.setWidget(1, 1, description);
    table.setWidget(2, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.credittypeDialogActivLabel()));
    table.setWidget(2, 1, active);

    setLayout(new FitLayout());
    add(table);
  }

  @Override
  protected void onButtonPressed(Button button) {
    super.onButtonPressed(button);
    if (button == getButtonById(OK)) {

      if (!name.validate() || !description.validate()) {
        MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.credittypeLabel(), AdminUI.ADMINCOMMONTEXTPOOL.credittypeDialogValidation(), null);
        return;
      }

      final MessageBox wait = MessageBox.wait(AdminUI.ADMINCOMMONTEXTPOOL.credittypeLabel(), AdminUI.ADMINCOMMONTEXTPOOL.credittypeMessageSave(), AdminUI.ADMINCOMMONTEXTPOOL.credittypeMessageSave());
      wait.show();

      if (ct == null) {
        ct = new CreditType(name.getValue(), description.getValue(), active.getValue());
      } else {
        ct.setName(name.getValue());
        ct.setDescription(description.getValue());
        ct.setActive(active.getValue());
      }

      SettingsServiceLocator.getCreditTypeServlet().saveCreditType(ct, new BaseAsyncCallback<CreditType>() {

        @Override
        public void onSuccess(CreditType result) {
          wait.close();
          PortletEventManager.fireEvent(new GenericEvent<Void>(CuCoEventType.UPDATECREDIT_TYPES));
          hide();
        }

        @Override
        public void onFailure(Throwable exception) {
          wait.close();
          MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.credittypeLabel(), AdminUI.ADMINCOMMONTEXTPOOL.messageboxSaveError(), null);
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
    ct = null;
  }
}
