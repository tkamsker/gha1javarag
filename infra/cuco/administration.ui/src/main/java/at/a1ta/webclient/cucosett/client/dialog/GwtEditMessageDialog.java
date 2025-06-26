package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.google.gwt.core.client.GWT;
import com.google.gwt.core.client.Scheduler;
import com.google.gwt.core.client.Scheduler.ScheduledCommand;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.bite.core.shared.dto.systemmessage.SystemMessage;
import at.a1ta.bite.ui.client.PopupFrame;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.CheckBox;
import at.a1ta.bite.ui.client.widget.DateBox;
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.TextArea;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.event.SelectRolesEvent;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.ErrorHandler;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.framework.ui.client.service.SystemMessageServlet;
import at.a1ta.framework.ui.client.service.SystemMessageServletAsync;

public class GwtEditMessageDialog extends Composite {

  // @formatter:off
  private static GwtEditMessageDialogUiBinder uiBinder = GWT.create(GwtEditMessageDialogUiBinder.class);

  interface GwtEditMessageDialogUiBinder extends UiBinder<Widget, GwtEditMessageDialog> {}

  private static GwtEditMessageDialog _instance = null;

  private PopupFrame popupFrame;

  private static SystemMessage message = null;

  private static boolean copy;

  private static long messageId;

  @UiField(provided = true)
  DataTable<Role> roleStore;
  @UiField
  InputBox title;
  @UiField
  TextArea txtText;
  @UiField
  CheckBox checkBoxOneTime;
  @UiField
  CheckBox checkBoxOnlyMenue;
  @UiField
  Button bRoles;
  @UiField
  Button bImage;
  @UiField
  Button bSave;
  @UiField
  Button bCancel;
  @UiField
  DateBox from;
  @UiField
  DateBox to;

  public static GwtEditMessageDialog getInstance() {
    if (_instance == null) {
      _instance = new GwtEditMessageDialog(messageId, copy);
    }
    _instance.title.setValue("");
    _instance.txtText.setValue("");
    _instance.checkBoxOneTime.setValue(true);
    _instance.checkBoxOnlyMenue.setValue(true);
    return _instance;
  }

  public static GwtEditMessageDialog getInstance(SystemMessage message) {
    GwtEditMessageDialog instance = getInstance();
    instance.setSystemMessage(message);
    return instance;
  }

  private void setSystemMessage(SystemMessage message) {
    GwtEditMessageDialog.message = message;
  }

  public GwtEditMessageDialog(long messageId, boolean copy) {
    createTable();
    initWidget(uiBinder.createAndBindUi(this));
    GwtEditMessageDialog.messageId = messageId;
    GwtEditMessageDialog.copy = copy;
    popupFrame = new PopupFrame(this, 500, 360);
    loadMessage();
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

    PortletEventManager.addListener(CuCoEventType.SELECT_ROLES, new PortletEventListener<SelectRolesEvent>() {

      @Override
      public void handleEvent(SelectRolesEvent be) {
        message.getAccessible4roles().clear();
        ArrayList<ModelData<Role>> roles = new ArrayList<ModelData<Role>>();
        for (Role r : be.getRoles()) {
          message.getAccessible4roles().add(r);
          ModelData<Role> help = new ModelData<Role>(r);
          help.put("bean", r);
          help.put("name", r.getName());
          roles.add(help);
        }
        roleStore.getStore().clear();
        roleStore.getStore().add(roles);
      }

    });

    bRoles.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        List<Role> r = new ArrayList<Role>();
        for (ModelData<Role> bm : roleStore.getStore().getAll()) {
          r.add((Role) bm.getBean());
        }
        new GwtSelectRolesDialog().show();
      }

    });
  }

  private void loadMessage() {

    final SystemMessageServletAsync service = (SystemMessageServletAsync) GWT.create(SystemMessageServlet.class);
    service.getMessageById(messageId, new BaseAsyncCallback<SystemMessage>() {

      @Override
      public void onSuccess(SystemMessage result) {
        message = result;

        if (copy) {
          message.setId(0L);
        }

        title.setValue(result.getMessageContent().getTitle());
        txtText.setText(result.getMessageContent().getText());
        from.setValue(result.getPeriodOfValidity().getValidFrom());
        to.setValue(result.getPeriodOfValidity().getValidUntil());
        checkBoxOneTime.setValue(result.getPromptOnce());
        checkBoxOnlyMenue.setValue(result.getShowInMenuBar());
        roles();

        Scheduler.get().scheduleDeferred(new ScheduledCommand() {

          @Override
          public void execute() {
            title.focus();
          }
        });
        popupFrame.center();
      }

      @Override
      public void onFailure(Throwable exception) {
        ErrorHandler.onError(exception);
      }
    });

  }

  public void roles() {
    for (Role r : message.getAccessible4roles()) {
      ModelData<Role> bm = new ModelData<Role>(r);
      bm.put("name", r.getName());
      bm.put("bean", r);
      roleStore.getStore().add(bm);
    }
  }

  private void createTable() {
    ArrayList<Column<Role>> columns = new ArrayList<Column<Role>>();
    columns.add(new Column<Role>("name", "", "100%"));
    roleStore = new DataTable<Role>(columns);
    roleStore.setHeight(50);
  }

  private void fillMessage() throws IllegalArgumentException {
    message.getMessageContent().setTitle(title.getValue());
    message.getMessageContent().setText(txtText.getText());
    message.setPromptOnce(checkBoxOneTime.getValue());
    message.setShowInMenuBar(checkBoxOnlyMenue.getValue());

    Date f = from.getValue();
    message.getPeriodOfValidity().setValidFrom(f);
    Date u = to.getValue();
    message.getPeriodOfValidity().setValidUntil(u);
  }

  protected void save() {
    if (message != null) {
      try {
        fillMessage();
        if (message.getMessageContent().getTitle() == null || message.getMessageContent().getTitle().equals("")) {
          Window.alert("Bitte geben sie einen Titel ein!");
          return;
        }
        if (message.getMessageContent().getText() == null || message.getMessageContent().getText().equals("")) {
          Window.alert("Bitte geben sie einen Text ein!");
          return;
        }
        final SystemMessageServletAsync service = (SystemMessageServletAsync) GWT.create(SystemMessageServlet.class);
        service.storeSystemMessage(message, new BaseAsyncCallback<String>() {

          @Override
          public void onSuccess(String result) {
            PortletEventManager.fireEvent(new GenericEvent<Void>(CuCoEventType.LOAD_MESSAGES));
            popupFrame.close();
          }

        });
      } catch (IllegalArgumentException ex) {
        Window.alert("Bitte ein gültiges Datum eingeben (Format: DD.MM.JJJJ)");
      }
    } else {
      popupFrame.close();
    }
  }

  public void show() {
    popupFrame.hideMessageBar();
    popupFrame.showContent();
  }

  public void hide() {
    popupFrame.hide();
  }
}
