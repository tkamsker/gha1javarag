package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class EmptyProductNode extends BaseNode implements Serializable {
  @Override
  public String getText() {
    return "Keine Produkte"; // TODO: externalize string
  }
}
