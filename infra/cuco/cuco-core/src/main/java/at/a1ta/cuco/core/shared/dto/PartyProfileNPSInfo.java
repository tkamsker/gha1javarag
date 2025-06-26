package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class PartyProfileNPSInfo implements Serializable {

  private static final long serialVersionUID = 1L;

  private String scoringType;
  private String scoringValue;
  private String scoringDate;

  public PartyProfileNPSInfo() {
    // default constructor to support GWT parsing
  }

  public PartyProfileNPSInfo(String scoringType, String scoringValue, String scoringDate) {

    this.scoringType = scoringType;
    this.scoringValue = scoringValue;
    this.scoringDate = scoringDate;
  }

  public String getScoringType() {
    return scoringType;
  }

  public void setScoringType(String scoringType) {
    this.scoringType = scoringType;
  }

  public String getScoringValue() {
    return scoringValue;
  }

  public void setScoringValue(String scoringValue) {
    this.scoringValue = scoringValue;
  }

  public String getScoringDate() {
    return scoringDate;
  }

  public void setScoringDate(String scoringDate) {
    this.scoringDate = scoringDate;
  }

  public String getStringTypeReadable() {
    if (getScoringType().equals("PA_TNPSVALUE")) {
      return "TNPS";
    } else if (getScoringType().equals("PA_PNPSVALUE")) {
      return "PNPS";
    } else if (getScoringType().equals("PA_RNPSVALUE")) {
      return "rNPS";
    }
    return "";
  }

  public String getCompleteNpsStatus() {
    return getStringTypeReadable() + ": " + getScoringValue() + " - " + getScoringDate().toString();
  }
}
