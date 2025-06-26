package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.logical.shared.ValueChangeEvent;
import com.google.gwt.event.logical.shared.ValueChangeHandler;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.core.shared.dto.security.Authority;
import at.a1ta.bite.core.shared.dto.security.RoleGroup;
import at.a1ta.bite.core.shared.dto.security.RoleWithGroup;
import at.a1ta.bite.ui.client.Delegate;
import at.a1ta.bite.ui.client.PopupFrame;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.CheckBox;
import at.a1ta.bite.ui.client.widget.ClickableIcon;
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.InputBox.InputBoxSize;
import at.a1ta.bite.ui.client.widget.Label;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.framework.ui.client.ui.dialog.DialogPanel;
import at.a1ta.framework.ui.client.util.Validator;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class EditRoleGroupManagementDialog extends Composite {

  // @formatter:off
  private static EditRoleGroupManagementDialogUiBinder uiBinder = GWT.create(EditRoleGroupManagementDialogUiBinder.class);

  private static Logger logger = Logger.getLogger(EditRoleGroupManagementDialog.class.getName());

  interface EditRoleGroupManagementDialogUiBinder extends UiBinder<Widget, EditRoleGroupManagementDialog> {}

  @UiField(provided = true)
  DataTable<RoleWithGroup> dtRoles;
  @UiField(provided = true)
  DataTable<Authority> dtAuth;
  @UiField
  Label lHeader;
  @UiField
  Label lRoleHeader;
  @UiField
  Label lAuthHeader;
  @UiField
  InputBox name;
  @UiField
  InputBox description;
  @UiField
  Button bSave;
  @UiField
  Button bCancel;
  // @formatter:on

  private PopupFrame popupFrame;

  private UserInfo userInfo;
  private RoleGroup rg;
  private RoleWithGroup roleWithGroup;

  private Delegate<RoleWithGroup> editValueRoleGroupDelegate;

  protected int singleRoleSelected = 0;

  private Delegate<RoleWithGroup> saveValueRoleGroupDelegate;

  protected RoleWithGroup rolegroupForValueChange;

  private InputBox ib = new InputBox();

  Button b = new Button("Speichern", Button.ButtonSize.Small);
  final DialogPanel dialog = new DialogPanel();

  public EditRoleGroupManagementDialog() {
    createTable();
    initWidget(uiBinder.createAndBindUi(this));

    popupFrame = new PopupFrame(this, 1200, 600);
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
    });

    loadRoles(null);
  }

  private void createTable() {
    ArrayList<Column<RoleWithGroup>> columns = new ArrayList<Column<RoleWithGroup>>();
    ArrayList<Column<Authority>> column = new ArrayList<Column<Authority>>();
    columns.add(createSelectorColumn());
    columns.add(new Column<RoleWithGroup>("name", "Bezeichnung", "35%"));
    columns.add(new Column<RoleWithGroup>("desc", "Beschreibung", "35%"));
    columns.add(new Column<RoleWithGroup>("app", "Anwendung", "20%"));
    columns.add(new Column<RoleWithGroup>("value", "Wert", "10%", createWertCellRenderer()));

    column.add(createAuthSelectorColumn());
    column.add(new Column<Authority>("authName", "Bezeichnung", "50%"));
    column.add(new Column<Authority>("authDesc", "Beschreibung", "50%"));

    dtRoles = new DataTable<RoleWithGroup>(columns);
    dtAuth = new DataTable<Authority>(column);
    dtRoles.setHeight(450);
    dtAuth.setHeight(450);

    dialog.setCaption("Wert");
    dialog.setSize(200, 100);
    ib.setEnabled(true);
    ib.focus();
    ib.setInputBoxSize(InputBoxSize.Medium);
    ib.setRegExValidation("^[0-9]+$");
    ib.setValidationErrorMessage("Geben Sie nur einen numerischen Wert ein");
    dialog.add(ib);
    dialog.add(b);
    b.addClickHandler(new ClickHandler() {

      @Override
      public void onClick(ClickEvent event) {
        saveValueRoleGroupDelegate.execute(rolegroupForValueChange);

      }
    });

    saveValueRoleGroupDelegate = new Delegate<RoleWithGroup>() {
      @Override
      public void execute(final RoleWithGroup rg) {
        rg.setValue(Integer.valueOf(ib.getValue()));
        dialog.hide();
      }
    };
    editValueRoleGroupDelegate = new Delegate<RoleWithGroup>() {
      @Override
      public void execute(final RoleWithGroup rg) {
        ib.setValue(rg.getValue() != null ? String.valueOf(rg.getValue()) : "");
        rolegroupForValueChange = rg;
        dialog.show();
        dialog.center();
        ib.focus();
      }
    };
  }

  public Column<RoleWithGroup> createSelectorColumn() {
    return new Column<RoleWithGroup>("selector", "", "50px", new CellRenderer<RoleWithGroup>() {
      @Override
      public IsWidget render(final ModelData<RoleWithGroup> model, String columnId, int rowId) {
        final CheckBox cb = new CheckBox();
        cb.setValue((Boolean) model.get("selector"));
        cb.addValueChangeHandler(new ValueChangeHandler<Boolean>() {
          @Override
          public void onValueChange(ValueChangeEvent<Boolean> event) {
            model.put("selector", cb.getValue());
            if (rg != null) {
              if (rg.getRoles() == null) {
                rg.setRoles(new ArrayList<RoleWithGroup>());
              }
              if (cb.getValue()) {
                rg.getRoles().add(model.getBean());
                if (rg.getRoles().size() == 1) {
                  dtAuth.setVisible(true);
                  showAuth(model.getBean());
                } else {
                  dtAuth.setVisible(false);
                }

              } else {
                rg.getRoles().remove(model.getBean());
                dtAuth.setVisible(rg.getRoles().size() == 1);
                if (rg.getRoles().size() == 1) {
                  showAuth(rg.getRoles().get(0));
                }
              }
            }
          }
        });
        return cb;
      }
    }, false, false);
  }

  private CellRenderer<RoleWithGroup> createWertCellRenderer() {
    return new CellRenderer<RoleWithGroup>() {
      @Override
      public IsWidget render(final ModelData<RoleWithGroup> model, String columnId, int rowId) {
        return new ClickableIcon<RoleWithGroup>(model.getBean(), editValueRoleGroupDelegate, UI.IMAGES.iconEdit(), null);
      }
    };
  }

  private Column<Authority> createAuthSelectorColumn() {
    return new Column<Authority>("authSelector", "", "20px", new CellRenderer<Authority>() {
      @Override
      public IsWidget render(final ModelData<Authority> model, String columnId, int rowId) {
        final CheckBox cb = new CheckBox();
        cb.setValue((Boolean) model.get("authSelector"));
        cb.addValueChangeHandler(new ValueChangeHandler<Boolean>() {
          @Override
          public void onValueChange(ValueChangeEvent<Boolean> event) {
            model.put("authSelector", cb.getValue());
            if (roleWithGroup != null) {
              if (rg.getRoles() == null) {
                roleWithGroup.setAuthorities(new ArrayList<Authority>());
              }
              if (cb.getValue()) {
                roleWithGroup.getAuthorities().add(model.getBean());
              } else {
                roleWithGroup.getAuthorities().remove(model.getBean());
              }
            }
          }
        });
        return cb;
      }
    }, false, false);
  }

  private void loadRoles(final RoleGroup rg) {

    CommonServiceLocator.getRoleServlet().getAllRolesWithGroup((rg == null) ? null : rg.getId(), new BaseAsyncCallback<ArrayList<RoleWithGroup>>() {

      @Override
      public void onSuccess(final ArrayList<RoleWithGroup> result) {
        ArrayList<ModelData<RoleWithGroup>> roles = new ArrayList<ModelData<RoleWithGroup>>();
        dtRoles.getStore().clear();
        for (RoleWithGroup role : result) {
          ModelData<RoleWithGroup> model = new ModelData<RoleWithGroup>(role);
          model.put("selector", false);
          model.put("name", role.getName());
          model.put("desc", role.getDescription());
          model.put("value", role.getValue());
          roles.add(model);

        }

        dtRoles.getStore().add(roles);
        dtRoles.sort("name", true);
        if (rg != null) {
          lHeader.setText("Rollengruppe bearbeiten:");
          name.setText(rg.getName());
          description.setText(rg.getDescription());
          name.setEnabled(false);
          description.setEnabled(false);
          selectRoles();
          popupFrame.hideMessageBar();
          popupFrame.showContent();
        } else {
          loadAuth();
        }
      }
    });
  }

  private void loadAuth() {
    SettingsServiceLocator.getAuthorityServlet().getAllAuthorities(new BaseAsyncCallback<ArrayList<Authority>>() {

      @Override
      public void onSuccess(final ArrayList<Authority> result) {
        ArrayList<ModelData<Authority>> auths = new ArrayList<ModelData<Authority>>();
        for (Authority auth : result) {
          ModelData<Authority> model = new ModelData<Authority>(auth);
          model.put("authSelector", false);
          model.put("authName", auth.getName());
          model.put("authDesc", auth.getDescription());
          auths.add(model);
        }
        dtAuth.getStore().add(auths);
        dtAuth.sort("authName", true);
        selectRoles();
      }

      @Override
      public void onFailure(Throwable caught) {
        logger.log(Level.SEVERE, "Failure while loading auths", caught);

      }
    });
  }

  private void selectRoles() {
    if (rg != null) {
      for (ModelData<RoleWithGroup> model : dtRoles.getStore().getAll()) {
        for (RoleWithGroup roleGroup : rg.getRoles()) {
          if (model.getBean().getName().equals(roleGroup.getName())) {
            model.put("selector", true);
          }
        }
      }
      dtRoles.update();
      dtAuth.setVisible(rg.getRoles().size() == 1);
    }
  }

  private void selectAuth() {
    for (ModelData<Authority> model : dtAuth.getStore().getAll()) {
      for (Authority auth : roleWithGroup.getAuthorities()) {
        if (model.getBean().getName().equals(auth.getName())) {
          model.put("authSelector", true);
        }
      }
    }
    dtAuth.update();
  }

  private void save() {

    if (Validator.isNullOrEmpty(name.getValue())) {
      Window.alert("Rollenname darf nicht leer sein");
      return;
    }

    if (rg == null) {
      rg = new RoleGroup();
    }
    rg.setName(name.getValue());
    rg.setDescription(description.getValue());

    List<RoleWithGroup> roles = new ArrayList<RoleWithGroup>();
    boolean authUpdatedForFirstRole = false;
    for (ModelData<RoleWithGroup> model : dtRoles.getStore().getAll()) {
      if ((Boolean) model.get("selector")) {
        RoleWithGroup help = model.getBean();
        help.setValue(model.getBean().getValue());
        if (!authUpdatedForFirstRole) {
          // if multiple roles are selected, it will update auths only for first role and remaining should be untouched.
          populateSelectedAuthoritiesForRole(help);
          authUpdatedForFirstRole = true;
        }
        roles.add(help);
      }
    }
    rg.setRoles(roles);

    for (RoleWithGroup r : roles) {
      if (r.getValue() == null) {
        Window.alert("Die Werte aller ausgewählten Rollen müssen ausgefüllt werden!");
        return;
      }
    }

    CommonServiceLocator.getRoleServlet().saveRoleGroup(rg, new AsyncCallback<RoleGroup>() {

      @Override
      public void onSuccess(RoleGroup result) {
        PortletEventManager.fireEvent(new GenericEvent<RoleGroup>(CuCoEventType.UPDATE_ROLEGROUP, result));
      }

      @Override
      public void onFailure(Throwable caught) {
        logger.log(Level.SEVERE, "Fehler beim Speichern einer RoleGroup", caught);
      }
    });

    cancel();
  }

  private void populateSelectedAuthoritiesForRole(RoleWithGroup help) {
    List<Authority> authorities = new ArrayList<Authority>();
    for (ModelData<Authority> model1 : dtAuth.getStore().getAll()) {
      if ((Boolean) model1.get("authSelector")) {
        authorities.add(model1.getBean());
      }
    }
    help.setAuthorities(authorities);
  }

  private void cancel() {
    popupFrame.close();

  }

  private UserInfo createRoleGroup(String name) {
    RoleGroup rg = new RoleGroup();
    rg.setName(name);
    rg.setRoles(getSelectedRoles(rg));
    return userInfo;
  }

  private List<RoleWithGroup> getSelectedRoles(RoleGroup rg) {
    List<RoleWithGroup> roles = new ArrayList<RoleWithGroup>();
    for (ModelData<RoleWithGroup> model : dtRoles.getStore().getAll()) {
      if ((Boolean) model.get("selector")) {
        roles.add(model.getBean());
      }
    }
    return roles;
  }

  public void show(RoleGroup group) {
    deselectAllRoles();
    if (group == null) {
      rg = new RoleGroup();
      lHeader.setText("Neue Rollengruppe:");
      name.clear();
      description.clear();
      dtRoles.update();
      name.setEnabled(true);
      description.setEnabled(true);
      popupFrame.hideMessageBar();
      popupFrame.showContent();
    } else {
      rg = group;
      loadRoles(rg);

    }

  }

  public void showAuth(RoleWithGroup rwg) {
    deselectAllAuth();
    if (rwg == null) {
      roleWithGroup = new RoleWithGroup();
      dtAuth.update();
    } else {
      roleWithGroup = rwg;
      selectAuth();
    }
    popupFrame.hideMessageBar();
    popupFrame.showContent();
  }

  private void deselectAllRoles() {
    for (ModelData<RoleWithGroup> model : dtRoles.getStore().getAll()) {
      model.put("selector", false);

    }
  }

  private void deselectAllAuth() {
    for (ModelData<Authority> model : dtAuth.getStore().getAll()) {
      model.put("authSelector", false);
    }
  }

  public void hide() {
    popupFrame.hide();
  }

}
