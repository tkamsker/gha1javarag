package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Map;

public class SalesConvEmailData implements Serializable {
  String partyId;
  String sender;
  String recipient;
  String subject;
  String message;
  Map<String, String> attachmentUrls;

  public String getPartyId() {
    return partyId;
  }

  public void setPartyId(String partyId) {
    this.partyId = partyId;
  }

  public String getSender() {
    return sender;
  }

  public void setSender(String sender) {
    this.sender = sender;
  }

  public String getRecipient() {
    return recipient;
  }

  public void setRecipient(String recipient) {
    this.recipient = recipient;
  }

  public String getSubject() {
    return subject;
  }

  public void setSubject(String subject) {
    this.subject = subject;
  }

  public String getMessage() {
    return message;
  }

  public void setMessage(String message) {
    this.message = message;
  }

  public Map<String, String> getAttachmentUrls() {
    return attachmentUrls;
  }

  public void setAttachmentUrls(Map<String, String> attachmentUrls) {
    this.attachmentUrls = attachmentUrls;
  }

}
