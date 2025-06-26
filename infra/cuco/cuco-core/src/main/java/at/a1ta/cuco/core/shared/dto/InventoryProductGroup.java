package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class InventoryProductGroup implements Serializable {
  private Long id;
  private String name;
  private int order;
  private boolean visible;
  private boolean anb;

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public int getOrder() {
    return order;
  }

  public void setOrder(int order) {
    this.order = order;
  }

  public boolean isVisible() {
    return visible;
  }

  public void setVisible(boolean visible) {
    this.visible = visible;
  }

  public boolean isAnb() {
    return anb;
  }

  public void setAnb(boolean anb) {
    this.anb = anb;
  }

}
