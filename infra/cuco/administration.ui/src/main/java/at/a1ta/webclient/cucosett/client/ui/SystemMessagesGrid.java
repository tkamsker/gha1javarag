package at.a1ta.webclient.cucosett.client.ui;

import java.util.ArrayList;
import java.util.List;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.logical.shared.SelectionEvent;
import com.google.gwt.event.logical.shared.SelectionHandler;
import com.google.gwt.i18n.client.DateTimeFormat;
import com.google.gwt.user.client.ui.Anchor;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.IsWidget;
import com.google.gwt.user.client.ui.SimplePanel;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.systemmessage.SystemMessage;
import at.a1ta.bite.ui.client.Delegate;
import at.a1ta.bite.ui.client.bundle.UI;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.Button.ButtonSize;
import at.a1ta.bite.ui.client.widget.ClickableIcon;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.admin.ui.common.client.ui.SystemMessagePreviewComponent;
import at.a1ta.cuco.ui.common.client.bundle.CuCoUI;
import at.a1ta.cuco.ui.common.client.ui.ModelData;
import at.a1ta.cuco.ui.common.client.ui.table.CellRenderer;
import at.a1ta.cuco.ui.common.client.ui.table.Column;
import at.a1ta.cuco.ui.common.client.ui.table.DataTable;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.PortletEvent;
import at.a1ta.framework.ui.client.event.PortletEventListener;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.framework.ui.client.service.ServiceLocator;
import at.a1ta.framework.ui.client.ui.dialog.DialogPanel;
import at.a1ta.framework.ui.client.util.Validator;
import at.a1ta.webclient.cucosett.client.dialog.GwtEditMessageDialog;

public class SystemMessagesGrid extends SimplePanel implements SelectionHandler<Integer> {

  private DataTable<SystemMessage> table;

  private Widget panel = null;

  private Button newMessageBtn;

  private Delegate<SystemMessage> viewMessageDelegate;

  private Delegate<SystemMessage> copyMessageDelegate;

  private final int tabIndex;

  private final boolean activeMsg;

  private boolean initialized;

  private boolean dirty;

  private DateTimeFormat fmt = DateTimeFormat.getFormat("dd.MM.yyyy");

  public SystemMessagesGrid(int tabIndex, boolean activeMsg) {
    this.tabIndex = tabIndex;
    this.activeMsg = activeMsg;
  }

  @Override
  public void onSelection(SelectionEvent<Integer> event) {
    if (event.getSelectedItem() != tabIndex) {
      deactviate();
    } else {

      if (!initialized) {
        initUI();
        load();
      }
      activate();
    }
  }

  public Widget getPanel() {
    return panel;
  }

  public void load() {
    if (activeMsg) {
      ServiceLocator.getSystemMessageService().loadUnexpiredMessages(createCallback());
    } else {
      ServiceLocator.getSystemMessageService().loadExpiredMessages(createCallback());
    }
  }

  private final void activate() {
    if (dirty) {
      load();
    }
  }

  private final void deactviate() {
    if (initialized) {
      // Do Nothing
    }
  }

  private BaseAsyncCallback<List<SystemMessage>> createCallback() {
    return new BaseAsyncCallback<List<SystemMessage>>() {

      @Override
      public void onSuccess(List<SystemMessage> result) {
        ArrayList<ModelData<SystemMessage>> models = new ArrayList<ModelData<SystemMessage>>();
        for (SystemMessage systemMessage : result) {
          ModelData<SystemMessage> m = new ModelData<SystemMessage>(systemMessage);
          m.put("id", systemMessage.getId() + "");
          if (Validator.isNullOrEmpty(systemMessage.getMessageContent().getImageUri())) {
            m.put("imgUri", "");
          } else {
            m.put("imgUri", "extImg/" + systemMessage.getMessageContent().getImageUri());
          }
          m.put("title", systemMessage.getMessageContent().getTitle());
          m.put("validity", getFmt().format(systemMessage.getPeriodOfValidity().getValidFrom()) + " - " + getFmt().format(systemMessage.getPeriodOfValidity().getValidUntil()));
          m.put("preview", systemMessage.getId() + "");
          models.add(m);
        }
        if (table.getStore() != null) {
          table.getStore().clear();
        }
        table.getStore().add(models);

        table.showFirstPage();
      }
    };
  }

  public DateTimeFormat getFmt() {
    return fmt;
  }

  public Widget initUI() {
    initialized = true;
    initTable();
    HTMLPanel pnl = new HTMLPanel("");
    pnl.setStyleName(UI.STYLES.bite_moduleContent());
    HorizontalPanel newMessage = createNewMessageRow();
    pnl.add(newMessage);

    pnl.add(new HTML("<div class='" + UI.STYLES.bite_heightPlaceHolder() + "'/>"));

    pnl.add(table);
    viewMessageDelegate = new Delegate<SystemMessage>() {

      @Override
      public void execute(final SystemMessage systemMessage) {
        DialogPanel dialog = new DialogPanel();
        dialog.setCaption(AdminUI.ADMINCOMMONTEXTPOOL.smPreview());
        dialog.setSize(600, 500);
        dialog.add(new SystemMessagePreviewComponent(systemMessage.getId()));
        dialog.center();
      }
    };

    copyMessageDelegate = new Delegate<SystemMessage>() {

      @Override
      public void execute(final SystemMessage systemMessage) {
        GwtEditMessageDialog p = new GwtEditMessageDialog(systemMessage.getId(), true);
        load();
        dirty = true;
        p.show();
      }
    };

    PortletEventManager.addListener(CuCoEventType.LOAD_MESSAGES, new PortletEventListener<PortletEvent>() {

      @Override
      public void handleEvent(PortletEvent be) {
        load();
      }
    });
    load();
    add(pnl);
    return pnl;
  }

  public boolean isDirty() {
    return dirty;
  }

  public void setDirty(boolean dirty) {
    this.dirty = dirty;
  }

  public void initTable() {
    table = new DataTable<SystemMessage>(createColumns());
    table.enablePaging(10);
  }

  private HorizontalPanel createNewMessageRow() {
    HorizontalPanel newMessage = new HorizontalPanel();
    if (activeMsg) {
      newMessage.add(createMessageButton());
    }
    return newMessage;
  }

  private Button createMessageButton() {
    newMessageBtn = new Button(AdminUI.ADMINCOMMONTEXTPOOL.smNewMessage(), ButtonSize.Small);

    newMessageBtn.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        GwtEditMessageDialog p = new GwtEditMessageDialog(0, false);
        load();
        dirty = true;
        p.show();
      }
    });
    return newMessageBtn;
  }

  private ArrayList<Column<SystemMessage>> createColumns() {
    ArrayList<Column<SystemMessage>> columns = new ArrayList<Column<SystemMessage>>();
    columns.add(new Column<SystemMessage>("id", AdminUI.ADMINCOMMONTEXTPOOL.smId(), "20%", createIdCellRenderer()));
    columns.add(new Column<SystemMessage>("imgUri", AdminUI.ADMINCOMMONTEXTPOOL.smImage(), "20%"));
    columns.add(new Column<SystemMessage>("title", AdminUI.ADMINCOMMONTEXTPOOL.smTitle(), "20%"));
    columns.add(new Column<SystemMessage>("validity", AdminUI.ADMINCOMMONTEXTPOOL.smValidity(), "20%"));
    columns.add(new Column<SystemMessage>("preview", AdminUI.ADMINCOMMONTEXTPOOL.smPreview(), "10%", createViewCellRenderer()));
    columns.add(new Column<SystemMessage>("copy", "Kopieren", "10%", createCopyCellRenderer()));
    return columns;
  }

  private CellRenderer<SystemMessage> createIdCellRenderer() {
    if (activeMsg) {
      return new CellRenderer<SystemMessage>() {
        @Override
        public Widget render(final ModelData<SystemMessage> model, String columnId, int rowId) {
          Anchor link = new Anchor(model.getBean().getId().toString());
          link.addClickHandler(new ClickHandler() {
            @Override
            public void onClick(ClickEvent event) {
              Long id = model.getBean().getId();
              GwtEditMessageDialog p = new GwtEditMessageDialog(id, false);
              load();
              dirty = true;
              p.show();

            }
          });
          return link;
        }
      };
    }
    return null;
  }

  private CellRenderer<SystemMessage> createViewCellRenderer() {
    return new CellRenderer<SystemMessage>() {
      @Override
      public IsWidget render(final ModelData<SystemMessage> model, String columnId, int rowId) {
        return new ClickableIcon<SystemMessage>(model.getBean(), viewMessageDelegate, UI.IMAGES.iconView(), null);
      }
    };
  }

  private CellRenderer<SystemMessage> createCopyCellRenderer() {
    return new CellRenderer<SystemMessage>() {
      @Override
      public IsWidget render(final ModelData<SystemMessage> model, String columnId, int rowId) {
        return new ClickableIcon<SystemMessage>(model.getBean(), copyMessageDelegate, CuCoUI.IMAGES.iconCalcActionSmallCopy(), null);
      }
    };
  }

}