package at.a1ta.webclient.cucosett.client.portlet;

import java.util.ArrayList;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.Anchor;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.bite.core.shared.dto.security.RoleGroup;
import at.a1ta.bite.core.shared.dto.security.RoleWithGroup;
import at.a1ta.bite.ui.client.Delegate;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.bite.ui.client.widget.ClickableIcon;
import at.a1ta.bite.ui.client.widget.WaitingWidget;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.cuco.ui.common.shared.AdminAuthorityHelper;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.EditRoleGroupManagementDialog;

public class RoleGroupsManagementPortlet extends CuCoSettBasePortlet {

  public static final String NAME = "Rollengruppenverwaltung";
  private static RoleGroupsManagementPortlet _instance;
  private DataTable<RoleGroup> table;

  private WaitingWidget waitingWidget;
  private EditRoleGroupManagementDialog editRoleGroupDialog = new EditRoleGroupManagementDialog();
  private Delegate<RoleGroup> deleteRoleGroupDelegate;

  public static RoleGroupsManagementPortlet create(PortletDefinition portletDefinition) {
    if (_instance == null) {
      _instance = new RoleGroupsManagementPortlet(portletDefinition, false);
    }
    return _instance;
  }

  private RoleGroupsManagementPortlet(PortletDefinition def, boolean isDetails) {
    super(def, isDetails, false, false);

    initTable();
    initUI();

    registerUpdateUserListener();
    registerUpdateUsersListener();

    loadUsers();

    showContent();
  }

  private void initUI() {
    waitingWidget = new WaitingWidget();
    HTMLPanel pnl = new HTMLPanel("");
    pnl.setStyleName(UI.STYLES.bite_moduleContent());
    HorizontalPanel newRoleGroup = createNewRoleGroupRow();
    pnl.add(newRoleGroup);
    pnl.add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    pnl.add(waitingWidget);
    pnl.add(table);
    add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    add(pnl);
    deleteRoleGroupDelegate = new Delegate<RoleGroup>() {

      @Override
      public void execute(final RoleGroup group) {
        CommonServiceLocator.getRoleServlet().deleteRoleGroup(group.getId(), new AsyncCallback<RpcStatus>() {

          @Override
          public void onSuccess(RpcStatus result) {
            ModelData<RoleGroup> m = new ModelData<RoleGroup>(group);
            m.remove(group);
            loadUsers();
          }

          @Override
          public void onFailure(Throwable caught) {
            showError();

          }
        });

      }
    };
  }

  private void initTable() {
    table = new DataTable<RoleGroup>(createColumns());
    table.enablePaging(25);
    table.setWidth("830px");
    table.setVisible(false);
  }

  private void registerUpdateUsersListener() {
    PortletEventManager.addListener(CuCoEventType.UPDATE_USERS, new PortletEventListener<PortletEvent>() {

      @Override
      public void handleEvent(PortletEvent be) {
        init();
        loadUsers();
      }
    });
  }

  protected void loadUsers() {
    waitingWidget.setVisible(true);
    table.setVisible(false);

    table.getStore().clear();

    CommonServiceLocator.getRoleServlet().getAllRoleGroups(new BaseAsyncCallback<ArrayList<RoleGroup>>(this) {

      @Override
      public void onSuccess(ArrayList<RoleGroup> result) {
        ArrayList<ModelData<RoleGroup>> results = new ArrayList<ModelData<RoleGroup>>();

        for (RoleGroup group : result) {
          ModelData<RoleGroup> m = new ModelData<RoleGroup>(group);
          m.put("bean", group);
          m.put("name", group.getName());
          m.put("desc", group.getDescription());
          results.add(m);
        }

        table.getStore().add(results);
        waitingWidget.setVisible(false);
        table.setVisible(true);
      }
    });
  }

  private void registerUpdateUserListener() {
    PortletEventManager.addListener(CuCoEventType.UPDATE_ROLEGROUP, new PortletEventListener<GenericEvent<RoleGroup>>() {

      @Override
      public void handleEvent(GenericEvent<RoleGroup> be) {
        RoleGroup group = be.get();
        ModelData<RoleGroup> model = table.getStore().get(group);
        if (model != null) {
          model.setBean(group);
        } else {
          model = new ModelData<RoleGroup>(group);
          model.put("bean", group);
          model.put("name", group.getName());
          model.put("desc", group.getDescription());
          table.getStore().add(model);
        }
        loadUsers();
      }
    });
  }

  private HorizontalPanel createNewRoleGroupRow() {
    HorizontalPanel roleGroup = new HorizontalPanel();
    if (AdminAuthorityHelper.canCreateRoleGroup(UserManager.getUserInfo())) {
      roleGroup.add(createNewButton());
    }
    return roleGroup;
  }

  private Widget createNewButton() {
    Button btnCreateRoleGroup = new Button("Neue Rollengruppe", ButtonSize.Small);
    btnCreateRoleGroup.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        editRoleGroupDialog = new EditRoleGroupManagementDialog();
        editRoleGroupDialog.show(null);
      }
    });
    return btnCreateRoleGroup;
  }

  private ArrayList<Column<RoleGroup>> createColumns() {
    ArrayList<Column<RoleGroup>> columns = new ArrayList<Column<RoleGroup>>();
    columns.add(new Column<RoleGroup>("name", "Bezeichnung", "15%", createRoleGroupCellRenderer()));
    columns.add(new Column<RoleGroup>("desc", "Beschreibung", "16%"));
    columns.add(new Column<RoleGroup>("delete", "Löschen", "16%", createDeleteCellRenderer()));
    return columns;
  }

  private CellRenderer<RoleGroup> createRoleGroupCellRenderer() {
    return new CellRenderer<RoleGroup>() {
      @Override
      public Widget render(final ModelData<RoleGroup> model, String columnId, int rowId) {
        Anchor link = new Anchor(model.getBean().getName());
        link.addClickHandler(new ClickHandler() {
          @Override
          public void onClick(ClickEvent event) {
            editRoleGroupDialog.show(model.getBean());
            if (model.getBean().getRoles().size() <= 1) {
              for (RoleWithGroup roleGroup : model.getBean().getRoles()) {
                editRoleGroupDialog.showAuth(roleGroup);
              }
            }
          }
        });
        return link;
      }
    };
  }

  private CellRenderer<RoleGroup> createDeleteCellRenderer() {
    return new CellRenderer<RoleGroup>() {
      @Override
      public IsWidget render(final ModelData<RoleGroup> model, String columnId, int rowId) {
        return new ClickableIcon<RoleGroup>(model.getBean(), deleteRoleGroupDelegate, UI.IMAGES.iconDelete(), null);
      }
    };
  }

  @Override
  public void init() {}
}