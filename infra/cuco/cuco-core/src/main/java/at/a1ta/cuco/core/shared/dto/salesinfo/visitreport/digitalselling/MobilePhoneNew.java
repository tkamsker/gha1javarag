package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class MobilePhoneNew extends MobilePhoneBase {
  private boolean partPayment; // Teilzahlung
  private BigDecimal partPaymentPrice;

  private boolean a1MobilePhoneInsurance; // A1 Handyversicherung
  private BigDecimal a1MobilePhoneInsurancePrice;

  private boolean a1CyberProtection; // A1 Cyberschutz
  private BigDecimal a1CyberProtectionPrice;

  private boolean a1Mastercard; // A1 Mastercard
  private BigDecimal a1MastercardPrice;

  private boolean a1XploreTvStreaming; // A1 Xplore TV Streaming
  private BigDecimal a1XploreTvStreamingPrice;

  private boolean a1XploreMusic; // A1 Xplore Music
  private BigDecimal a1XploreMusicPrice;

  private boolean a1UpgradePackage; // A1 Upgrade Paket
  private BigDecimal a1UpgradePackagePrice;

  private String optionValue;

  public boolean isPartPayment() {
    return partPayment;
  }

  public void setPartPayment(boolean partPayment) {
    this.partPayment = partPayment;
  }

  public BigDecimal getPartPaymentPrice() {
    return partPaymentPrice;
  }

  public void setPartPaymentPrice(BigDecimal partPaymentPrice) {
    this.partPaymentPrice = partPaymentPrice;
  }

  public boolean isA1MobilePhoneInsurance() {
    return a1MobilePhoneInsurance;
  }

  public void setA1MobilePhoneInsurance(boolean a1MobilePhoneInsurance) {
    this.a1MobilePhoneInsurance = a1MobilePhoneInsurance;
  }

  public BigDecimal getA1MobilePhoneInsurancePrice() {
    return a1MobilePhoneInsurancePrice;
  }

  public void setA1MobilePhoneInsurancePrice(BigDecimal a1MobilePhoneInsurancePrice) {
    this.a1MobilePhoneInsurancePrice = a1MobilePhoneInsurancePrice;
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

  public boolean isA1XploreMusic() {
    return a1XploreMusic;
  }

  public void setA1XploreMusic(boolean a1XploreMusic) {
    this.a1XploreMusic = a1XploreMusic;
  }

  public BigDecimal getA1XploreMusicPrice() {
    return a1XploreMusicPrice;
  }

  public void setA1XploreMusicPrice(BigDecimal a1XploreMusicPrice) {
    this.a1XploreMusicPrice = a1XploreMusicPrice;
  }

  public boolean isA1UpgradePackage() {
    return a1UpgradePackage;
  }

  public void setA1UpgradePackage(boolean a1UpgradePackage) {
    this.a1UpgradePackage = a1UpgradePackage;
  }

  public BigDecimal getA1UpgradePackagePrice() {
    return a1UpgradePackagePrice;
  }

  public void setA1UpgradePackagePrice(BigDecimal a1UpgradePackagePrice) {
    this.a1UpgradePackagePrice = a1UpgradePackagePrice;
  }

  public String getOptionValue() {
    return optionValue;
  }

  public void setOptionValue(String optionValue) {
    this.optionValue = optionValue;
  }

  @Override
  public String toString() {
    return "MobilePhoneNew [partPayment=" + partPayment + ", partPaymentPrice=" + partPaymentPrice + ", a1MobilePhoneInsurance=" + a1MobilePhoneInsurance + ", a1MobilePhoneInsurancePrice="
        + a1MobilePhoneInsurancePrice + ", a1CyberProtection=" + a1CyberProtection + ", a1CyberProtectionPrice=" + a1CyberProtectionPrice + ", a1Mastercard=" + a1Mastercard + ", a1MastercardPrice="
        + a1MastercardPrice + ", a1XploreTvStreaming=" + a1XploreTvStreaming + ", a1XploreTvStreamingPrice=" + a1XploreTvStreamingPrice + ", a1XploreMusic=" + a1XploreMusic + ", a1XploreMusicPrice="
        + a1XploreMusicPrice + ", a1UpgradePackage=" + a1UpgradePackage + ", a1UpgradePackagePrice=" + a1UpgradePackagePrice + ", optionValue=" + optionValue + "]";
  }

}
