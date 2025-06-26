package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.extjs.gxt.ui.client.Style.SelectionMode;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.CheckBoxSelectionModel;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.google.gwt.core.client.Scheduler;
import com.google.gwt.core.client.Scheduler.ScheduledCommand;

import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.cuco.admin.ui.common.client.event.SelectRolesEvent;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.framework.gxt.ui.GridContainer;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.PortletEventManager;

public class SelectRolesDialog extends Dialog {

  private GridContainer<ListStore<BaseModelData>, BaseModelData> gridContainer;

  private CheckBoxSelectionModel<BaseModelData> roleSM = null;

  private Long appId;

  private List<Role> preSelection;

  public SelectRolesDialog(String header, List<Role> preselection) {
    this.preSelection = preselection;

    setModal(true);
    setHeading(header);
    okText = "Speichern";
    cancelText = "Abbrechen";
    setButtons(OKCANCEL);

    setClosable(false);
    setLayoutOnChange(true);
    setBodyBorder(false);
    setBorders(false);
    setHideOnButtonClick(false);
    setHeight(600);
    setWidth(500);

    initRoles();
  }

  private void initRoles() {
    roleSM = new CheckBoxSelectionModel<BaseModelData>() {

      @Override
      protected void doMultiSelect(java.util.List<BaseModelData> models, boolean keepExisting, boolean supressEvent) {
        if (models.size() == grid.getStore().getModels().size()) {
          super.doMultiSelect(models, keepExisting, supressEvent);
        } else {
          super.doMultiSelect(models, true, supressEvent);
        }
      }

      @Override
      protected void handleMouseDown(com.extjs.gxt.ui.client.event.GridEvent<BaseModelData> e) {
        BaseModelData sel = listStore.getAt(e.getRowIndex());
        boolean issel = isSelected(sel);
        super.handleMouseDown(e);
        if (issel) {
          doDeselect(Arrays.asList(sel), false);
        }
      }
    };
    roleSM.setSelectionMode(SelectionMode.MULTI);

    gridContainer = new GridContainer<ListStore<BaseModelData>, BaseModelData>(new ListStore<BaseModelData>(), createRoleColumnModel());
    gridContainer.setWidth(480);

    gridContainer.getGrid().setSelectionModel(roleSM);
    gridContainer.getGrid().addPlugin(roleSM);

    CommonServiceLocator.getRoleServlet().getAllRolesForSysMsg(UserManager.getUserInfo().getId(), new BaseAsyncCallback<ArrayList<Role>>() {

      @Override
      public void onSuccess(ArrayList<Role> result) {
        ArrayList<BaseModelData> roles = new ArrayList<BaseModelData>();

        for (Role role : result) {
          roles.add(createRoleModel(role));
        }
        gridContainer.getGrid().getStore().add(roles);

        Scheduler.get().scheduleDeferred(new ScheduledCommand() {

          @Override
          public void execute() {
            gridContainer.getGrid().getSelectionModel().deselectAll();
            List<BaseModelData> roles = new ArrayList<BaseModelData>();
            for (Role role : preSelection) {
              roles.add(createRoleModel(role));
            }
            gridContainer.getGrid().getSelectionModel().setSelection(roles);
          }
        });
      }

    });
    add(gridContainer);
  }

  private BaseModelData createRoleModel(Role role) {
    BaseModelData model = new BaseModelData() {

      // needed for selection model of grid/store
      @Override
      public boolean equals(Object obj) {
        if (!(obj instanceof BaseModelData)) {
          return false;
        }
        Object name = get("name");
        Object other = ((BaseModelData) obj).get("name");
        return name != null ? name.equals(other) : other == null;
      }

      @Override
      public int hashCode() {
        Object name = get("name");
        return name != null ? name.hashCode() : super.hashCode();
      }
    };
    model.set("bean", role);
    model.set("name", role.getName());
    model.set("desc", role.getDescription());

    return model;
  }

  private ColumnModel createRoleColumnModel() {
    List<ColumnConfig> columns = new ArrayList<ColumnConfig>();
    columns.add(roleSM.getColumn());
    columns.add(new ColumnConfig("name", "Bezeichnung", 200));
    columns.add(new ColumnConfig("desc", "Beschreibung", 200));

    return new ColumnModel(columns);
  }

  @Override
  protected void onButtonPressed(Button button) {
    if (button == getButtonBar().getItemByItemId(OK)) {
      List<Role> roles = new ArrayList<Role>();
      for (BaseModelData bm : gridContainer.getGrid().getSelectionModel().getSelectedItems()) {
        roles.add((Role) bm.get("bean"));
      }
      PortletEventManager.fireEvent(new SelectRolesEvent(roles));
    }
    hide();
  }

}
