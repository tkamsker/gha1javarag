package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.event.ComponentEvent;
import com.extjs.gxt.ui.client.event.Events;
import com.extjs.gxt.ui.client.event.Listener;
import com.extjs.gxt.ui.client.widget.Component;
import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.LayoutContainer;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.button.ToolButton;
import com.google.gwt.core.client.Scheduler;
import com.google.gwt.core.client.Scheduler.ScheduledCommand;
import com.google.gwt.event.logical.shared.ResizeEvent;
import com.google.gwt.event.logical.shared.ResizeHandler;
import com.google.gwt.event.shared.HandlerRegistration;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.Window.ScrollEvent;
import com.google.gwt.user.client.Window.ScrollHandler;
import com.google.gwt.user.client.ui.SimplePanel;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.core.shared.dto.PortletDefinition;
import at.a1ta.bite.ui.client.widget.WaitingWidget;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.framework.ui.client.ui.ErrorWidgetHolder;
import at.a1ta.framework.ui.client.ui.TextWidget;

/**
 * Base class for all detail views of the portlets. Consists of a card layout to switch between different contents:
 * <ul>
 * <li>showLoading() - shows the loading widget</li>
 * <li>showContent() - shows the normal content</li>
 * <li>showEmptyContent() - shows that no content exists</li>
 * <li>showError() - shows an error label</li>
 * </ul>
 */
public abstract class DetailsDialog extends Dialog implements ErrorWidgetHolder {

  // GXT wrapper for rootPanel. Allows to re-parent the rootPanel (i.e. the wrapper) to other widgets. Re-parenting
  // GWT widgets only work if current parent implements HasWidgets interface.
  private LayoutContainer wrapper = new LayoutContainer();

  private SimplePanel rootPanel;

  private WaitingWidget loadingWidget;

  private TextWidget emptyContent;

  private VerticalPanel contentPanel;

  private TextWidget errorWidget;

  // indicates whether the data is dirty and the details should render again or only show
  private boolean dirty = true;

  private ScrollHandler scrollHandler;

  private HandlerRegistration windowScrollHandler;

  private ResizeHandler resizeHandler;

  private HandlerRegistration windowResizeHandler;

  private final PortletDefinition portletDefinition;

  public DetailsDialog(PortletDefinition portletDefinition, String header) {
    this.portletDefinition = portletDefinition;
    setModal(true);
    setFrame(true);
    setHeading(header);
    setClosable(true);
    setButtons(CLOSE);
    setBodyBorder(false);
    setBorders(false);
    setOnEsc(true);
    setSize(950, 500);
    setPlain(true);
    setShim(false);

    scrollHandler = new ScrollHandler() {

      @Override
      public void onWindowScroll(ScrollEvent event) {
        Scheduler.get().scheduleDeferred(new ScheduledCommand() {

          @Override
          public void execute() {
            el().center();
          }
        });
      }
    };

    resizeHandler = new ResizeHandler() {

      @Override
      public void onResize(ResizeEvent event) {
        Scheduler.get().scheduleDeferred(new ScheduledCommand() {

          @Override
          public void execute() {
            el().center();
          }
        });
      }
    };

    createContent();
  }

  private void createContent() {
    rootPanel = new SimplePanel();
    rootPanel.setSize("100%", "100%");
    wrapper.add(rootPanel);

    WaitingWidget lw = new WaitingWidget(AdminUI.ADMINCOMMONTEXTPOOL.loading());
    lw.setSize("100%", "100%");
    loadingWidget = lw;

    emptyContent = createEmptyContentWidget();
    contentPanel = new VerticalPanel();
    contentPanel.setSize("100%", "100%");
    contentPanel.setSpacing(3);

    errorWidget = new TextWidget(AdminUI.ADMINCOMMONTEXTPOOL.error());
  }

  @Override
  protected void initTools() {

    if (isPrintable()) {
      ToolButton printBtn = new ToolButton("x-tool-print");
      printBtn.addListener(Events.Select, new Listener<ComponentEvent>() {

        @Override
        public void handleEvent(ComponentEvent ce) {
          print();
        }
      });
      head.addTool(printBtn);
    }
    super.initTools();
  }

  private boolean isPrintable() {
    return false;
  }

  private void print() {}

  @Override
  protected void onHide() {
    super.onHide();
    windowScrollHandler.removeHandler();
    windowResizeHandler.removeHandler();
  }

  @Override
  protected void onShow() {
    super.onShow();
    windowScrollHandler = Window.addWindowScrollHandler(scrollHandler);
    windowResizeHandler = Window.addResizeHandler(resizeHandler);
  }

  @Override
  protected void afterShow() {
    super.afterShow();
    el().center(true);
  }

  public final void init() {
    showLoading();
    super.removeAll();

    Widget top = createTopComponent();
    if (top != null) {
      super.add(top);
    }
    super.add(wrapper);
    layout();
    showLoading();

    // getContentPanel().removeAll();
    Scheduler.get().scheduleDeferred(new ScheduledCommand() {

      @Override
      public void execute() {
        createDetailsContent();
        Scheduler.get().scheduleDeferred(new ScheduledCommand() {

          @Override
          public void execute() {
            layout(); // layout content
          }
        });
      }
    });

  }

  public LayoutContainer getRootContainer() {
    return wrapper;
  }

  private Widget createTopComponent() {
    return null;
  }

  protected VerticalPanel getContentPanel() {
    return contentPanel;
  }

  public void showLoading() {
    loadingWidget.setSize("100%", "100%");
    rootPanel.setWidget(loadingWidget);
  }

  protected void showEmptyContent() {
    emptyContent.setSize("100%", "100%");
    rootPanel.setWidget(emptyContent);
  }

  public void showContent() {
    Scheduler.get().scheduleDeferred(new ScheduledCommand() {

      @Override
      public void execute() {
        contentPanel.setSize("100%", "100%");
        rootPanel.setWidget(contentPanel);
        // contentPanel.layout();
      }
    });
  }

  @Override
  public void showError() {
    errorWidget.setSize("100%", "100%");
    rootPanel.setWidget(errorWidget);
  }

  @Override
  public boolean add(Widget widget) {
    contentPanel.add(widget);
    return true;
  }

  @Override
  public boolean add(Component c) {
    contentPanel.add(c);
    return true;
  }

  private TextWidget createEmptyContentWidget() {
    return new TextWidget(getEmtpyWidgetLabel());
  }

  private String getEmtpyWidgetLabel() {
    return AdminUI.ADMINCOMMONTEXTPOOL.noData();
  }

  protected abstract void createDetailsContent();

  @Override
  protected void onButtonPressed(Button button) {
    hide(button);
  }

  public void setDirty(boolean dirty) {
    this.dirty = dirty;
  }

  public boolean isDirty() {
    return dirty;
  }

  public LayoutContainer getPrintContainer() {
    return getRootContainer();
  }

  public PortletDefinition getPortletDefinition() {
    return portletDefinition;
  }

}
