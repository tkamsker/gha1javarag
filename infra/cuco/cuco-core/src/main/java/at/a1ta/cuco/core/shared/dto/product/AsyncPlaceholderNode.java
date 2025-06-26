package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class AsyncPlaceholderNode extends BaseNode implements Serializable {
  @Override
  public String getText() {
    return "wird geladen"; // TODO: externalize string
  }
}
