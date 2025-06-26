package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class VipStatus implements Serializable {

  public enum State {
    VIP, NO_VIP, UNKNOWN;
  }

  private Integer intValue;
  private State state;

  public VipStatus() {
    state = State.UNKNOWN;
  }

  public VipStatus(State state) {
    this.state = state;
  }

  public VipStatus(Integer intValue) {
    this.intValue = intValue;
    state = intValue != null ? State.VIP : State.NO_VIP;
  }

  public Integer getIntValue() {
    return intValue;
  }

  public void setIntValue(Integer intValue) {
    this.intValue = intValue;
  }

  public State getState() {
    return state;
  }

  public void setState(State state) {
    this.state = state;
  }

}
