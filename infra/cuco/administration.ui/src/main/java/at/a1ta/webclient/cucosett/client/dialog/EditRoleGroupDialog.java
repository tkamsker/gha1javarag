package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.extjs.gxt.ui.client.Style.SelectionMode;
import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.event.GridEvent;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.Text;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.grid.CellEditor;
import com.extjs.gxt.ui.client.widget.grid.CheckBoxSelectionModel;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.google.gwt.i18n.client.NumberFormat;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.FlexTable;

import at.a1ta.bite.core.shared.dto.security.RoleGroup;
import at.a1ta.bite.core.shared.dto.security.RoleWithGroup;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.framework.gxt.ui.GridContainer;
import at.a1ta.framework.gxt.ui.NumberFieldFixed;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.framework.ui.client.util.Validator;

public class EditRoleGroupDialog extends Dialog {

  private static Logger logger = Logger.getLogger(EditRoleGroupDialog.class.getName());

  private TextField<String> nameField = new TextField<String>();

  private TextField<String> descriptionField = new TextField<String>();

  private GridContainer<ListStore<BaseModelData>, BaseModelData> gridContainer;

  private CheckBoxSelectionModel<BaseModelData> roleSM = null;

  private RoleGroup rg;

  public EditRoleGroupDialog(String header, RoleGroup rg) {
    this.rg = rg;

    setModal(true);
    setHeading(header);
    okText = "Speichern";
    cancelText = "Abbrechen";
    setButtons(OKCANCEL);

    setClosable(true);
    setLayoutOnChange(true);
    setBodyBorder(false);
    setBorders(false);
    setHideOnButtonClick(false);
    setWidth(600);
    setHeight(600);

    FlexTable table = new FlexTable();
    table.setWidget(0, 0, new Text("Bezeichnung"));
    table.setWidget(0, 1, nameField);
    table.setWidget(1, 0, new Text("Beschreibung"));
    table.setWidget(1, 1, descriptionField);

    if (rg != null) {
      nameField.setValue(rg.getName());
      descriptionField.setValue(rg.getDescription());
    }

    add(table);
    initRolePanel();

    loadRoles();
  }

  private void loadRoles() {
    CommonServiceLocator.getRoleServlet().getAllRolesWithGroup((rg == null) ? null : rg.getId(), new BaseAsyncCallback<ArrayList<RoleWithGroup>>() {

      @Override
      public void onSuccess(final ArrayList<RoleWithGroup> result) {
        ArrayList<BaseModelData> roles = new ArrayList<BaseModelData>();
        ArrayList<BaseModelData> selection = new ArrayList<BaseModelData>();

        for (RoleWithGroup role : result) {
          BaseModelData help = new BaseModelData();
          help.set("bean", role);
          help.set("name", role.getName());
          help.set("desc", role.getDescription());
          help.set("value", role.getValue());
          roles.add(help);
          if (rg != null) {
            if (role.getValue() != null && role.getGroupId().equals(rg.getId())) {
              selection.add(help);
            }
          }
        }

        gridContainer.getGrid().getStore().removeAll();
        gridContainer.getGrid().getStore().add(roles);
        gridContainer.getGrid().getSelectionModel().setSelection(selection);
      }
    });
  }

  @Override
  protected void onButtonPressed(final Button button) {
    if (button == getButtonById(OK)) {
      if (Validator.isNullOrEmpty(nameField.getValue())) {
        Window.alert("Rollenname darf nicht leer sein");
        return;
      }

      if (rg == null) {
        rg = new RoleGroup();
      }
      rg.setName(nameField.getValue());
      rg.setDescription(descriptionField.getValue());

      List<RoleWithGroup> roles = new ArrayList<RoleWithGroup>();
      for (BaseModelData bm : gridContainer.getGrid().getSelectionModel().getSelectedItems()) {
        RoleWithGroup help = (RoleWithGroup) bm.get("bean");
        help.setValue((Integer) bm.get("value"));
        roles.add(help);

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
          hide(button);
        }

        @Override
        public void onFailure(Throwable caught) {
          logger.log(Level.SEVERE, "Fehler beim Speichern einer RoleGroup", caught);
        }
      });
    } else {
      hide(button);
    }
  }

  private void initRolePanel() {

    roleSM = new CheckBoxSelectionModel<BaseModelData>() {

      @Override
      protected void doMultiSelect(List<BaseModelData> models, boolean keepExisting, boolean supressEvent) {
        if (models.size() == grid.getStore().getCount()) {
          super.doMultiSelect(models, keepExisting, supressEvent);
        } else {
          super.doMultiSelect(models, true, supressEvent);
        }
      }

      @Override
      protected void handleMouseDown(GridEvent<BaseModelData> e) {
        BaseModelData selected = listStore.getAt(e.getRowIndex());
        if (grid.getColumnModel().getColumn(e.getColIndex()).getId().equals("value")) {
          return;
        }
        boolean issel = isSelected(selected);
        super.handleMouseDown(e);
        if (issel) {
          doDeselect(Arrays.asList(selected), false);
        }
      }
    };

    roleSM.setSelectionMode(SelectionMode.MULTI);

    gridContainer = new GridContainer<ListStore<BaseModelData>, BaseModelData>(new ListStore<BaseModelData>(), createRoleColumnModel(), 475, true);
    gridContainer.setHeading("Rollen");
    gridContainer.setHeaderVisible(true);

    gridContainer.getGrid().setSelectionModel(roleSM);
    gridContainer.getGrid().addPlugin(roleSM);
    gridContainer.getGrid().setAutoExpandColumn("desc");

    gridContainer.setWidth(580);
    add(gridContainer);
  }

  private ColumnModel createRoleColumnModel() {
    List<ColumnConfig> columns = new ArrayList<ColumnConfig>();
    columns.add(roleSM.getColumn());

    ColumnConfig nameColumn = new ColumnConfig("name", "Bezeichnung", 150);
    columns.add(nameColumn);

    ColumnConfig descColumn = new ColumnConfig("desc", "Beschreibung", 200);
    columns.add(descColumn);

    ColumnConfig appColumn = new ColumnConfig("app", "Anwendung", 75);
    columns.add(appColumn);

    ColumnConfig valueCol = new ColumnConfig("value", "Wert", 50);
    valueCol.setNumberFormat(NumberFormat.getFormat("#"));
    NumberFieldFixed numberField = new NumberFieldFixed();
    numberField.setAllowBlank(false);
    valueCol.setEditor(new CellEditor(numberField) {

      @Override
      public Object postProcessValue(Object value) {
        return new Integer(((Double) super.postProcessValue(value)).intValue());
      }
    });
    columns.add(valueCol);

    return new ColumnModel(columns);
  }

}
