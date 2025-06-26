package at.a1ta.cuco.core.shared.dto;

import java.math.BigInteger;

public class PartnerCenterAccessTokenRequest extends AccessTokenRequest {

  public PartnerCenterAccessTokenRequest() {
    super();
  }

  public PartnerCenterAccessTokenRequest(String targetSystem, String sourceSystem) {
    super(targetSystem, sourceSystem);
  }

  public void setCountryCode(String countryCode) {
    this.addParameter("cc", countryCode);
  }

  public void setNationalDestinationCode(String nationalDesitnationCode) {
    this.addParameter("ndc", nationalDesitnationCode);
  }

  public void setSubscriberNumber(String subscriberNumber) {
    this.addParameter("sn", subscriberNumber);
  }

  public String setProcessId(String processId) {
    return addParameter("processId", processId);
  }

  public String getCountryCode() {
    return getParameter("cc");
  }

  public String getNationalDesitnationCode() {
    return getParameter("ndc");
  }

  public String getSubscriberNumber() {
    return getParameter("sn");
  }

  public String getProcessId() {
    return getParameter("processId");
  }

  public int getCountryCodeAsInt() {
    return Integer.parseInt(getCountryCode());
  }

  public int getNationalDestinationCodeAsInt() {
    return Integer.parseInt(getNationalDesitnationCode());
  }

  public BigInteger getSubscriberNumberAsInt() {
    return BigInteger.valueOf(Long.valueOf(getSubscriberNumber()));
  }

  @Override
  public String toString() {
    return "PartnerCenterAccessTokenRequest [countryCode=" + getCountryCode() + ", nationalDesitnationCode=" + getNationalDesitnationCode()
        + ", subscriberNumber=" + getSubscriberNumber() + ", processId=" + getProcessId() + ", targetSystem=" + getTargetSystem()
        + ", sourceSystem=" + getSourceSystem() + "]";
  }

}
