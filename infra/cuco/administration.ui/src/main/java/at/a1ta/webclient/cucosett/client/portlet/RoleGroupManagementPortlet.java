package at.a1ta.webclient.cucosett.client.portlet;

import java.util.ArrayList;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.BasePagingLoader;
import com.extjs.gxt.ui.client.data.LoadConfig;
import com.extjs.gxt.ui.client.data.PagingLoadResult;
import com.extjs.gxt.ui.client.event.BaseEvent;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.toolbar.ToolBar;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.bite.core.shared.dto.security.RoleGroup;
import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.service.CommonServiceLocator;
import at.a1ta.cuco.admin.ui.common.client.ui.ImageRenderer;
import at.a1ta.cuco.ui.common.shared.AdminAuthorityHelper;
import at.a1ta.framework.gxt.ui.FilterablePagingMemoryProxy;
import at.a1ta.framework.gxt.ui.LinkCellRenderer;
import at.a1ta.framework.gxt.ui.PagingGridContainer;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.dialog.EditRoleGroupDialog;

public class RoleGroupManagementPortlet extends CuCoSettBasePortlet {

  public static final String NAME = "RollengruppenverwaltungOld";

  private static RoleGroupManagementPortlet _instance;

  private PagingGridContainer<ListStore<BaseModelData>, BaseModelData> gridContainer;

  public static RoleGroupManagementPortlet create(PortletDefinition portletDefinition) {
    if (_instance == null) {
      _instance = new RoleGroupManagementPortlet(portletDefinition, false);
    }
    return _instance;
  }

  private RoleGroupManagementPortlet(PortletDefinition def, boolean isDetails) {
    super(def, isDetails, false, false);

    add(renderGrid());

    PortletEventManager.addListener(CuCoEventType.UPDATE_ROLEGROUP, new PortletEventListener<GenericEvent<RoleGroup>>() {

      @Override
      public void handleEvent(GenericEvent<RoleGroup> be) {
        RoleGroup group = be.get();
        for (BaseModelData bm : gridContainer.getGrid().getStore().getModels()) {
          if (((RoleGroup) bm.get("bean")).getId().equals(group.getId())) {
            bm.set("bean", group);
            bm.set("desc", group.getDescription());
            return;
          }
        }

        BaseModelData m = new BaseModelData();
        m.set("bean", group);
        m.set("name", group.getName());
        m.set("desc", group.getDescription());

        gridContainer.getGrid().getStore().add(m);
      }
    });
  }

  private Widget renderGrid() {

    ListStore<BaseModelData> store = new ListStore<BaseModelData>();

    gridContainer = new PagingGridContainer<ListStore<BaseModelData>, BaseModelData>(store, createRoleGroupColumnModel(), 10);
    gridContainer.getGrid().setAutoExpandColumn("name");

    if (AdminAuthorityHelper.canCreateRoleGroup(UserManager.getUserInfo())) {
      Button newBtn = new Button("Neue Rollengruppe");
      newBtn.addSelectionListener(new SelectionListener<ButtonEvent>() {

        @Override
        public void componentSelected(ButtonEvent ce) {
          EditRoleGroupDialog d = new EditRoleGroupDialog("Neue Rollengruppe", null);
          d.show();
        }
      });

      ToolBar tb = new ToolBar();
      tb.add(newBtn);
      gridContainer.setTopComponent(tb);
    }

    return gridContainer;
  }

  @Override
  public void init() {
    gridContainer.getGrid().getStore().removeAll();

    CommonServiceLocator.getRoleServlet().getAllRoleGroups(new BaseAsyncCallback<ArrayList<RoleGroup>>(this) {

      @Override
      public void onSuccess(ArrayList<RoleGroup> result) {
        ArrayList<BaseModelData> results = new ArrayList<BaseModelData>();

        for (RoleGroup group : result) {
          BaseModelData m = new BaseModelData();
          m.set("bean", group);
          m.set("name", group.getName());
          m.set("desc", group.getDescription());
          results.add(m);
        }

        FilterablePagingMemoryProxy proxy = new FilterablePagingMemoryProxy(results);
        // loader
        BasePagingLoader<PagingLoadResult<LoadConfig>> gridloader = new BasePagingLoader<PagingLoadResult<LoadConfig>>(proxy);
        gridloader.setRemoteSort(true);
        gridContainer.getToolbar().bind(gridloader);

        ListStore<BaseModelData> store = new ListStore<BaseModelData>(gridloader);
        gridContainer.reconfigure(store);
        gridloader.load();
        showContent();
      }
    });
  }

  private ColumnModel createRoleGroupColumnModel() {
    ArrayList<ColumnConfig> columns = new ArrayList<ColumnConfig>();

    ColumnConfig c = new ColumnConfig("name", "Bezeichnung", 30);
    c.setRenderer(new LinkCellRenderer(new ClickHandler() {

      @Override
      public void onClick(ClickEvent event) {
        if (gridContainer.getGrid().getSelectionModel().getSelectedItem() != null) {
          EditRoleGroupDialog d = new EditRoleGroupDialog("Rollengruppe bearbeiten", (RoleGroup) gridContainer.getGrid().getSelectionModel().getSelectedItem().get("bean"));
          d.show();
        }
      }
    }));
    columns.add(c);
    columns.add(new ColumnConfig("desc", "Beschreibung", 60));
    c = new ColumnConfig("delete", "Löschen", 10);
    c.setRenderer(new ImageRenderer(ImageRenderer.ERASE, new Listener<BaseEvent>() {

      @Override
      public void handleEvent(BaseEvent be) {
        final BaseModelData m = gridContainer.getGrid().getSelectionModel().getSelectedItem();
        if (Window.confirm("Soll " + m.get("name") + " gelöscht werden?")) {
          CommonServiceLocator.getRoleServlet().deleteRoleGroup(((RoleGroup) m.get("bean")).getId(), new BaseAsyncCallback<RpcStatus>() {

            @Override
            public void onSuccess(RpcStatus result) {
              gridContainer.getGrid().getStore().remove(m);
            }
          });
        }

      }
    }));
    columns.add(c);

    return new ColumnModel(columns);
  }
}
