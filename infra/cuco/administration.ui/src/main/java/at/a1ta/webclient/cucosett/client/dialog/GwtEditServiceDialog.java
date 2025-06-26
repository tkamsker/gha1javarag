package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;
import java.util.List;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.i18n.client.NumberFormat;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.systemmessage.PeriodOfValidity;
import at.a1ta.bite.ui.client.PopupFrame;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.DateBox;
import at.a1ta.bite.ui.client.widget.Icon;
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.ListBox;
import at.a1ta.bite.ui.client.widget.TextArea;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.core.shared.dto.ChargingType;
import at.a1ta.cuco.core.shared.dto.CreditType;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class GwtEditServiceDialog extends Composite {

  // @formatter:off
  private static GwtEditServiceDialogUiBinder uiBinder = GWT.create(GwtEditServiceDialogUiBinder.class);

  interface GwtEditServiceDialogUiBinder extends UiBinder<Widget, GwtEditServiceDialog> {}

  @UiField
  InputBox name;
  @UiField
  InputBox cost;
  @UiField
  InputBox product;
  @UiField
  InputBox reason1;
  @UiField
  InputBox reason2;
  @UiField
  InputBox reason3;
  @UiField
  InputBox result;
  @UiField
  InputBox multi;
  @UiField
  InputBox productCode;

  @UiField
  TextArea description;
  @UiField
  TextArea employeeinfo;

  @UiField
  Icon iconInfo;

  @UiField
  ListBox<ChargingType> chargingType;
  @UiField
  ListBox<CreditType> creditType;

  @UiField
  Button bSave;
  @UiField
  Button bCancel;

  @UiField
  DateBox from;
  @UiField
  DateBox to;

  // @formatter:on

  private static GwtEditServiceDialog _instance = null;

  private Service service = null;

  private NumberFormat decimal = NumberFormat.getFormat("0.00");
  private PopupFrame popupFrame;

  public static GwtEditServiceDialog getInstance() {
    if (_instance == null) {
      _instance = new GwtEditServiceDialog();
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

  public static GwtEditServiceDialog getInstance(Service service) {
    GwtEditServiceDialog instance = getInstance();
    instance.setService(service);
    return instance;
  }

  private void setService(Service service) {
    this.service = service;
    _instance.name.setValue(service.getName());
    _instance.description.setValue(service.getComment());
    _instance.from.setValue(service.getValidity().getValidFrom());
    _instance.to.setValue(service.getValidity().getValidUntil());
    _instance.cost.setValue(decimal.format(service.getCosts()) + " €");
    _instance.multi.setValue(service.getMulti().toString());
    _instance.productCode.setValue(service.getProductCode());
    _instance.product.setValue(service.getProduct());
    _instance.reason1.setValue(service.getReason1());
    _instance.reason2.setValue(service.getReason2());
    _instance.result.setValue(service.getResult());
    _instance.employeeinfo.setValue(service.getEmployeeinfo());
  }

  public GwtEditServiceDialog() {
    initWidget(uiBinder.createAndBindUi(this));
    popupFrame = new PopupFrame(this, 650, 500);
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
    iconInfo.setText(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogCostsTooltip());
  }

  protected void save() {
    if (!name.validate() || !productCode.validate() || !cost.validate() || !description.validate() || !employeeinfo.validate() || !multi.validate() || !product.validate() || !reason1.validate()
        || !reason2.validate() || !reason3.validate() || !result.validate()) {
      Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogValidation());
      return;
    }

    if (service == null) {
      service = new Service();
    }
    service.setCreditType(creditType.getSelectedValue());
    service.setName(name.getValue());
    service.setProduct(product.getValue());
    service.setProductCode(productCode.getValue());
    service.setReason1(reason1.getValue());
    service.setReason2(reason2.getValue());
    service.setReason3(reason3.getValue());
    service.setResult(result.getValue());
    service.setValidity(new PeriodOfValidity(from.getValue(), to.getValue()));

    service.setChargingType(chargingType.getSelectedValue());
    service.setComment(description.getValue());
    if (employeeinfo.getValue() != null) {
      service.setEmployeeinfo(employeeinfo.getValue().replaceAll("\n", "<br>"));
    }
    try {
      service.setCosts(decimal.parse(cost.getValue()));
    } catch (NumberFormatException e) {
      popupFrame.close();
      Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogValidationCosts());
      return;
    }
    try {
      if (!multi.getValue().isEmpty()) {
        service.setMulti(new Long(multi.getValue()));
      } else {
        service.setMulti(null);
      }
    } catch (NumberFormatException e) {
      popupFrame.close();
      Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.serviceDialogValidationMulti());
      return;
    }

    CommonServiceLocator.getServiceServlet().saveService(service, new BaseAsyncCallback<Service>() {

      @Override
      public void onSuccess(Service result) {
        PortletEventManager.fireEvent(new GenericEvent<Void>(CuCoEventType.UPDATE_SERVICES));
        popupFrame.close();

      }

      @Override
      public void onFailure(Throwable exception) {
        Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.messageboxSaveError());
        popupFrame.close();
      }
    });
  }

  protected void hide() {
    popupFrame.hide();
  }

  public void onShow() {
    SettingsServiceLocator.getCreditTypeServlet().getAllCreditTypes(new BaseAsyncCallback<ArrayList<CreditType>>() {

      @Override
      public void onSuccess(ArrayList<CreditType> result) {
        for (CreditType ct : result) {
          creditType.addItem(ct.getName(), ct);
        }
        creditType.setEnabled(true);
      }
    });

    SettingsServiceLocator.getChargingTypeServlet().getAllChargingTypes(new BaseAsyncCallback<List<ChargingType>>() {

      @Override
      public void onSuccess(List<ChargingType> result) {
        for (ChargingType ct : result) {
          chargingType.addItem(ct.getName(), ct);
        }
        chargingType.setEnabled(true);
      }
    });
  }

  public void show(Service service) {
    if (service == null) {
      name.clear();
      description.clear();
      from.setValue(null);
      to.setValue(null);
      cost.clear();
      multi.clear();
      productCode.clear();
      product.clear();
      reason1.clear();
      reason2.clear();
      reason3.clear();
      result.clear();
      employeeinfo.clear();
      creditType.setSelectedIndex(0);
      chargingType.setSelectedIndex(0);
    } else {
      chargingType.clear();
      creditType.clear();
      this.service = service;
      name.setValue(service.getName());
      description.setValue(service.getComment());
      from.setValue(service.getValidity().getValidFrom());
      to.setValue(service.getValidity().getValidUntil());
      cost.setValue(service.getCosts().toString());
      multi.setValue(service.getMulti().toString());
      productCode.setValue(service.getProductCode());
      product.setValue(service.getProduct());
      reason1.setValue(service.getReason1());
      reason2.setValue(service.getReason2());
      reason3.setValue(service.getReason3());
      reason3.setEnabled(false);
      result.setValue(service.getResult());
      employeeinfo.setValue(service.getEmployeeinfo());
      chargingType.addItem(service.getChargingType().getName(), service.getChargingType());
      creditType.addItem(service.getCreditType().getName(), service.getCreditType());
    }
    onShow();
    popupFrame.hideMessageBar();
    popupFrame.showContent();
  }
}
