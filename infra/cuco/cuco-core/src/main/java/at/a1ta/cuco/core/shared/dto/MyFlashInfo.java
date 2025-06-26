package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class MyFlashInfo extends FlashInfo implements Serializable {

  private Long partyId;
  private String creatorName;

  public Long getPartyId() {
    return partyId;
  }

  public void setPartyId(Long partyId) {
    this.partyId = partyId;
  }

  public String getCreatorName() {
    return creatorName;
  }

  public void setCreatorName(String creatorName) {
    this.creatorName = creatorName;
  }

}
