package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class GamificationCuCoMessages implements Serializable {
  private static final long serialVersionUID = 1L;

  private String agentId;

  private List<GamificationMessage> messages = new ArrayList<GamificationMessage>();

  public String getAgentId() {
    return agentId;
  }

  public void setAgentId(String agentId) {
    this.agentId = agentId;
  }

  public List<GamificationMessage> getMessages() {
    return messages;
  }

  public void setMessages(List<GamificationMessage> messages) {
    this.messages = messages;
  }
}