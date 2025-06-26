package at.a1ta.cuco.core.shared.dto.mobilpoints;

import java.io.Serializable;

import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;

public class MobilPoints implements Serializable {
  private long amdocsPoints;
  private long partnerWebPoints;
  private long clarifyPoints;
  private PhoneNumberStructure number;

  public long getAmdocsPoints() {
    return amdocsPoints;
  }

  public void setAmdocsPoints(long amdocsPoints) {
    this.amdocsPoints = amdocsPoints;
  }

  public long getPartnerWebPoints() {
    return partnerWebPoints;
  }

  public void setPartnerWebPoints(long partnerWebPoints) {
    this.partnerWebPoints = partnerWebPoints;
  }

  public long getClarifyPoints() {
    return clarifyPoints;
  }

  public void setClarifyPoints(long clarifyPoints) {
    this.clarifyPoints = clarifyPoints;
  }

  public long getPendingMobilPoints() {
    return partnerWebPoints + clarifyPoints;
  }

  public PhoneNumberStructure getNumber() {
    return number;
  }

  public void setNumber(PhoneNumberStructure number) {
    this.number = number;
  }
}
