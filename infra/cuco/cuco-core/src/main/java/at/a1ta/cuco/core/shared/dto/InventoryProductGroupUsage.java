package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class InventoryProductGroupUsage implements Serializable {
  private String name;
  private int number;
  private boolean anb;
  private int order;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public int getNumber() {
    return number;
  }

  public void setNumber(int number) {
    this.number = number;
  }

  public boolean isAnb() {
    return anb;
  }

  public void setAnb(boolean anb) {
    this.anb = anb;
  }

  public int getOrder() {
    return order;
  }

  public void setOrder(int order) {
    this.order = order;
  }

}
