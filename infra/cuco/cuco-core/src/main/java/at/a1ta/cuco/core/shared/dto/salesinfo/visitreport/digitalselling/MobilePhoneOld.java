package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class MobilePhoneOld extends MobilePhoneBase {

  private boolean partPayment; // Teilzahlung
  private BigDecimal partPaymentPrice;

  private boolean mobilePhoneInsurance; // Handyversicherung
  private BigDecimal mobilePhoneInsurancePrice;

  private boolean cyberProtection; // Cyberschutz
  private BigDecimal cyberProtectionPrice;

  private boolean creditCard; // Kreditkarte
  private BigDecimal creditCardPrice;

  private boolean videoStreaming; // Videostreaming
  private BigDecimal videoStreamingPrice;

  private boolean musicStreaming; // Musikstreaming
  private BigDecimal musicStreamingPrice;

  private boolean upgradePackage; // Sonstige Pakete
  private BigDecimal upgradePackagePrice;

  private String advantageText; // Vorteile
  private String disadvantageText; // Nachteile

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

  public boolean isMobilePhoneInsurance() {
    return mobilePhoneInsurance;
  }

  public void setMobilePhoneInsurance(boolean mobilePhoneInsurance) {
    this.mobilePhoneInsurance = mobilePhoneInsurance;
  }

  public BigDecimal getMobilePhoneInsurancePrice() {
    return mobilePhoneInsurancePrice;
  }

  public void setMobilePhoneInsurancePrice(BigDecimal mobilePhoneInsurancePrice) {
    this.mobilePhoneInsurancePrice = mobilePhoneInsurancePrice;
  }

  public boolean isCyberProtection() {
    return cyberProtection;
  }

  public void setCyberProtection(boolean cyberProtection) {
    this.cyberProtection = cyberProtection;
  }

  public BigDecimal getCyberProtectionPrice() {
    return cyberProtectionPrice;
  }

  public void setCyberProtectionPrice(BigDecimal cyberProtectionPrice) {
    this.cyberProtectionPrice = cyberProtectionPrice;
  }

  public boolean isCreditCard() {
    return creditCard;
  }

  public void setCreditCard(boolean creditCard) {
    this.creditCard = creditCard;
  }

  public BigDecimal getCreditCardPrice() {
    return creditCardPrice;
  }

  public void setCreditCardPrice(BigDecimal creditCardPrice) {
    this.creditCardPrice = creditCardPrice;
  }

  public boolean isVideoStreaming() {
    return videoStreaming;
  }

  public void setVideoStreaming(boolean videoStreaming) {
    this.videoStreaming = videoStreaming;
  }

  public BigDecimal getVideoStreamingPrice() {
    return videoStreamingPrice;
  }

  public void setVideoStreamingPrice(BigDecimal videoStreamingPrice) {
    this.videoStreamingPrice = videoStreamingPrice;
  }

  public boolean isMusicStreaming() {
    return musicStreaming;
  }

  public void setMusicStreaming(boolean musicStreaming) {
    this.musicStreaming = musicStreaming;
  }

  public BigDecimal getMusicStreamingPrice() {
    return musicStreamingPrice;
  }

  public void setMusicStreamingPrice(BigDecimal musicStreamingPrice) {
    this.musicStreamingPrice = musicStreamingPrice;
  }

  public boolean isUpgradePackage() {
    return upgradePackage;
  }

  public void setUpgradePackage(boolean upgradePackage) {
    this.upgradePackage = upgradePackage;
  }

  public BigDecimal getUpgradePackagePrice() {
    return upgradePackagePrice;
  }

  public void setUpgradePackagePrice(BigDecimal upgradePackagePrice) {
    this.upgradePackagePrice = upgradePackagePrice;
  }

  public String getAdvantageText() {
    return advantageText;
  }

  public void setAdvantageText(String advantageText) {
    this.advantageText = advantageText;
  }

  public String getDisadvantageText() {
    return disadvantageText;
  }

  public void setDisadvantageText(String disadvantageText) {
    this.disadvantageText = disadvantageText;
  }

  @Override
  public String toString() {
    return "MobilePhoneOld [partPayment=" + partPayment + ", partPaymentPrice=" + partPaymentPrice + ", mobilePhoneInsurance=" + mobilePhoneInsurance + ", mobilePhoneInsurancePrice="
        + mobilePhoneInsurancePrice + ", cyberProtection=" + cyberProtection + ", cyberProtectionPrice=" + cyberProtectionPrice + ", creditCard=" + creditCard + ", creditCardPrice=" + creditCardPrice
        + ", videoStreaming=" + videoStreaming + ", videoStreamingPrice=" + videoStreamingPrice + ", musicStreaming=" + musicStreaming + ", musicStreamingPrice=" + musicStreamingPrice
        + ", upgradePackage=" + upgradePackage + ", upgradePackagePrice=" + upgradePackagePrice + ", advantageText=" + advantageText + ", disadvantageText=" + disadvantageText + "]";
  }

}
