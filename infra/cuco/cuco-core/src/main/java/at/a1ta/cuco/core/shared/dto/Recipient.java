package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class Recipient implements Serializable {
  private Long recipientId;
  private String recipientName;

  public Long getRecipientId() {
    return recipientId;
  }

  public void setRecipientId(Long recipientId) {
    this.recipientId = recipientId;
  }

  public String getRecipientName() {
    return recipientName;
  }

  public void setRecipientName(String recipientName) {
    this.recipientName = recipientName;
  }
}