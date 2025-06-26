package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class GamificationResponse implements Serializable {

  private static final long serialVersionUID = 1L;
  private GamificationData data;

  private String status;

  private int unreadMsgCount;

  public String getAgentId() {
    return getData() != null && getData().getCucoMessages() != null ? getData().getCucoMessages().getAgentId() : "-";
  }

  public List<GamificationMessage> getMessages() {
    return getData() != null && getData().getCucoMessages() != null ? getData().getCucoMessages().getMessages() : new ArrayList<GamificationMessage>();
  }

  public void setStatus(String status) {
    this.status = status;

  }

  public String getStatus() {
    return this.status;
  }

  public GamificationData getData() {
    return data;
  }

  public void setData(GamificationData data) {
    this.data = data;
  }

  public int getUnreadMsgCount() {
    return unreadMsgCount;
  }

  public void setUnreadMsgCount(int unreadMsgCount) {
    this.unreadMsgCount = unreadMsgCount;
  }
}
