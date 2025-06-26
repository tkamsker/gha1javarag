package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.core.XDOM;
import com.google.gwt.dom.client.Element;
import com.google.gwt.user.client.ui.impl.PopupImplIE6;

public class PopupImplIE6Extended extends PopupImplIE6 {

  @Override
  public void onShow(Element popup) {
    super.onShow(popup);
    popup.getStyle().setZIndex(XDOM.getTopZIndex());
  }

}
