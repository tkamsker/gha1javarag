package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class InternetSpeedNew extends InternetSpeedBase {
  private String productName;

  private boolean a1InternetProtection; // Internetschutz
  private BigDecimal a1InternetProtectionPrice;

  private boolean a1InternetPowerPlus; // Internet Power Plus
  private BigDecimal a1InternetPowerPlusPrice;

  private boolean a1CyberProtection; // Cyberschutz
  private BigDecimal a1CyberProtectionPrice;

  private boolean a1MobileWarranty; // Handygarantie
  private BigDecimal a1MobileWarrantyPrice;

  private boolean a1Mastercard; // Mastercard
  private BigDecimal a1MastercardPrice;

  private boolean a1XploreTvStreaming; // Xplore TV Streaming
  private BigDecimal a1XploreTvStreamingPrice;

  private boolean a1PLC;
  private BigDecimal a1PLCPrice;

  private boolean a1Mesh;
  private BigDecimal a1MeshPrice;

  private boolean connectPlus;

  public String getProductName() {
    return productName;
  }

  public void setProductName(String productName) {
    this.productName = productName;
  }

  public boolean isA1InternetProtection() {
    return a1InternetProtection;
  }

  public void setA1InternetProtection(boolean a1InternetProtection) {
    this.a1InternetProtection = a1InternetProtection;
  }

  public BigDecimal getA1InternetProtectionPrice() {
    return a1InternetProtectionPrice;
  }

  public void setA1InternetProtectionPrice(BigDecimal a1InternetProtectionPrice) {
    this.a1InternetProtectionPrice = a1InternetProtectionPrice;
  }

  public boolean isA1InternetPowerPlus() {
    return a1InternetPowerPlus;
  }

  public void setA1InternetPowerPlus(boolean a1InternetPowerPlus) {
    this.a1InternetPowerPlus = a1InternetPowerPlus;
  }

  public BigDecimal getA1InternetPowerPlusPrice() {
    return a1InternetPowerPlusPrice;
  }

  public void setA1InternetPowerPlusPrice(BigDecimal a1InternetPowerPlusPrice) {
    this.a1InternetPowerPlusPrice = a1InternetPowerPlusPrice;
  }

  public boolean isA1CyberProtection() {
    return a1CyberProtection;
  }

  public void setA1CyberProtection(boolean a1CyberProtection) {
    this.a1CyberProtection = a1CyberProtection;
  }

  public BigDecimal getA1CyberProtectionPrice() {
    return a1CyberProtectionPrice;
  }

  public void setA1CyberProtectionPrice(BigDecimal a1CyberProtectionPrice) {
    this.a1CyberProtectionPrice = a1CyberProtectionPrice;
  }

  public boolean isA1MobileWarranty() {
    return a1MobileWarranty;
  }

  public void setA1MobileWarranty(boolean a1MobileWarranty) {
    this.a1MobileWarranty = a1MobileWarranty;
  }

  public BigDecimal getA1MobileWarrantyPrice() {
    return a1MobileWarrantyPrice;
  }

  public void setA1MobileWarrantyPrice(BigDecimal a1MobileWarrantyPrice) {
    this.a1MobileWarrantyPrice = a1MobileWarrantyPrice;
  }

  public boolean isA1Mastercard() {
    return a1Mastercard;
  }

  public void setA1Mastercard(boolean a1Mastercard) {
    this.a1Mastercard = a1Mastercard;
  }

  public BigDecimal getA1MastercardPrice() {
    return a1MastercardPrice;
  }

  public void setA1MastercardPrice(BigDecimal a1MastercardPrice) {
    this.a1MastercardPrice = a1MastercardPrice;
  }

  public boolean isA1XploreTvStreaming() {
    return a1XploreTvStreaming;
  }

  public void setA1XploreTvStreaming(boolean a1XploreTvStreaming) {
    this.a1XploreTvStreaming = a1XploreTvStreaming;
  }

  public BigDecimal getA1XploreTvStreamingPrice() {
    return a1XploreTvStreamingPrice;
  }

  public void setA1XploreTvStreamingPrice(BigDecimal a1XploreTvStreamingPrice) {
    this.a1XploreTvStreamingPrice = a1XploreTvStreamingPrice;
  }

  public boolean isA1PLC() {
    return a1PLC;
  }

  public void setA1PLC(boolean a1plc) {
    a1PLC = a1plc;
  }

  public BigDecimal getA1PLCPrice() {
    return a1PLCPrice;
  }

  public void setA1PLCPrice(BigDecimal a1plcPrice) {
    a1PLCPrice = a1plcPrice;
  }

  public boolean isA1Mesh() {
    return a1Mesh;
  }

  public void setA1Mesh(boolean a1Mesh) {
    this.a1Mesh = a1Mesh;
  }

  public BigDecimal getA1MeshPrice() {
    return a1MeshPrice;
  }

  public void setA1MeshPrice(BigDecimal a1MeshPrice) {
    this.a1MeshPrice = a1MeshPrice;
  }

  public boolean isConnectPlus() {
    return connectPlus;
  }

  public void setConnectPlus(boolean connectPlus) {
    this.connectPlus = connectPlus;
  }

  @Override
  public String toString() {
    return "InternetSpeedNew [productName=" + productName + ", a1InternetProtection=" + a1InternetProtection + ", a1InternetProtectionPrice=" + a1InternetProtectionPrice + ", a1InternetPowerPlus="
        + a1InternetPowerPlus + ", a1InternetPowerPlusPrice=" + a1InternetPowerPlusPrice + ", a1CyberProtection=" + a1CyberProtection + ", a1CyberProtectionPrice=" + a1CyberProtectionPrice
        + ", a1MobileWarranty=" + a1MobileWarranty + ", a1MobileWarrantyPrice=" + a1MobileWarrantyPrice + ", a1Mastercard=" + a1Mastercard + ", a1MastercardPrice=" + a1MastercardPrice
        + ", a1XploreTvStreaming=" + a1XploreTvStreaming + ", a1XploreTvStreamingPrice=" + a1XploreTvStreamingPrice + ", a1PLC=" + a1PLC + ", a1PLCPrice=" + a1PLCPrice + ", a1Mesh=" + a1Mesh
        + ", a1MeshPrice=" + a1MeshPrice + ", connectPlus=" + connectPlus + "]";
  }
}
