package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.GXT;
import com.extjs.gxt.ui.client.event.FieldEvent;
import com.extjs.gxt.ui.client.widget.form.NumberField;

/**
 * Workaround for an issue with number fields and GWT2.1. Current GXT version: 2.1.2
 */
public class NumberFieldFixed extends NumberField {

  @Override
  protected void onKeyPress(FieldEvent fe) {
    if ( !GXT.isGecko) {
      super.onKeyPress(fe);
    }
  }
}
