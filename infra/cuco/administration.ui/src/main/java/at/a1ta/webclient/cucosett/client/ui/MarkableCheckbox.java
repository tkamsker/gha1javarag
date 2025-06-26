package at.a1ta.webclient.cucosett.client.ui;

import com.google.gwt.user.client.ui.CheckBox;

public class MarkableCheckbox<B> extends CheckBox {

  private B marker;

  public MarkableCheckbox(B marker) {
    super(marker.toString());
    this.marker = marker;
  }

  public B getMarker() {
    return marker;
  }
}
