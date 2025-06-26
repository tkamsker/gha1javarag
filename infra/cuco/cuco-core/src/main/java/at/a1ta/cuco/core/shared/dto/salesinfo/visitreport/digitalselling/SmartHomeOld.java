package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class SmartHomeOld extends SmartHomeBase {
  private boolean smartSolution;
  private BigDecimal smartSolutionPrice;
  private String smartSolutionText;

  private boolean alarmSystem;
  private BigDecimal alarmSystemPrice;
  private String alarmSystemText;

  private String smartProductText;
  private boolean googleNest;

  public boolean isSmartSolution() {
    return smartSolution;
  }

  public void setSmartSolution(boolean smartSolution) {
    this.smartSolution = smartSolution;
  }

  public BigDecimal getSmartSolutionPrice() {
    return smartSolutionPrice;
  }

  public void setSmartSolutionPrice(BigDecimal smartSolutionPrice) {
    this.smartSolutionPrice = smartSolutionPrice;
  }

  public String getSmartSolutionText() {
    return smartSolutionText;
  }

  public void setSmartSolutionText(String smartSolutionText) {
    this.smartSolutionText = smartSolutionText;
  }

  public boolean isAlarmSystem() {
    return alarmSystem;
  }

  public void setAlarmSystem(boolean alarmSystem) {
    this.alarmSystem = alarmSystem;
  }

  public BigDecimal getAlarmSystemPrice() {
    return alarmSystemPrice;
  }

  public void setAlarmSystemPrice(BigDecimal alarmSystemPrice) {
    this.alarmSystemPrice = alarmSystemPrice;
  }

  public String getAlarmSystemText() {
    return alarmSystemText;
  }

  public void setAlarmSystemText(String alarmSystemText) {
    this.alarmSystemText = alarmSystemText;
  }

  public String getSmartProductText() {
    return smartProductText;
  }

  public void setSmartProductText(String smartProductText) {
    this.smartProductText = smartProductText;
  }

  public boolean isGoogleNest() {
    return googleNest;
  }

  public void setGoogleNest(boolean googleNest) {
    this.googleNest = googleNest;
  }

  @Override
  public String toString() {
    return "SmartHomeOld [smartSolution=" + smartSolution + ", smartSolutionPrice=" + smartSolutionPrice + ", smartSolutionText=" + smartSolutionText + ", alarmSystem=" + alarmSystem
        + ", alarmSystemPrice=" + alarmSystemPrice + ", alarmSystemText=" + alarmSystemText + ", smartProductText=" + smartProductText + ", googleNest=" + googleNest + "]";
  }

}
