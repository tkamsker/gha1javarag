package at.a1ta.webclient.cucosett.client.dialog;

import java.util.ArrayList;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.ui.client.PopupFrame;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.WaitingWidget;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.GwtAddTeamMembersEvent;
import at.a1ta.cuco.ui.common.client.ui.ClickListener;
import at.a1ta.cuco.ui.common.client.ui.DoubleClickListener;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.framework.ui.client.util.Validator;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class GwtSelectTeamMemberDialog extends Composite {

  private static GwtSelectTeamMemberDialogUiBinder uiBinder = GWT.create(GwtSelectTeamMemberDialogUiBinder.class);

  interface GwtSelectTeamMemberDialogUiBinder extends UiBinder<Widget, GwtSelectTeamMemberDialog> {}

  private static GwtSelectTeamMemberDialog _instance = null;

  @UiField(provided = true)
  DataTable<BiteUser> table;
  @UiField
  InputBox surName;
  @UiField
  InputBox ntAccount;
  @UiField
  InputBox oe;
  @UiField
  Button add;
  @UiField
  Button remove;
  @UiField
  Button bSave;
  @UiField
  Button bCancel;

  @UiField
  Button bSearch;
  @UiField(provided = true)
  DataTable<BiteUser> table2;

  private ModelData<BiteUser> modeldata;
  private PopupFrame popupFrame;
  private WaitingWidget waitingWidget;

  public static GwtSelectTeamMemberDialog getInstance() {
    if (_instance == null) {
      _instance = new GwtSelectTeamMemberDialog();
    }
    return _instance;
  }

  public GwtSelectTeamMemberDialog() {
    initTable();
    initWidget(uiBinder.createAndBindUi(this));
    renderSelectionGrid();
    renderTeamGrid();
    renderMoveButtons();
    surName.setCaption(AdminUI.ADMINCOMMONTEXTPOOL.teamName());
    ntAccount.setCaption(AdminUI.ADMINCOMMONTEXTPOOL.teamNtAccount());
    oe.setCaption(AdminUI.ADMINCOMMONTEXTPOOL.teamOe());
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
    bSearch.addClickHandler(new ClickHandler() {

      @Override
      public void onClick(ClickEvent event) {
        if (Validator.isNullOrEmpty(oe.getText()) && Validator.isNullOrEmpty(surName.getText()) && Validator.isNullOrEmpty(ntAccount.getText())) {
          return;
        }

        search();
      }

    });

    popupFrame = new PopupFrame(this, 600, 570);
  }

  public void search() {
    table.getStore().clear();

    String name = Validator.isNullOrEmpty(surName.getText()) ? null : ('%' + surName.getText().toLowerCase() + '%');
    String account = Validator.isNullOrEmpty(ntAccount.getText()) ? null : ('%' + ntAccount.getText().toLowerCase() + '%');
    String oE = Validator.isNullOrEmpty(oe.getText()) ? null : '%' + oe.getText().toLowerCase() + '%';
    SettingsServiceLocator.getTeamServlet().searchUsers(name, account, oE, new BaseAsyncCallback<ArrayList<BiteUser>>() {

      @Override
      public void onFailure(Throwable exception) {
        super.onFailure(exception);
      }

      @Override
      public void onSuccess(ArrayList<BiteUser> result) {
        ArrayList<ModelData<BiteUser>> results = new ArrayList<ModelData<BiteUser>>();
        for (BiteUser user : result) {
          ModelData<BiteUser> model = new ModelData<BiteUser>(user);
          model.put("bean", user);
          model.put("name", user.getName());
          model.put("user", user.getUsername());
          model.put("orgunit", user.getManagementLevel1OrgUnitShort());
          results.add(model);
        }
        table.getStore().add(results);
        table.setVisible(true);
      }
    });
  }

  private void initTable() {
    waitingWidget = new WaitingWidget();
    table = new DataTable<BiteUser>(createColumns());
    table.enablePaging(10);
    table.setWidth("550px");
    table.setVisible(true);
    table2 = new DataTable<BiteUser>(createColumns());
    table2.enablePaging(10);
    table2.setWidth("550px");
    table2.setHeight("200");
    table2.setVisible(true);
  }

  private ArrayList<Column<BiteUser>> createColumns() {
    ArrayList<Column<BiteUser>> columns = new ArrayList<Column<BiteUser>>();
    columns.add(new Column<BiteUser>("name", AdminUI.ADMINCOMMONTEXTPOOL.teamName(), "40%"));
    columns.add(new Column<BiteUser>("user", AdminUI.ADMINCOMMONTEXTPOOL.teamNtAccount(), "40%"));
    columns.add(new Column<BiteUser>("orgunit", AdminUI.ADMINCOMMONTEXTPOOL.teamOe(), "20%"));

    return columns;
  }

  public void renderSelectionGrid() {
    table.addClickListener(new ClickListener<BiteUser>() {

      @Override
      public void onClick(ModelData<BiteUser> data) {
        if (data != null) {
          modeldata = data;
          add.enable();
        } else {
          add.disable();
        }
      }
    });

    table.addDoubleClickListener(new DoubleClickListener<BiteUser>() {

      @Override
      public void onDoubleClick(ModelData<BiteUser> data) {
        add.disable();
        table2.getStore().add(data);
        ArrayList<ModelData<BiteUser>> changed = new ArrayList<ModelData<BiteUser>>();
        changed.addAll(table.getStore().getAll());
        table.getStore().clear();
        changed.remove(data);
        table.getStore().add(changed);
        table2.setVisible(true);
      }
    });
  }

  public void renderTeamGrid() {
    table2.addClickListener(new ClickListener<BiteUser>() {
      @Override
      public void onClick(ModelData<BiteUser> data) {

        if (data != null) {
          modeldata = data;
          remove.enable();
        } else {
          remove.disable();
        }
      }
    });

    table2.addDoubleClickListener(new DoubleClickListener<BiteUser>() {

      @Override
      public void onDoubleClick(ModelData<BiteUser> data) {

        remove.disable();
        ArrayList<ModelData<BiteUser>> changed = new ArrayList<ModelData<BiteUser>>();
        changed.addAll(table2.getStore().getAll());
        table2.getStore().clear();
        changed.remove(data);
        table2.getStore().add(changed);
      }
    });
  }

  public void init() {
    waitingWidget.setVisible(true);
    table.setVisible(false);
    table.getStore().clear();
    table2.getStore().clear();
    surName.clear();
    oe.clear();
    ntAccount.clear();
    SettingsServiceLocator.getTeamServlet().getAllUsers(new BaseAsyncCallback<ArrayList<BiteUser>>() {

      @Override
      public void onSuccess(ArrayList<BiteUser> result) {
        ArrayList<ModelData<BiteUser>> results = new ArrayList<ModelData<BiteUser>>();
        for (BiteUser user : result) {
          ModelData<BiteUser> model = new ModelData<BiteUser>(user);
          model.put("bean", user);
          model.put("name", user.getName());
          model.put("user", user.getUsername());
          model.put("orgunit", user.getManagementLevel1OrgUnitShort());
          results.add(model);
        }
        table.getStore().add(results);
        waitingWidget.setVisible(false);
        table.setVisible(true);
      }

      @Override
      public void onFailure(Throwable exception) {
        super.onFailure(exception);
        waitingWidget.setVisible(false);
      }
    });
  }

  public void show() {
    popupFrame.hideMessageBar();
    popupFrame.showContent();
  }

  public void renderMoveButtons() {

    add.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        if (modeldata == null) {
          return;
        }
        table2.getStore().add(modeldata);
        table2.update();
        modeldata = null;
        add.disable();
      }
    });
    add.disable();
    remove.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        if (modeldata == null) {
          return;
        }
        ArrayList<ModelData<BiteUser>> changed = new ArrayList<ModelData<BiteUser>>();
        changed.addAll(table2.getStore().getAll());
        table2.getStore().clear();
        changed.remove(modeldata);
        table2.getStore().add(changed);
        remove.disable();
      }
    });
    remove.disable();
  }

  public void save() {
    try {
      PortletEventManager.fireEvent(new GwtAddTeamMembersEvent(table2.getStore().getAll()));
    } catch (Exception e) {
      popupFrame.close();
    }

  }

}
