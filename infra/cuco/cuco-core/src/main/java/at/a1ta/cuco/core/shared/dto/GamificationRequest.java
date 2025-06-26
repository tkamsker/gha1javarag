package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class GamificationRequest implements Serializable {

  /**
   * 
   */
  private static final long serialVersionUID = 1L;

  private String agentId;

  private int limit;

  private String contentType;

  private String apiKey;

  private String queryString;

  public int getLimit() {
    return limit;
  }

  public void setLimit(int limit) {
    this.limit = limit;
  }

  public String getAgentId() {
    return agentId;
  }

  public void setAgentId(String agentId) {
    this.agentId = agentId;
  }

  public String getContentType() {
    return contentType;
  }

  public void setContentType(String contentType) {
    this.contentType = contentType;
  }

  public String getApiKey() {
    return apiKey;
  }

  public void setApiKey(String apiKey) {
    this.apiKey = apiKey;
  }

  public String getQueryString() {
    return queryString;
  }

  public void setQueryString(String queryString) {
    this.queryString = queryString;
  }

}
