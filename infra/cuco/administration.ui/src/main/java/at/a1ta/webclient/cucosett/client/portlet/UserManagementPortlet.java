package at.a1ta.webclient.cucosett.client.portlet;

import java.util.ArrayList;
import java.util.HashMap;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.dom.client.KeyCodes;
import com.google.gwt.event.dom.client.KeyPressEvent;
import com.google.gwt.event.dom.client.KeyPressHandler;
import com.google.gwt.user.client.ui.Anchor;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.InputBox.InputBoxSize;
import at.a1ta.bite.ui.client.widget.Label;
import at.a1ta.bite.ui.client.widget.WaitingWidget;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.admin.ui.common.client.ui.PortletHelper;
import at.a1ta.cuco.ui.common.client.popup.PartnerCenterUserDetailsPopup;
import at.a1ta.cuco.ui.common.client.popup.PartnerCenterUserDetailsPopup.EditType;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.cuco.ui.common.shared.AdminAuthorityHelper;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.EditUserDialog;

public class UserManagementPortlet extends CuCoSettBasePortlet {

  public static final String NAME = "Benutzerverwaltung";
  private static UserManagementPortlet _instance;
  private DataTable<BiteUser> table;
  private HashMap<String, String> shopIDs;

  private InputBox userFilter;
  private InputBox firstNameFilter;
  private InputBox lastNameFilter;

  private WaitingWidget waitingWidget;
  private EditUserDialog editUserDialog = new EditUserDialog();

  private PartnerCenterUserDetailsPopup partnerCenterUserDetailsPopup = new PartnerCenterUserDetailsPopup();

  public static UserManagementPortlet create(PortletDefinition def) {
    if (_instance == null) {
      _instance = new UserManagementPortlet(def);
    }
    return _instance;
  }

  private UserManagementPortlet(PortletDefinition def) {
    super(def, false, false);

    initTable();
    initUI();

    registerUpdateUserListener();
    registerUpdateUsersListener();
    userFilter.setValue(UserManager.getUserInfo().getUsername());
    loadUsers();

    showContent();
  }

  private void initUI() {
    waitingWidget = new WaitingWidget();
    HTMLPanel pnl = new HTMLPanel("");
    pnl.setStyleName(UI.STYLES.bite_moduleContent());
    HorizontalPanel filters = createFilterRow();
    pnl.add(filters);
    pnl.add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    pnl.add(waitingWidget);
    pnl.add(table);
    add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));
    add(pnl);
  }

  private void initTable() {
    table = new DataTable<BiteUser>(createColumns());
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

  private HorizontalPanel createFilterRow() {
    HorizontalPanel filters = new HorizontalPanel();
    filters.add(new Label("Benutzer:"));
    filters.add(new HTML("<div class='" + UI.STYLES.bite_widthPlaceHolder() + "'/>"));
    filters.add(createUserFilter());
    filters.add(new HTML("<div class='" + UI.STYLES.bite_widthPlaceHolder() + "'/>"));
    filters.add(new Label("Vorname:"));
    filters.add(new HTML("<div class='" + UI.STYLES.bite_widthPlaceHolder() + "'/>"));
    filters.add(createFirstNameFilter());
    filters.add(new HTML("<div class='" + UI.STYLES.bite_widthPlaceHolder() + "'/>"));
    filters.add(new Label("Nachname:"));
    filters.add(new HTML("<div class='" + UI.STYLES.bite_widthPlaceHolder() + "'/>"));
    filters.add(createLastNameFilter());
    filters.add(new HTML("<div class='" + UI.STYLES.bite_widthPlaceHolder() + "'/>"));
    filters.add(createSearchButton());
    filters.add(createNewButton());
    return filters;
  }

  private Widget createUserFilter() {
    userFilter = new InputBox(InputBoxSize.Medium);
    userFilter.addKeyPressHandler(createKeyPressHandler());
    return userFilter;
  }

  private Widget createFirstNameFilter() {
    firstNameFilter = new InputBox(InputBoxSize.Medium);
    firstNameFilter.addKeyPressHandler(createKeyPressHandler());
    return firstNameFilter;
  }

  private Widget createLastNameFilter() {
    lastNameFilter = new InputBox(InputBoxSize.Medium);
    lastNameFilter.addKeyPressHandler(createKeyPressHandler());
    return lastNameFilter;
  }

  private KeyPressHandler createKeyPressHandler() {
    return new KeyPressHandler() {
      @Override
      public void onKeyPress(KeyPressEvent event) {
        if (event.getNativeEvent().getKeyCode() == KeyCodes.KEY_ENTER) {
          loadUsers();
        }
      }
    };
  }

  private void registerUpdateUserListener() {
    PortletEventManager.addListener(CuCoEventType.UPDATE_USER, new PortletEventListener<GenericEvent<BiteUser>>() {
      @Override
      public void handleEvent(GenericEvent<BiteUser> be) {
        BiteUser user = be.get();
        ModelData<BiteUser> model = table.getStore().get(user);

        if (model != null) {
          model.setBean(user);
        } else {
          model = new ModelData<BiteUser>(user);
          model.put("bean", user);
          model.put("name", user.getName());
          model.put("username", user.getUsername());
          model.put("orgunitshort", user.getManagementLevel1OrgUnitShort());
          model.put("orgunitDesc", user.getManagementLevel1OrgUnitDescription());
          model.put("edit", "Partner Center");
          table.getStore().add(model);
        }
      }
    });
  }

  private Widget createNewButton() {
    Button btnCreateUser = new Button("Neuer Benutzer", ButtonSize.Small);
    btnCreateUser.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        editUserDialog.show(null);
      }
    });
    return btnCreateUser;
  }

  private Widget createSearchButton() {
    Button btnSearch = new Button("Suchen", ButtonSize.Small);
    btnSearch.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        loadUsers();
      }
    });
    return btnSearch;
  }

  @Override
  public void init() {}

  private void loadUsers() {
    waitingWidget.setVisible(true);
    table.setVisible(false);

    table.getStore().clear();

    CommonServiceLocator.getUserShopAssignmentServlet().getUserShopAssignmentsForUserManagement(new BaseAsyncCallback<HashMap<String, String>>() {

      @Override
      public void onSuccess(HashMap<String, String> result) {
        shopIDs = result;
      }

      @Override
      public void onFailure(Throwable exception) {
        shopIDs = new HashMap<String, String>();
      }

    });

    CommonServiceLocator.getRoleServlet().searchUsers(userFilter.getValue(), firstNameFilter.getValue(), lastNameFilter.getValue(), new BaseAsyncCallback<ArrayList<BiteUser>>() {
      @Override
      public void onSuccess(ArrayList<BiteUser> result) {
        ArrayList<ModelData<BiteUser>> users = new ArrayList<ModelData<BiteUser>>();

        for (BiteUser user : result) {
          ModelData<BiteUser> m = new ModelData<BiteUser>(user);
          m.put("bean", user);
          m.put("firstName", user.getFirstName());
          m.put("lastName", user.getLastName());
          m.put("username", user.getUsername());
          m.put("orgunitshort", user.getManagementLevel1OrgUnitShort());
          m.put("edit", user.getUsername());
          users.add(m);
        }

        table.getStore().add(users);
        waitingWidget.setVisible(false);
        table.setVisible(true);
      }
    });
  }

  private ArrayList<Column<BiteUser>> createColumns() {
    ArrayList<Column<BiteUser>> columns = new ArrayList<Column<BiteUser>>();
    columns.add(new Column<BiteUser>("username", "Benutzername", "15%", createNameCellRenderer()));
    columns.add(new Column<BiteUser>("firstName", "Vorname", "16%"));
    columns.add(new Column<BiteUser>("lastName", "Nachname", "16%"));
    columns.add(new Column<BiteUser>("orgUnit", "Bereich", "14%", createOrgUnitRenderer()));
    columns.add(new Column<BiteUser>("edit", "Partner Center", "14%", createEditCellRenderer()));

    Column<BiteUser> shopid = new Column<BiteUser>("shopid", "Shop-ID", "25%", createUserShopIDCellRenderer());
    shopid.setSortable(false);
    columns.add(shopid);

    return columns;
  }

  private CellRenderer<BiteUser> createUserShopIDCellRenderer() {
    return new CellRenderer<BiteUser>() {
      @Override
      public IsWidget render(ModelData<BiteUser> model, String columnId, int rowId) {
        if (shopIDs != null && model != null && model.getBean() != null) {
          if (shopIDs.containsKey(model.getBean().getUsername().toUpperCase())) {
            return new HTML("" + shopIDs.get(model.getBean().getUsername().toUpperCase()));
          }
        }
        return new HTML("");
      }
    };
  }

  private CellRenderer<BiteUser> createEditCellRenderer() {
    if (AdminAuthorityHelper.canEditUser(UserManager.getUserInfo())) {
      return new CellRenderer<BiteUser>() {
        @Override
        public Widget render(final ModelData<BiteUser> model, String columnId, int rowId) {
          if (model.getBean().isPartnerCenterUser()) {
            Anchor link = new Anchor("Stammdaten bearbeiten");
            link.addClickHandler(new ClickHandler() {
              @Override
              public void onClick(ClickEvent event) {
                CommonServiceLocator.getRoleServlet().getUserWithRoles(model.getBean().getUsername(), new BaseAsyncCallback<UserInfo>() {
                  @Override
                  public void onSuccess(UserInfo result) {
                    partnerCenterUserDetailsPopup.show(result, EditType.ADMIN);
                  }
                });
              }
            });
            return link;
          }

          return new HTML("");

        }
      };
    }
    return null;
  }

  private CellRenderer<BiteUser> createNameCellRenderer() {
    if (AdminAuthorityHelper.canEditUser(UserManager.getUserInfo())) {
      return new CellRenderer<BiteUser>() {
        @Override
        public Widget render(final ModelData<BiteUser> model, String columnId, int rowId) {
          Anchor link = new Anchor(model.getBean().getUsername());
          link.addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
              CommonServiceLocator.getRoleServlet().getUserWithRoles(model.getBean().getUsername(), new BaseAsyncCallback<UserInfo>() {
                @Override
                public void onSuccess(UserInfo result) {
                  editUserDialog.show(result);
                }
              });
            }
          });
          return link;
        }
      };
    }
    return null;
  }

  private CellRenderer<BiteUser> createOrgUnitRenderer() {
    return new CellRenderer<BiteUser>() {
      @Override
      public Widget render(ModelData<BiteUser> model, String columnId, int rowId) {
        if (model.getBean().getManagementLevel1OrgUnitShort() == null) {
          return null;
        }
        return PortletHelper.createInfoWidget(new HTML(model.getBean().getManagementLevel1OrgUnitShort()), model.getBean().getManagementLevel1OrgUnitDescription());
      }
    };
  }
}
