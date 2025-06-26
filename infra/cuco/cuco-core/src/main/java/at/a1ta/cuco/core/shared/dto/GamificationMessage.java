package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

public class GamificationMessage implements Serializable {

  private static final long serialVersionUID = 1L;

  private String url;

  private String messageUid;

  private String timestamp;

  private Date timestampDateFormat;

  private String type;

  private String title;

  private String message;

  private String agentUserId;

  private boolean readByAgent = false;

  public String getUrl() {
    return url;
  }

  public void setUrl(String url) {
    this.url = url;
  }

  public String getMessageUid() {
    return messageUid;
  }

  public void setMessageUid(String messageUid) {
    this.messageUid = messageUid;
  }

  public String getTimestamp() {
    return timestamp;
  }

  public void setTimestamp(String timestamp) {
    this.timestamp = timestamp;
  }

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public String getMessage() {
    return message;
  }

  public void setMessage(String message) {
    this.message = message;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((messageUid == null) ? 0 : messageUid.hashCode());
    result = prime * result + ((type == null) ? 0 : type.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) return true;
    if (obj == null) return false;
    if (getClass() != obj.getClass()) return false;
    GamificationMessage other = (GamificationMessage) obj;
    if (messageUid == null) {
      if (other.messageUid != null) return false;
    } else if (!messageUid.equals(other.messageUid)) return false;
    if (type == null) {
      if (other.type != null) return false;
    } else if (!type.equals(other.type)) return false;
    return true;
  }

  public String getAgentUserId() {
    return agentUserId;
  }

  public void setAgentUserId(String agentUserId) {
    this.agentUserId = agentUserId;
  }

  public boolean isReadByAgent() {
    return readByAgent;
  }

  public void setReadByAgent(boolean readByAgent) {
    this.readByAgent = readByAgent;
  }

  public Date getTimestampDateFormat() {
    return timestampDateFormat;
  }

  public void setTimestampDateFormat(Date timestampDateFormat) {
    this.timestampDateFormat = timestampDateFormat;
  }

}
