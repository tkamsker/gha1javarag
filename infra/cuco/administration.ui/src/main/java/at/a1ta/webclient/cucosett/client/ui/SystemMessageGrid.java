package at.a1ta.webclient.cucosett.client.ui;

import java.util.ArrayList;
import java.util.List;

import com.extjs.gxt.ui.client.data.BaseModelData;
import com.extjs.gxt.ui.client.data.BasePagingLoader;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.data.PagingLoadResult;
import com.extjs.gxt.ui.client.data.PagingModelMemoryProxy;
import com.extjs.gxt.ui.client.event.ButtonEvent;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.SelectionChangedEvent;
import com.extjs.gxt.ui.client.event.SelectionChangedListener;
import com.extjs.gxt.ui.client.event.SelectionListener;
import com.extjs.gxt.ui.client.event.WindowEvent;
import com.extjs.gxt.ui.client.event.WindowListener;
import com.extjs.gxt.ui.client.store.ListStore;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.grid.ColumnConfig;
import com.extjs.gxt.ui.client.widget.grid.ColumnModel;
import com.extjs.gxt.ui.client.widget.toolbar.ToolBar;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.logical.shared.SelectionEvent;
import com.google.gwt.event.logical.shared.SelectionHandler;
import com.google.gwt.i18n.client.DateTimeFormat;
import com.google.gwt.user.client.ui.SimplePanel;

import at.a1ta.bite.core.shared.dto.systemmessage.SystemMessage;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.ui.SystemMessagePreviewComponent;
import at.a1ta.framework.gxt.ui.LinkCellRenderer;
import at.a1ta.framework.gxt.ui.PagingGridContainer;
import at.a1ta.framework.gxt.ui.Util;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.service.ServiceLocator;
import at.a1ta.framework.ui.client.ui.dialog.DialogPanel;
import at.a1ta.framework.ui.client.util.Validator;
import at.a1ta.webclient.cucosett.client.dialog.EditMessageDialog;

public class SystemMessageGrid extends SimplePanel implements SelectionHandler<Integer> {

  private final int tabIndex;

  private final boolean activeMsg;

  private ToolBar toolbar = new ToolBar();

  private PagingGridContainer<ListStore<ModelData>, ModelData> gridContainer;

  private Button newMessageBtn = new Button();

  private Button copyBtn = new Button();

  private EditButtonListener editHandler = new EditButtonListener();

  private CopyButtonListener copyHandler = new CopyButtonListener();

  private PreviewButtonListener prevHandler = new PreviewButtonListener();

  private IconButtonRenderer prevRenderer = new IconButtonRenderer(prevHandler,
      at.a1ta.cuco.ui.common.client.bundle.CuCoUI.IMAGES.icon_preview());

  private ImageRenderer imgRenderer = new ImageRenderer(0, 70);

  private DateTimeFormat fmt = DateTimeFormat.getFormat("dd.MM.yyyy");

  private HideWindowListener hideListener = new HideWindowListener();

  private PagingModelMemoryProxy dataProxy;

  private ListStore<ModelData> store;

  private boolean initialized;

  private boolean dirty;

  public SystemMessageGrid(int tabIndex, boolean activeMsg) {
    this.tabIndex = tabIndex;
    this.activeMsg = activeMsg;
  }

  @Override
  public void onSelection(SelectionEvent<Integer> event) {
    if (event.getSelectedItem() != tabIndex) {
      deactviate();
    } else {
      if (!initialized) {
        init();
        load();
      }
      activate();
    }
  }

  private void load() {
    if (activeMsg) {
      ServiceLocator.getSystemMessageService().loadUnexpiredMessages(createCallback());
    } else {
      ServiceLocator.getSystemMessageService().loadExpiredMessages(createCallback());
    }
  }

  private BaseAsyncCallback<List<SystemMessage>> createCallback() {
    return new BaseAsyncCallback<List<SystemMessage>>() {

      @Override
      @SuppressWarnings("unchecked")
      public void onSuccess(List<SystemMessage> result) {
        List<BaseModelData> models = new ArrayList<BaseModelData>();
        for (SystemMessage systemMessage : result) {
          BaseModelData m = new BaseModelData();
          m.set("id", systemMessage.getId() + "");
          if (Validator.isNullOrEmpty(systemMessage.getMessageContent().getImageUri())) {
            m.set("imgUri", "");
          } else {
            m.set("imgUri", Util.getExtImgPath() + systemMessage.getMessageContent().getImageUri());
          }
          m.set("title", systemMessage.getMessageContent().getTitle());
          m.set(
              "validity",
              getFmt().format(systemMessage.getPeriodOfValidity().getValidFrom()) + " - "
                  + getFmt().format(systemMessage.getPeriodOfValidity().getValidUntil()));
          m.set("preview", systemMessage.getId() + "");
          models.add(m);
        }

        ((List<BaseModelData>) dataProxy.getData()).clear();
        ((List<BaseModelData>) dataProxy.getData()).addAll(models);

        gridContainer.first();
      }
    };
  }

  private final void activate() {
    getCopy().setEnabled(false);
    if (dirty) {
      load();
    }
  }

  private final void deactviate() {
    if (initialized) {
      gridContainer.getGrid().getSelectionModel().deselectAll();
    }
  }

  private void init() {
    initialized = true;

    newMessageBtn.setText(AdminUI.ADMINCOMMONTEXTPOOL.smNewMessage());
    newMessageBtn.addSelectionListener(editHandler);
    copyBtn.setText(AdminUI.ADMINCOMMONTEXTPOOL.smCopy());
    copyBtn.addSelectionListener(copyHandler);

    dataProxy = new PagingModelMemoryProxy(new ArrayList<BaseModelData>());
    BasePagingLoader<PagingLoadResult<BaseModelData>> loader = new BasePagingLoader<PagingLoadResult<BaseModelData>>(dataProxy);
    loader.setRemoteSort(true);
    store = new ListStore<ModelData>(loader);

    gridContainer = new PagingGridContainer<ListStore<ModelData>, ModelData>(store, createColumnModel(), 10, 400);
    gridContainer.getGrid().getSelectionModel().addSelectionChangedListener(new SelectionChangedListener<ModelData>() {

      @Override
      public void selectionChanged(SelectionChangedEvent<ModelData> se) {
        getCopy().setEnabled(se.getSelectedItem() != null);
      }
    });

    fillToolBar(toolbar);
    gridContainer.setTopComponent(toolbar);
    add(gridContainer);
  }

  private void fillToolBar(ToolBar toolbar) {
    if (activeMsg) {
      toolbar.add(getNewMessage());
    }
    toolbar.add(getCopy());
  }

  public Button getNewMessage() {
    return newMessageBtn;
  }

  public Button getCopy() {
    return copyBtn;
  }

  public CopyButtonListener getCopyHandler() {
    return copyHandler;
  }

  public PreviewButtonListener getPrevHandler() {
    return prevHandler;
  }

  public IconButtonRenderer getPrevRenderer() {
    return prevRenderer;
  }

  public ImageRenderer getImgRenderer() {
    return imgRenderer;
  }

  public DateTimeFormat getFmt() {
    return fmt;
  }

  public HideWindowListener getHideListener() {
    return hideListener;
  }

  private class HideWindowListener extends WindowListener {

    @Override
    public void handleEvent(WindowEvent e) {
      if (e.getType() == Events.Hide) {
        load();
        dirty = true;
      }
    }
  }

  private class EditButtonListener extends SelectionListener<ButtonEvent> {

    @Override
    public void componentSelected(ButtonEvent ce) {
      Button button = ce.getButton();

      long id = 0;
      if (button != newMessageBtn) {
        id = Long.parseLong(button.getText());
      }
      EditMessageDialog p = new EditMessageDialog(AdminUI.ADMINCOMMONTEXTPOOL.smEditMessage(), id, false);
      p.addWindowListener(hideListener);
      p.show();
    }
  }

  private class CopyButtonListener extends SelectionListener<ButtonEvent> {

    @Override
    public void componentSelected(ButtonEvent ce) {
      ModelData data = gridContainer.getGrid().getSelectionModel().getSelectedItem();

      if (data != null) {
        long id = Long.parseLong((String) data.get("id"));
        EditMessageDialog p = new EditMessageDialog(AdminUI.ADMINCOMMONTEXTPOOL.smEditMessage(), id, true);
        p.addWindowListener(hideListener);
        p.show();
      }
    }
  }

  private class PreviewButtonListener extends SelectionListener<ButtonEvent> {

    @Override
    public void componentSelected(ButtonEvent ce) {
      Button button = ce.getButton();

      long id = 0;
      id = Long.parseLong(button.getItemId());
      DialogPanel dialog = new DialogPanel();
      dialog.setCaption(AdminUI.ADMINCOMMONTEXTPOOL.smPreview());
      dialog.setSize(600, 500);
      dialog.add(new SystemMessagePreviewComponent(id));
      dialog.center();
    }
  }

  private ColumnModel createColumnModel() {
    List<ColumnConfig> columns = new ArrayList<ColumnConfig>();
    ColumnConfig idColumn = new ColumnConfig("id", AdminUI.ADMINCOMMONTEXTPOOL.smId(), 100);
    idColumn.setMenuDisabled(true);
    if (activeMsg) {
      idColumn.setRenderer(new LinkCellRenderer(new ClickHandler() {

        @Override
        public void onClick(ClickEvent event) {
          Long id = Long.parseLong((String) gridContainer.getGrid().getSelectionModel().getSelectedItem().get("id"));
          EditMessageDialog p = new EditMessageDialog(AdminUI.ADMINCOMMONTEXTPOOL.smEditMessage(), id, false);
          p.addWindowListener(hideListener);
          p.show();
        }
      }));
    }
    columns.add(idColumn);

    ColumnConfig imgColumn = new ColumnConfig("imgUri", AdminUI.ADMINCOMMONTEXTPOOL.smImage(), 100);
    imgColumn.setMenuDisabled(true);
    imgColumn.setRenderer(getImgRenderer());
    columns.add(imgColumn);

    ColumnConfig titleColumn = new ColumnConfig("title", AdminUI.ADMINCOMMONTEXTPOOL.smTitle(), 100);
    titleColumn.setMenuDisabled(true);
    columns.add(titleColumn);

    ColumnConfig valColumn = new ColumnConfig("validity", AdminUI.ADMINCOMMONTEXTPOOL.smValidity(), 100);
    valColumn.setMenuDisabled(true);
    columns.add(valColumn);

    ColumnConfig prevColumn = new ColumnConfig("preview", AdminUI.ADMINCOMMONTEXTPOOL.smPreview(), 100);
    prevColumn.setMenuDisabled(true);
    prevColumn.setRenderer(getPrevRenderer());
    columns.add(prevColumn);

    return new ColumnModel(columns);
  }

  public boolean isDirty() {
    return dirty;
  }

  public void setDirty(boolean dirty) {
    this.dirty = dirty;
  }
}
