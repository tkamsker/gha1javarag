package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.logical.shared.ValueChangeEvent;
import com.google.gwt.event.logical.shared.ValueChangeHandler;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.bite.ui.client.PopupFrame;
import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.CheckBox;
import at.a1ta.cuco.admin.ui.common.client.event.SelectRolesEvent;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.PortletEventManager;

public class GwtSelectRolesDialog extends Composite {

  // @formatter:off
  private static EditUserDialogUiBinder uiBinder = GWT.create(EditUserDialogUiBinder.class);

  interface EditUserDialogUiBinder extends UiBinder<Widget, GwtSelectRolesDialog> {}

  @UiField(provided = true)
  DataTable<Role> dtRoles;
  @UiField
  Button bSave;
  @UiField
  Button bCancel;
  // @formatter:on

  private PopupFrame popupFrame;

  public GwtSelectRolesDialog() {
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
    bCancel.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        popupFrame.close();
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
          }
        });
        return cb;
      }
    }, false, false);
  }

  private void loadRoles() {
    CommonServiceLocator.getRoleServlet().getAllRolesForSysMsg(UserManager.getUserInfo().getId(), new BaseAsyncCallback<ArrayList<Role>>() {
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

      }
    });
  }

  private void save() {
    ArrayList<Role> roles = new ArrayList<Role>();
    for (ModelData<Role> model : dtRoles.getStore().getAll()) {
      if ((Boolean) model.get("selector")) {
        roles.add(model.getBean());
      }
    }
    PortletEventManager.fireEvent(new SelectRolesEvent(roles));
    popupFrame.close();
  }

  public void show() {
    popupFrame.hideMessageBar();
    popupFrame.showContent();
  }

  public void hide() {
    popupFrame.hide();
  }
}
