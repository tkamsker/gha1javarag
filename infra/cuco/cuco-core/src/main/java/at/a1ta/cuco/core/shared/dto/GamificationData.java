package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class GamificationData implements Serializable {
  private static final long serialVersionUID = 1L;
  private GamificationCuCoMessages cucoMessages;

  public GamificationCuCoMessages getCucoMessages() {
    return cucoMessages;
  }

  public void setCucoMessages(GamificationCuCoMessages cucoMessages) {
    this.cucoMessages = cucoMessages;
  }
}