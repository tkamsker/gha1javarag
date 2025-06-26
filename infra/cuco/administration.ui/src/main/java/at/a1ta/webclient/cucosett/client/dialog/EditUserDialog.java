package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.BlurEvent;
import com.google.gwt.event.dom.client.BlurHandler;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.logical.shared.ValueChangeEvent;
import com.google.gwt.event.logical.shared.ValueChangeHandler;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.bite.ui.client.PopupFrame;
import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.CheckBox;
import at.a1ta.bite.ui.client.widget.Label;
import at.a1ta.bite.ui.client.widget.TextArea;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.UserRoleServlet;
import at.a1ta.cuco.admin.ui.common.client.service.UserRoleServletAsync;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventManager;

public class EditUserDialog extends Composite {

  // @formatter:off
  private static EditUserDialogUiBinder uiBinder = GWT.create(EditUserDialogUiBinder.class);

  interface EditUserDialogUiBinder extends UiBinder<Widget, EditUserDialog> {}

  @UiField(provided = true)
  DataTable<Role> dtRoles;
  @UiField
  Label lHeader;
  @UiField
  TextArea taUsers;
  @UiField
  Button bSave;
  // @formatter:on

  private UserRoleServletAsync userRoleServlet = GWT.create(UserRoleServlet.class);
  private PopupFrame popupFrame;

  private UserInfo userInfo;

  public EditUserDialog() {
    createTable();
    initWidget(uiBinder.createAndBindUi(this));
    popupFrame = new PopupFrame(this, 630, 620);
    loadRoles();

    bSave.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        save();
      }
    });

    taUsers.addBlurHandler(new BlurHandler() {
      @Override
      public void onBlur(BlurEvent event) {
        loadUser();
      }
    });
  }

  private void createTable() {
    ArrayList<Column<Role>> columns = new ArrayList<Column<Role>>();
    columns.add(createSelectorColumn());
    columns.add(new Column<Role>("name", "Bezeichnung", "50%"));
    columns.add(new Column<Role>("description", "Beschreibung", "50%"));
    dtRoles = new DataTable<Role>(columns);
    dtRoles.setHeight(450);
  }

  private Column<Role> createSelectorColumn() {
    return new Column<Role>("selector", "", "50px", new CellRenderer<Role>() {
      @Override
      public IsWidget render(final ModelData<Role> model, String columnId, int rowId) {
        final CheckBox cb = new CheckBox();
        cb.setValue((Boolean) model.get("selector"));
        cb.addValueChangeHandler(new ValueChangeHandler<Boolean>() {
          @Override
          public void onValueChange(ValueChangeEvent<Boolean> event) {
            model.put("selector", cb.getValue());
            if (userInfo != null) {
              if (cb.getValue()) {
                userInfo.getRoles().add(model.getBean());
              } else {
                userInfo.getRoles().remove(model.getBean());
              }
            }
          }
        });
        return cb;
      }
    }, false, false);
  }

  private void loadRoles() {
    userRoleServlet.getRolesInGroupsForUser(UserManager.getUserInfo().getId(), new BaseAsyncCallback<ArrayList<Role>>() {
      @Override
      public void onSuccess(ArrayList<Role> result) {
        ArrayList<ModelData<Role>> models = new ArrayList<ModelData<Role>>();
        for (Role role : result) {
          ModelData<Role> model = new ModelData<Role>(role);
          model.put("selector", false);
          model.put("name", role.getName());
          model.put("description", role.getDescription());
          models.add(model);
        }
        dtRoles.getStore().add(models);
        dtRoles.sort("name", true);
        if (userInfo != null) {
          selectRoles();
        }
      }
    });
  }

  private void selectRoles() {
    for (ModelData<Role> model : dtRoles.getStore().getAll()) {
      for (Role role : userInfo.getRoles()) {
        if (model.getBean().getName().equals(role.getName())) {
          model.put("selector", true);
        }
      }
    }
    dtRoles.update();
  }

  private void save() {
    // update of existing user
    if (!taUsers.isEnabled()) {
      userInfo.setRoles(getSelectedRoles(userInfo));
      userRoleServlet.saveUser(userInfo, new BaseAsyncCallback<UserInfo>() {
        @Override
        public void onSuccess(UserInfo result) {
          PortletEventManager.fireEvent(new GenericEvent<Void>(CuCoEventType.UPDATE_USERS));
          popupFrame.showInfoMessage(userInfo.getUsername() + " gespeichert", true, false);
        }

        @Override
        public void onFailure(Throwable exception) {
          popupFrame.showWarningMessage("Es ist ein Fehler beim Speichern aufgetreten.", false, true);
        }
      });
    } else {
      // new Users
      final String[] userArray = taUsers.getText().split(";");
      if (userArray.length > 1) {
        ArrayList<UserInfo> users = new ArrayList<UserInfo>();
        for (String account : userArray) {
          users.add(createUserInfo(account.trim()));
        }
        userRoleServlet.saveUsers(users, new BaseAsyncCallback<RpcStatus>() {
          @Override
          public void onSuccess(RpcStatus result) {
            PortletEventManager.fireEvent(new GenericEvent<Void>(CuCoEventType.UPDATE_USERS));
            popupFrame.showInfoMessage(userArray.length + " Benutzer gespeichert", true, false);
          }

          @Override
          public void onFailure(Throwable exception) {
            popupFrame.showWarningMessage("Es ist ein Fehler beim Speichern aufgetreten. Kontrollieren Sie bitte den CorporateAccount.", false, true);
          }
        });
      } else {
        userRoleServlet.saveUser(createUserInfo(taUsers.getText().trim()), new BaseAsyncCallback<UserInfo>() {
          @Override
          public void onSuccess(UserInfo result) {
            PortletEventManager.fireEvent(new GenericEvent<Void>(CuCoEventType.UPDATE_USERS));
            popupFrame.showInfoMessage(result.getUsername() + " gespeichert", true, false);
          }

          @Override
          public void onFailure(Throwable exception) {
            popupFrame.showWarningMessage("Es ist ein Fehler beim Speichern aufgetreten. Kontrollieren Sie bitte den CorporateAccount.", false, true);
          }
        });
      }
    }
  }

  private UserInfo createUserInfo(String account) {
    UserInfo userInfo = new UserInfo();
    userInfo.getBiteUser().setUsername(account);
    userInfo.setRoles(getSelectedRoles(userInfo));
    return userInfo;
  }

  private ArrayList<Role> getSelectedRoles(UserInfo userInfo) {
    ArrayList<Role> roles = new ArrayList<Role>();
    for (ModelData<Role> model : dtRoles.getStore().getAll()) {
      if ((Boolean) model.get("selector")) {
        roles.add(model.getBean());
      }
    }
    return roles;
  }

  private void loadUser() {
    if (taUsers.getText().split(";").length == 1) {
      userRoleServlet.getUserWithRoles(taUsers.getText(), new BaseAsyncCallback<UserInfo>() {
        @Override
        public void onSuccess(UserInfo result) {
          userInfo = result;
          deselectAllRoles();
          if (result != null) {
            selectRoles();
          }
        }

        @Override
        public void onFailure(Throwable exception) {
          // Do Nothing.
        }
      });
    }
  }

  public void show(UserInfo user) {
    deselectAllRoles();
    if (user == null) {
      lHeader.setText("Neue(n) Benutzer anlegen");
      taUsers.clear();
      dtRoles.update();
      taUsers.setEnabled(true);
    } else {
      userInfo = user;
      lHeader.setText("Benutzer bearbeiten");
      taUsers.setText(user.getUsername());
      taUsers.setEnabled(false);
      selectRoles();
    }
    popupFrame.hideMessageBar();
    popupFrame.showContent();
  }

  private void deselectAllRoles() {
    for (ModelData<Role> model : dtRoles.getStore().getAll()) {
      model.put("selector", false);
    }
  }

  public void hide() {
    popupFrame.hide();
  }
}
