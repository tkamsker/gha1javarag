package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class MobileTariffBase implements Serializable {
  private static final long serialVersionUID = 1L;

  private String minutesValue; // Minuten
  private String smsMmsValue; // SMS/MMS
  private String dataVolumeValue; // Datenvolumen
  private String internetSpeedValue; // Internetspeed
  private String roamingOutsideEUValue; // Roaming außer EU
  private String foreignCountryMinutesValue; // Auslandsminuten

  private String comment;

  private BigDecimal sum;

  public String getMinutesValue() {
    return minutesValue;
  }

  public void setMinutesValue(String minutesValue) {
    this.minutesValue = minutesValue;
  }

  public String getSmsMmsValue() {
    return smsMmsValue;
  }

  public void setSmsMmsValue(String smsMmsValue) {
    this.smsMmsValue = smsMmsValue;
  }

  public String getDataVolumeValue() {
    return dataVolumeValue;
  }

  public void setDataVolumeValue(String dataVolumeValue) {
    this.dataVolumeValue = dataVolumeValue;
  }

  public String getInternetSpeedValue() {
    return internetSpeedValue;
  }

  public void setInternetSpeedValue(String internetSpeedValue) {
    this.internetSpeedValue = internetSpeedValue;
  }

  public String getRoamingOutsideEUValue() {
    return roamingOutsideEUValue;
  }

  public void setRoamingOutsideEUValue(String roamingOutsideEUValue) {
    this.roamingOutsideEUValue = roamingOutsideEUValue;
  }

  public String getForeignCountryMinutesValue() {
    return foreignCountryMinutesValue;
  }

  public void setForeignCountryMinutesValue(String foreignCountryMinutesValue) {
    this.foreignCountryMinutesValue = foreignCountryMinutesValue;
  }

  public String getComment() {
    return comment;
  }

  public void setComment(String comment) {
    this.comment = comment;
  }

  public BigDecimal getSum() {
    return sum;
  }

  public void setSum(BigDecimal sum) {
    this.sum = sum;
  }

  @Override
  public String toString() {
    return "MobileTariffBase [minutesValue=" + minutesValue + ", smsMmsValue=" + smsMmsValue + ", dataVolumeValue=" + dataVolumeValue + ", internetSpeedValue=" + internetSpeedValue
        + ", roamingOutsideEUValue=" + roamingOutsideEUValue + ", foreignCountryMinutesValue=" + foreignCountryMinutesValue + ", comment=" + comment + ", sum=" + sum + "]";
  }

}
