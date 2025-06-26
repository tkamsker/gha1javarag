package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class SmartHomeNew extends SmartHomeBase {

  private boolean smartHomeTariff;
  private BigDecimal smartHomeTariffPrice;
  private String smartHomeTariffText;

  private boolean securitySolution;
  private BigDecimal securitySolutionPrice;
  private String securitySolutionText;

  private boolean indoorCamera;
  private BigDecimal indoorCameraPrice;

  private boolean multiSensor;
  private BigDecimal multiSensorPrice;

  private boolean bulb;
  private BigDecimal bulbPrice;

  private boolean socket;
  private BigDecimal socketPrice;

  private boolean outdoorCamera;

  private boolean nukiCombo;
  private BigDecimal nukiComboPrice;

  public boolean isSmartHomeTariff() {
    return smartHomeTariff;
  }

  public void setSmartHomeTariff(boolean smartHomeTariff) {
    this.smartHomeTariff = smartHomeTariff;
  }

  public BigDecimal getSmartHomeTariffPrice() {
    return smartHomeTariffPrice;
  }

  public void setSmartHomeTariffPrice(BigDecimal smartHomeTariffPrice) {
    this.smartHomeTariffPrice = smartHomeTariffPrice;
  }

  public String getSmartHomeTariffText() {
    return smartHomeTariffText;
  }

  public void setSmartHomeTariffText(String smartHomeTariffText) {
    this.smartHomeTariffText = smartHomeTariffText;
  }

  public boolean isSecuritySolution() {
    return securitySolution;
  }

  public void setSecuritySolution(boolean securitySolution) {
    this.securitySolution = securitySolution;
  }

  public BigDecimal getSecuritySolutionPrice() {
    return securitySolutionPrice;
  }

  public void setSecuritySolutionPrice(BigDecimal securitySolutionPrice) {
    this.securitySolutionPrice = securitySolutionPrice;
  }

  public String getSecuritySolutionText() {
    return securitySolutionText;
  }

  public void setSecuritySolutionText(String securitySolutionText) {
    this.securitySolutionText = securitySolutionText;
  }

  public boolean isIndoorCamera() {
    return indoorCamera;
  }

  public void setIndoorCamera(boolean indoorCamera) {
    this.indoorCamera = indoorCamera;
  }

  public BigDecimal getIndoorCameraPrice() {
    return indoorCameraPrice;
  }

  public void setIndoorCameraPrice(BigDecimal indoorCameraPrice) {
    this.indoorCameraPrice = indoorCameraPrice;
  }

  public boolean isMultiSensor() {
    return multiSensor;
  }

  public void setMultiSensor(boolean multiSensor) {
    this.multiSensor = multiSensor;
  }

  public BigDecimal getMultiSensorPrice() {
    return multiSensorPrice;
  }

  public void setMultiSensorPrice(BigDecimal multiSensorPrice) {
    this.multiSensorPrice = multiSensorPrice;
  }

  public boolean isBulb() {
    return bulb;
  }

  public void setBulb(boolean bulb) {
    this.bulb = bulb;
  }

  public BigDecimal getBulbPrice() {
    return bulbPrice;
  }

  public void setBulbPrice(BigDecimal bulbPrice) {
    this.bulbPrice = bulbPrice;
  }

  public boolean isSocket() {
    return socket;
  }

  public void setSocket(boolean socket) {
    this.socket = socket;
  }

  public BigDecimal getSocketPrice() {
    return socketPrice;
  }

  public void setSocketPrice(BigDecimal socketPrice) {
    this.socketPrice = socketPrice;
  }

  public boolean isOutdoorCamera() {
    return outdoorCamera;
  }

  public void setOutdoorCamera(boolean outdoorCamera) {
    this.outdoorCamera = outdoorCamera;
  }

  public boolean isNukiCombo() {
    return nukiCombo;
  }

  public void setNukiCombo(boolean nukiCombo) {
    this.nukiCombo = nukiCombo;
  }

  public BigDecimal getNukiComboPrice() {
    return nukiComboPrice;
  }

  public void setNukiComboPrice(BigDecimal nukiComboPrice) {
    this.nukiComboPrice = nukiComboPrice;
  }

  @Override
  public String toString() {
    return "SmartHomeNew [smartHomeTariff=" + smartHomeTariff + ", smartHomeTariffPrice=" + smartHomeTariffPrice + ", smartHomeTariffText=" + smartHomeTariffText + ", securitySolution="
        + securitySolution + ", securitySolutionPrice=" + securitySolutionPrice + ", securitySolutionText=" + securitySolutionText + ", indoorCamera=" + indoorCamera + ", indoorCameraPrice="
        + indoorCameraPrice + ", multiSensor=" + multiSensor + ", multiSensorPrice=" + multiSensorPrice + ", bulb=" + bulb + ", bulbPrice=" + bulbPrice + ", socket=" + socket + ", socketPrice="
        + socketPrice + ", outdoorCamera=" + outdoorCamera + ", nukiCombo=" + nukiCombo + ", nukiComboPrice=" + nukiComboPrice + "]";
  }

}
