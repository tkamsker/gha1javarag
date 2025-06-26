package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;
import java.util.List;

import com.extjs.gxt.ui.client.Style.Orientation;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.ContentPanel;
import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.ComboBox;
import com.extjs.gxt.ui.client.widget.form.ComboBox.TriggerAction;
import com.extjs.gxt.ui.client.widget.form.TextArea;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.extjs.gxt.ui.client.widget.layout.RowLayout;
import com.google.gwt.i18n.client.DateTimeFormat;
import com.google.gwt.i18n.client.DateTimeFormat.PredefinedFormat;
import com.google.gwt.i18n.client.NumberFormat;
import com.google.gwt.user.client.ui.FlexTable;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.Widget;
import com.google.gwt.user.datepicker.client.DateBox;

import at.a1ta.bite.core.shared.dto.systemmessage.PeriodOfValidity;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.admin.ui.common.client.ui.PortletHelper;
import at.a1ta.cuco.core.shared.dto.ChargingType;
import at.a1ta.cuco.core.shared.dto.CreditType;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.framework.gxt.ui.ComboBoxFix;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.framework.ui.client.util.Validator;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class EditServiceDialog extends Dialog {

  private static EditServiceDialog _instance = null;

  private Service service = null;

  private DateBox from = new DateBox();

  private DateBox to = new DateBox();

  private TextField<String> name = new TextField<String>();

  private TextArea description = new TextArea();

  private TextArea employeeinfo = new TextArea();

  private TextField<String> cost = new TextField<String>();

  private TextField<String> multi = new TextField<String>();

  private TextField<String> productCode = new TextField<String>();

  private ComboBox<BaseModelData> chargingType = new ComboBoxFix<BaseModelData>();

  private ComboBox<BaseModelData> creditType = new ComboBoxFix<BaseModelData>();

  private TextField<String> product = new TextField<String>();

  private TextField<String> reason1 = new TextField<String>();

  private TextField<String> reason2 = new TextField<String>();

  private TextField<String> reason3 = new TextField<String>();

  private TextField<String> result = new TextField<String>();

  private NumberFormat decimal = NumberFormat.getFormat("0.00");

  public static EditServiceDialog getInstance() {
    if (_instance == null) {
      _instance = new EditServiceDialog();
    }
    _instance.name.setValue(null);
    _instance.description.setValue(null);
    _instance.from.setValue(null);
    _instance.to.setValue(null);
    _instance.cost.setValue(null);
    _instance.multi.setValue(null);
    _instance.productCode.setValue(null);
    _instance.product.setValue(null);
    _instance.reason1.setValue(null);
    _instance.reason2.setValue(null);
    _instance.result.setValue(null);
    _instance.employeeinfo.setValue(null);
    return _instance;
  }

  public static EditServiceDialog getInstance(Service service) {
    EditServiceDialog instance = getInstance();
    instance.setService(service);
    return instance;
  }

  private void setService(Service service) {
    this.service = service;
    _instance.name.setValue(service.getName());
    _instance.description.setValue(service.getComment());
    _instance.from.setValue(service.getValidity().getValidFrom());
    _instance.to.setValue(service.getValidity().getValidUntil());
    _instance.cost.setValue(decimal.format(service.getCosts()));
    _instance.multi.setValue(service.getMulti().toString());
    _instance.productCode.setValue(service.getProductCode());
    _instance.product.setValue(service.getProduct());
    _instance.reason1.setValue(service.getReason1());
    _instance.reason2.setValue(service.getReason2());
    _instance.result.setValue(service.getResult());
    _instance.employeeinfo.setValue(service.getEmployeeinfo());
  }

  public EditServiceDialog() {
    setSize(700, 540);
    setResizable(false);
    okText = AdminUI.ADMINCOMMONTEXTPOOL.dialogSave();
    cancelText = AdminUI.ADMINCOMMONTEXTPOOL.dialogCancel();
    setButtons(Dialog.OKCANCEL);
    setHeading(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogHeading());
    setBorders(false);

    from.setFormat(new DateBox.DefaultFormat(DateTimeFormat.getFormat(PredefinedFormat.DATE_SHORT)));
    to.setFormat(new DateBox.DefaultFormat(DateTimeFormat.getFormat(PredefinedFormat.DATE_SHORT)));

    setLayout(new RowLayout(Orientation.VERTICAL));
    add(renderCommonDataBox());
    add(renderBillingDataBox());
    add(renderInteractionDataBox());
  }

  private Widget renderCommonDataBox() {

    name.setWidth(555);
    name.addStyleName("field-necessary");
    name.setAllowBlank(false);
    description.setWidth(555);
    description.setHeight(60);
    description.setMaxLength(2000);
    employeeinfo.setWidth(555);
    employeeinfo.setHeight(60);
    employeeinfo.setMaxLength(500);

    ContentPanel cp = new ContentPanel(new FitLayout());
    cp.setHeading(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogCpServicedata());
    cp.setHeight(210);
    cp.setStyleAttribute("margin-bottom", "5px");

    FlexTable table = new FlexTable();
    table.setWidget(0, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogFromLabel()));
    table.setWidget(0, 1, from);
    table.setWidget(0, 2, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogToLabel()));
    table.setWidget(0, 3, to);
    table.setWidget(1, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogNameLabel()));
    table.setWidget(1, 1, name);
    table.setWidget(2, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogDescription()));
    table.setWidget(2, 1, description);
    table.setWidget(3, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogEmployeeinfo()));
    table.setWidget(3, 1, employeeinfo);

    table.getFlexCellFormatter().setColSpan(1, 1, 3);
    table.getFlexCellFormatter().setColSpan(2, 1, 3);
    table.getFlexCellFormatter().setColSpan(3, 1, 3);
    table.getFlexCellFormatter().setWidth(0, 0, "110px");
    table.getFlexCellFormatter().setWidth(0, 2, "120px");
    table.getFlexCellFormatter().setWidth(0, 3, "150px");

    cp.add(table);
    return cp;
  }

  private Widget renderBillingDataBox() {
    productCode.addStyleName("field-necessary");
    productCode.setAllowBlank(false);
    cost.setWidth(50);
    cost.addStyleName("field-necessary");
    cost.setAllowBlank(false);
    multi.setWidth(50);

    ListStore<BaseModelData> charges = new ListStore<BaseModelData>() {};
    ListStore<BaseModelData> credits = new ListStore<BaseModelData>() {};
    chargingType.setStore(charges);
    chargingType.setAllowBlank(false);
    chargingType.setDisplayField("value");
    chargingType.setForceSelection(true);
    chargingType.setTriggerAction(TriggerAction.ALL);
    chargingType.setEditable(false);
    creditType.setStore(credits);
    creditType.setAllowBlank(false);
    creditType.setDisplayField("value");
    creditType.setForceSelection(true);
    creditType.setTriggerAction(TriggerAction.ALL);
    creditType.setEditable(false);

    ContentPanel cp = new ContentPanel(new FitLayout());
    cp.setHeading(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogCpChargingdata());
    cp.setHeight(85);
    cp.setStyleAttribute("margin-bottom", "5px");

    FlexTable table = new FlexTable();
    table.setWidget(0, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogCostsLabel()));
    table.setWidget(0, 1, PortletHelper.createInfoWidget(cost, AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogCostsTooltip()));
    table.setWidget(0, 2, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogMultiLabel()));
    table.setWidget(0, 3, multi);
    table.setWidget(0, 4, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogProductcodeLabel()));
    table.setWidget(0, 5, productCode);
    table.setWidget(1, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogChargingtypeLabel()));
    table.setWidget(1, 1, chargingType);
    table.setWidget(1, 2, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogCredittypeLabel()));
    table.setWidget(1, 3, creditType);

    table.getFlexCellFormatter().setWidth(0, 0, "110px");
    table.getFlexCellFormatter().setColSpan(1, 1, 3);
    table.getFlexCellFormatter().setWidth(0, 5, "150px");
    table.getFlexCellFormatter().setWidth(0, 4, "120px");
    table.getFlexCellFormatter().setWidth(0, 2, "145px");

    cp.add(table);
    return cp;
  }

  private Widget renderInteractionDataBox() {

    product.setWidth(560);
    product.setMaxLength(120);
    reason1.setWidth(560);
    reason1.setMaxLength(120);
    reason2.setWidth(560);
    reason2.setMaxLength(120);
    reason3.setWidth(560);
    reason3.setMaxLength(120);
    reason3.disable();
    reason3.setValue(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogReason3Value());
    result.setWidth(560);
    result.setMaxLength(120);

    ContentPanel cp = new ContentPanel(new FitLayout());
    cp.setHeading(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogCpClarifydata());
    cp.setHeight(167);

    FlexTable table = new FlexTable();
    table.setWidget(0, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogProductcodeLabel()));
    table.setWidget(0, 1, product);
    table.setWidget(1, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogReason1Label()));
    table.setWidget(1, 1, reason1);
    table.setWidget(2, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogReason2Label()));
    table.setWidget(2, 1, reason2);
    table.setWidget(3, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogReason3Label()));
    table.setWidget(3, 1, reason3);
    table.setWidget(4, 0, new HTML(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogResultLabel()));
    table.setWidget(4, 1, result);

    table.getFlexCellFormatter().setWidth(0, 0, "110px");

    cp.add(table);
    return cp;
  }

  @Override
  protected void onButtonPressed(Button button) {
    super.onButtonPressed(button);
    if (button == getButtonById(OK)) {

      if (!name.validate() || !productCode.validate() || !cost.validate() || !description.validate() || !employeeinfo.validate() || !multi.validate() || !product.validate() || !reason1.validate()
          || !reason2.validate() || !reason3.validate() || !result.validate()) {
        MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.serviceLabel(), AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogValidation(), null);
        return;
      }

      final MessageBox wait = MessageBox.wait(AdminUI.ADMINCOMMONTEXTPOOL.serviceLabel(), AdminUI.ADMINCOMMONTEXTPOOL.serviceMessageSave(), AdminUI.ADMINCOMMONTEXTPOOL.messageboxSave());
      wait.show();

      if (service == null) {
        service = new Service();
      }

      service.setChargingType((ChargingType) chargingType.getSelection().get(0).get("bean"));
      service.setComment(description.getValue());
      if (employeeinfo.getValue() != null) {
        service.setEmployeeinfo(employeeinfo.getValue().replaceAll("\n", "<br>"));
      }
      try {
        service.setCosts(decimal.parse(cost.getValue()));
      } catch (NumberFormatException e) {
        wait.close();
        MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.serviceLabel(), AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogValidationCosts(), null);
        return;
      }
      try {
        if (!Validator.isNullOrEmpty(multi.getValue())) {
          service.setMulti(new Long(multi.getValue()));
        } else {
          service.setMulti(null);
        }
      } catch (NumberFormatException e) {
        wait.close();
        MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.serviceLabel(), AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogValidationMulti(), null);
        return;
      }
      service.setCreditType((CreditType) creditType.getSelection().get(0).get("bean"));
      service.setName(name.getValue());
      service.setProduct(product.getValue());
      service.setProductCode(productCode.getValue());
      service.setReason1(reason1.getValue());
      service.setReason2(reason2.getValue());
      service.setReason3(reason3.getValue());
      service.setResult(result.getValue());
      service.setValidity(new PeriodOfValidity(from.getValue(), to.getValue()));

      CommonServiceLocator.getServiceServlet().saveService(service, new BaseAsyncCallback<Service>() {

        @Override
        public void onSuccess(Service result) {
          wait.close();
          PortletEventManager.fireEvent(new GenericEvent<Void>(CuCoEventType.UPDATE_SERVICES));
          hide();
        }

        @Override
        public void onFailure(Throwable exception) {
          wait.close();
          MessageBox.info(AdminUI.ADMINCOMMONTEXTPOOL.serviceLabel(), AdminUI.ADMINCOMMONTEXTPOOL.messageboxSaveError(), null);
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
    service = null;
  }

  @Override
  public void onShow() {
    super.onShow();
    creditType.getStore().removeAll();
    creditType.disable();
    SettingsServiceLocator.getCreditTypeServlet().getAllCreditTypes(new BaseAsyncCallback<ArrayList<CreditType>>() {

      @Override
      public void onSuccess(ArrayList<CreditType> result) {
        ArrayList<BaseModelData> results = new ArrayList<BaseModelData>();
        BaseModelData actual = null;

        for (CreditType ct : result) {
          BaseModelData m = new BaseModelData();
          m.set("bean", ct);
          m.set("value", ct.getName());

          if (service != null && service.getCreditType().getId().equals(ct.getId())) {
            actual = m;
            results.add(m);
            continue;
          }

          if (ct.getActive()) {
            results.add(m);
          }
        }
        creditType.getStore().add(results);

        ArrayList<BaseModelData> list = new ArrayList<BaseModelData>();
        if (actual == null) {
          list.add(results.get(0));
        } else {
          list.add(actual);
        }
        creditType.setSelection(list);

        creditType.enable();
      }
    });

    chargingType.getStore().removeAll();
    chargingType.disable();
    SettingsServiceLocator.getChargingTypeServlet().getAllChargingTypes(new BaseAsyncCallback<List<ChargingType>>() {

      @Override
      public void onSuccess(List<ChargingType> result) {
        List<BaseModelData> results = new ArrayList<BaseModelData>();
        BaseModelData actual = null;

        for (ChargingType ct : result) {
          BaseModelData m = new BaseModelData();
          m.set("bean", ct);
          m.set("value", ct.getName());
          results.add(m);

          if (service != null && service.getChargingType().getId().equals(ct.getId())) {
            actual = m;
          }
        }
        chargingType.getStore().add(results);

        List<BaseModelData> list = new ArrayList<BaseModelData>();
        if (actual == null) {
          list.add(results.get(0));
        } else {
          list.add(actual);
        }
        chargingType.setSelection(list);

        chargingType.enable();
      }
    });
  }
}
