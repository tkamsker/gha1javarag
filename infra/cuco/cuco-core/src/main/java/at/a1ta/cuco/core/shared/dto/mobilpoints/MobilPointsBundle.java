package at.a1ta.cuco.core.shared.dto.mobilpoints;

import java.io.Serializable;

public class MobilPointsBundle implements Serializable {
  private String phoneNumber;
  private MobilPoints mobilPoints;
  private BusinessHardwareReplacement businessHardwareReplacement;

  public String getPhoneNumber() {
    return phoneNumber;
  }

  public void setPhoneNumber(String phoneNumber) {
    this.phoneNumber = phoneNumber;
  }

  public MobilPoints getMobilPoints() {
    return mobilPoints;
  }

  public void setMobilPoints(MobilPoints mobilPoints) {
    this.mobilPoints = mobilPoints;
  }

  public BusinessHardwareReplacement getBusinessHardwareReplacement() {
    return businessHardwareReplacement;
  }

  public void setBusinessHardwareReplacement(BusinessHardwareReplacement businessHardwareReplacement) {
    this.businessHardwareReplacement = businessHardwareReplacement;
  }

}
