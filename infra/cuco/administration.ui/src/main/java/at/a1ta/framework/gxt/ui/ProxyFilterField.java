package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.data.BaseListLoader;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.event.ComponentEvent;
import com.extjs.gxt.ui.client.widget.form.TriggerField;

/**
 * @author q909158 This is a FilterField for FilterablePagingMemoryProxy.
 * @param <M>
 */
public abstract class ProxyFilterField<M> extends TriggerField<M> implements ProxyFilter<M> {
  private BaseListLoader<?> loader;

  public ProxyFilterField() {
    setAutoValidate(true);
    setValidateOnBlur(false);
    setTriggerStyle("x-form-clear-trigger");
  }

  /**
   * @see at.telekom.webclient.cuco.client.util.ProxyFilter#bind(com.extjs.gxt.ui.client.data.BaseListLoader)
   */
  @Override
  public void bind(BaseListLoader<?> loader) {
    this.loader = loader;
    try {

      FilterableMemoryProxy proxy = (FilterableMemoryProxy) loader.getProxy();
      proxy.addFilter(this);

    } catch (ClassCastException e) {
      throw new RuntimeException("ProxyFilterField can only be bound to FilterablePagingMemoryProxy");
    }
  }

  private void onClick() {
    loader.load();
  }

  @Override
  protected void onTriggerClick(ComponentEvent ce) {
    super.onTriggerClick(ce);
    if (getValue() == null || getValue().equals("")) {
      return;
    }
    setValue(null);
  }

  @Override
  protected boolean validateValue(String value) {
    boolean ret = super.validateValue(value);
    onClick();
    return ret;
  }

  @Override
  public abstract boolean doFilter(ModelData m);
}
