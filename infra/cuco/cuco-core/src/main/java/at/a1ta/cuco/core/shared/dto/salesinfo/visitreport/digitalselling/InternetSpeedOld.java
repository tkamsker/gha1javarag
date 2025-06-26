package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class InternetSpeedOld extends InternetSpeedBase {
  private boolean virusProtection; // Virenschutz
  private BigDecimal virusProtectionPrice;

  private boolean mobilityFeature; // Mobilitaetsfunktion
  private BigDecimal mobilityFeaturePrice;

  private boolean cyberProtection; // Cyberschutz
  private BigDecimal cyberProtectionPrice;

  private boolean homeNetwork;
  private String homeNetworkValue;
  private boolean verbundPowerOffer;

  public boolean isVirusProtection() {
    return virusProtection;
  }

  public void setVirusProtection(boolean virusProtection) {
    this.virusProtection = virusProtection;
  }

  public BigDecimal getVirusProtectionPrice() {
    return virusProtectionPrice;
  }

  public void setVirusProtectionPrice(BigDecimal virusProtectionPrice) {
    this.virusProtectionPrice = virusProtectionPrice;
  }

  public boolean isMobilityFeature() {
    return mobilityFeature;
  }

  public void setMobilityFeature(boolean mobilityFeature) {
    this.mobilityFeature = mobilityFeature;
  }

  public BigDecimal getMobilityFeaturePrice() {
    return mobilityFeaturePrice;
  }

  public void setMobilityFeaturePrice(BigDecimal mobilityFeaturePrice) {
    this.mobilityFeaturePrice = mobilityFeaturePrice;
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

  public boolean isHomeNetwork() {
    return homeNetwork;
  }

  public void setHomeNetwork(boolean homeNetwork) {
    this.homeNetwork = homeNetwork;
  }

  public String getHomeNetworkValue() {
    return homeNetworkValue;
  }

  public void setHomeNetworkValue(String homeNetworkValue) {
    this.homeNetworkValue = homeNetworkValue;
  }

  public boolean isVerbundPowerOffer() {
    return verbundPowerOffer;
  }

  public void setVerbundPowerOffer(boolean verbundPowerOffer) {
    this.verbundPowerOffer = verbundPowerOffer;
  }

  @Override
  public String toString() {
    return "InternetSpeedOld [virusProtection=" + virusProtection + ", virusProtectionPrice=" + virusProtectionPrice + ", mobilityFeature=" + mobilityFeature + ", mobilityFeaturePrice="
        + mobilityFeaturePrice + ", cyberProtection=" + cyberProtection + ", cyberProtectionPrice=" + cyberProtectionPrice + ", homeNetwork=" + homeNetwork + ", homeNetworkValue=" + homeNetworkValue
        + ", verbundPowerOffer=" + verbundPowerOffer + "]";
  }

}
