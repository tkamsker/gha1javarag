package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class PhysicalResourceNode extends BaseNode implements Serializable {
  private String text;

  @Override
  public String getText() {
    return text;
  }

  public void setText(String text) {
    this.text = text;
  }
}
