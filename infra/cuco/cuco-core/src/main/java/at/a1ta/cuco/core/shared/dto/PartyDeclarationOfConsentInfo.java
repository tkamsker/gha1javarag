package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class PartyDeclarationOfConsentInfo implements Serializable {

  public enum StatusOfCompleteness {
    COMPLETE("Grün"), NONE("Rot"), PARTIAL("Gelb"), UNKNOWN("Unbekannt");

    private String displayText;

    private StatusOfCompleteness(String name) {
      this.displayText = name;
    }

    public String getDisplayText() {
      return displayText;
    }
  };

  public enum StatusNeedForAction {
    COMPLETE("Grün"), NONE("Rot"), PARTIAL("Gelb"), UNKNOWN("Unbekannt");

    private String displayText;

    private StatusNeedForAction(String name) {
      this.displayText = name;
    }

    public String getDisplayText() {
      return displayText;
    }
  };

  private static final long serialVersionUID = 1L;
  private int staus = LOADING;
  private String declarationOfConsentDefinitionVersion;
  private String declarationOfConsentId;
  private StatusOfCompleteness statusOfCompleteness = StatusOfCompleteness.UNKNOWN;
  private StatusNeedForAction statusNeedForAction = StatusNeedForAction.UNKNOWN;

  public static final int ERROR = 99;
  public static final int LOADING = -1;
  public static final int NOT_RECEIVED = 98;
  public static final int LOADED = 0;

  public PartyDeclarationOfConsentInfo() {}

  public PartyDeclarationOfConsentInfo(int staus, StatusOfCompleteness statusOfCompleteness) {
    this.staus = staus;
    this.statusOfCompleteness = statusOfCompleteness;
  }

  public int getStaus() {
    return staus;
  }

  public void setStaus(int staus) {
    this.staus = staus;
  }

  public String getDeclarationOfConsentDefinitionVersion() {
    return declarationOfConsentDefinitionVersion;
  }

  public void setDeclarationOfConsentDefinitionVersion(String declarationOfConsentDefinitionVersion) {
    this.declarationOfConsentDefinitionVersion = declarationOfConsentDefinitionVersion;
  }

  public String getDeclarationOfConsentId() {
    return declarationOfConsentId;
  }

  public void setDeclarationOfConsentId(String declarationOfConsentId) {
    this.declarationOfConsentId = declarationOfConsentId;
  }

  public StatusOfCompleteness getStatusOfCompleteness() {
    return statusOfCompleteness;
  }

  public void setStatusOfCompleteness(StatusOfCompleteness statusOfCompleteness) {
    this.statusOfCompleteness = statusOfCompleteness;
  }

  public StatusNeedForAction getStatusNeedForAction() {
    return statusNeedForAction;
  }

  public void setStatusNeedForAction(StatusNeedForAction statusNeedForAction) {
    this.statusNeedForAction = statusNeedForAction;
  }

}
