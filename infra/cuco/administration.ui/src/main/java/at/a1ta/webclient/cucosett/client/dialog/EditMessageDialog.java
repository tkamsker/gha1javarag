package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.ListView;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.CheckBox;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.google.gwt.core.client.GWT;
import com.google.gwt.core.client.Scheduler;
import com.google.gwt.core.client.Scheduler.ScheduledCommand;
import com.google.gwt.i18n.client.DateTimeFormat;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Grid;
import com.google.gwt.user.client.ui.Image;

import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.bite.core.shared.dto.systemmessage.SystemMessage;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.event.SelectRolesEvent;
import at.a1ta.framework.gxt.ui.Util;
import at.a1ta.framework.ui.client.ErrorHandler;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.framework.ui.client.service.ServiceLocator;
import at.a1ta.framework.ui.client.service.SystemMessageServlet;
import at.a1ta.framework.ui.client.service.SystemMessageServletAsync;
import at.a1ta.framework.ui.client.tinymce.CuCoTinyMCEConfiguration;
import at.a1ta.framework.ui.client.tinymce.TinyMCE;
import at.a1ta.framework.ui.client.util.Validator;

public class EditMessageDialog extends Dialog {

  private Grid grid;
  private TextField<String> title = new TextField<String>();
  private TinyMCE editor = new TinyMCE(50, 15, new CuCoTinyMCEConfiguration());
  private TextField<String> from = new TextField<String>();
  private TextField<String> until = new TextField<String>();
  private CheckBox once = new CheckBox();
  private CheckBox menue = new CheckBox();
  private SystemMessage message = null;
  private ButtonListener listener = new ButtonListener();
  private DateTimeFormat fmt = DateTimeFormat.getFormat("dd.MM.yyyy");
  private Button selectImage = new Button(AdminUI.ADMINCOMMONTEXTPOOL.smPickImage());
  private Image img = new Image("");
  private Button deleteImage;

  private boolean copy;
  private ListStore<BaseModelData> roleStore = new ListStore<BaseModelData>();
  private long messageId;

  public EditMessageDialog(String header, long messageId, boolean copy) {
    this.messageId = messageId;
    setModal(true);
    setHeading(header);
    okText = AdminUI.ADMINCOMMONTEXTPOOL.save();
    cancelText = AdminUI.ADMINCOMMONTEXTPOOL.cancel();
    setButtons(OKCANCEL);
    setMinHeight(600);
    setWidth(650);

    setClosable(true);
    setLayoutOnChange(true);
    setBodyBorder(false);
    setBorders(false);
    setResizable(false);

    this.copy = copy;

    if (this.messageId != 0 && !copy) {
      Button delete = new Button(AdminUI.ADMINCOMMONTEXTPOOL.delete());
      delete.addSelectionListener(listener);
      getButtonBar().add(delete);
    }
    selectImage.addSelectionListener(listener);

    PortletEventManager.addListener(CuCoEventType.SELECT_ROLES, new PortletEventListener<SelectRolesEvent>() {

      @Override
      public void handleEvent(SelectRolesEvent be) {
        message.getAccessible4roles().clear();
        List<BaseModelData> roles = new ArrayList<BaseModelData>();
        for (Role r : be.getRoles()) {
          message.getAccessible4roles().add(r);
          BaseModelData help = new BaseModelData();
          help.set("name", r.getName());
          help.set("bean", r);
          roles.add(help);
        }

        roleStore.removeAll();

        roleStore.add(roles);
      }
    });

  }

  @Override
  protected void beforeRender() {

    final SystemMessageServletAsync service = (SystemMessageServletAsync) GWT.create(SystemMessageServlet.class);
    service.getMessageById(messageId, new BaseAsyncCallback<SystemMessage>() {

      @Override
      public void onSuccess(SystemMessage result) {
        message = result;

        if (copy) {
          message.setId(0L);
        }

        grid = new Grid(7, 2);
        String[] labels = {AdminUI.ADMINCOMMONTEXTPOOL.smTitle(), AdminUI.ADMINCOMMONTEXTPOOL.smText(), AdminUI.ADMINCOMMONTEXTPOOL.smValidity(), AdminUI.ADMINCOMMONTEXTPOOL.smOptions(),
            AdminUI.ADMINCOMMONTEXTPOOL.smRoles(), AdminUI.ADMINCOMMONTEXTPOOL.smImageFile()};
        for (int i = 0; i < labels.length; ++i) {
          grid.setText(i, 0, labels[i]);
        }

        title.setValue(result.getMessageContent().getTitle());
        grid.setWidget(0, 1, title);

        editor.setWidth("100%");
        editor.setText(result.getMessageContent().getText());
        grid.setWidget(1, 1, editor);

        Grid g = new Grid(1, 4);
        g.setText(0, 0, AdminUI.ADMINCOMMONTEXTPOOL.smFrom());
        from.setValue(fmt.format(result.getPeriodOfValidity().getValidFrom()));
        g.setWidget(0, 1, from);
        g.setText(0, 2, AdminUI.ADMINCOMMONTEXTPOOL.smUntil());
        until.setValue(fmt.format(result.getPeriodOfValidity().getValidUntil()));
        g.setWidget(0, 3, until);
        grid.setWidget(2, 1, g);

        g = new Grid(2, 1);
        once.setValue(result.getPromptOnce());
        once.setBoxLabel(AdminUI.ADMINCOMMONTEXTPOOL.smOptionsOneTime());
        g.setWidget(0, 0, once);
        menue.setValue(result.getShowInMenuBar());
        menue.setBoxLabel(AdminUI.ADMINCOMMONTEXTPOOL.smOptionsOnlyMenue());
        g.setWidget(1, 0, menue);
        grid.setWidget(3, 1, g);

        g = new Grid(1, 2);
        Button b = new Button("Rollen auswählen");
        b.addSelectionListener(new SelectionListener<ButtonEvent>() {

          @Override
          public void componentSelected(ButtonEvent ce) {
            List<Role> r = new ArrayList<Role>();
            for (BaseModelData bm : roleStore.getModels()) {
              r.add((Role) bm.get("bean"));
            }
            new SelectRolesDialog("Rolle auswählen", r).show();
          }
        });

        for (Role r : message.getAccessible4roles()) {
          BaseModelData bm = new BaseModelData();
          bm.set("name", r.getName());
          bm.set("bean", r);
          roleStore.add(bm);
        }
        g.setWidget(0, 1, b);
        ListView<BaseModelData> roles = new ListView<BaseModelData>();
        roles.setStore(roleStore);
        roles.setDisplayProperty("name");
        roles.setHeight(75);
        roles.setWidth(200);
        g.setWidget(0, 0, roles);

        grid.setWidget(4, 1, g);

        g = new Grid(1, 2);

        deleteImage = new Button(AdminUI.ADMINCOMMONTEXTPOOL.smDeleteImage());
        deleteImage.addSelectionListener(new SelectionListener<ButtonEvent>() {

          @Override
          public void componentSelected(ButtonEvent ce) {
            message.getMessageContent().setImageUri("");
            img.setUrl("");
            img.setVisible(false);
            deleteImage.setVisible(false);
          }
        });
        g.setWidget(0, 1, deleteImage);

        img.setUrl(Util.getExtImgPath() + message.getMessageContent().getImageUri());
        if (Validator.isNullOrEmpty(message.getMessageContent().getImageUri())) {
          img.setVisible(false);
          deleteImage.setVisible(false);
        } else {
          img.setVisible(true);
          deleteImage.setVisible(true);
        }
        g.setWidget(0, 0, img);

        grid.setWidget(5, 1, g);
        grid.setWidget(6, 0, selectImage);

        grid.setWidth("100%");
        add(grid);
        Scheduler.get().scheduleDeferred(new ScheduledCommand() {

          @Override
          public void execute() {
            title.focus();
          }
        });
        center();
      }

      @Override
      public void onFailure(Throwable exception) {
        ErrorHandler.onError(exception);
      }
    });

  }

  private void fillMessage() throws IllegalArgumentException {
    message.getMessageContent().setTitle(title.getValue());
    message.getMessageContent().setText(editor.getText());
    message.setPromptOnce(once.getValue());
    message.setShowInMenuBar(menue.getValue());

    Date f = fmt.parseStrict(from.getValue());
    message.getPeriodOfValidity().setValidFrom(f);
    Date u = fmt.parseStrict(until.getValue());
    message.getPeriodOfValidity().setValidUntil(u);
  }

  @Override
  protected void onButtonPressed(final Button button) {
    if (button == getButtonBar().getItemByItemId(OK)) {
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
              hide(button);
            }

          });
        } catch (IllegalArgumentException ex) {
          Window.alert("Bitte ein gültiges Datum eingeben (Format: DD.MM.JJJJ)");
        }
      }
    } else {
      hide(button);
    }
  }

  private class ButtonListener extends SelectionListener<ButtonEvent> {

    @Override
    public void componentSelected(ButtonEvent ce) {
      if (ce.getButton() != selectImage) {
        ServiceLocator.getSystemMessageService().deleteSystemMessage(message, new BaseAsyncCallback<String>() {
          @Override
          public void onSuccess(String result) {
            hide();
          }
        });
      }
    }
  }
}
