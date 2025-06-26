package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class MobileTariffNew extends MobileTariffBase {
  private static final long serialVersionUID = 1L;

  private String tariffValue;
  private BigDecimal tariffPrice;

  private String featureNutzenBoxValue;

  private String tariffOptionValue;
  private BigDecimal tariffOptionPrice;

  private boolean internetProtection; // Internetschutz
  private BigDecimal internetProtectionPrice;

  private boolean cyberProtection; // Cyberschutz
  private BigDecimal cyberProtectionPrice;

  private boolean a1Mastercard; // A1 Mastercard;
  private BigDecimal a1MastercardPrice;

  private boolean a1XploreTvStreaming; // A1 Xplore TV Streaming
  private BigDecimal a1XploreTvStreamingPrice;

  private boolean a1XploreMusic; // A1 Xplore Music
  private BigDecimal a1XploreMusicPrice;

  private boolean additionSim; // Zusatz SIM
  private BigDecimal additionSimPrice;

  private String optionValue;
  private BigDecimal optionPrice;

  private BigDecimal freeStreaming;
  private BigDecimal connectPlusDiscount;
  private BigDecimal connectPlusBonus;

  public String getTariffValue() {
    return tariffValue;
  }

  public void setTariffValue(String tariffValue) {
    this.tariffValue = tariffValue;
  }

  public BigDecimal getTariffPrice() {
    return tariffPrice;
  }

  public void setTariffPrice(BigDecimal tariffPrice) {
    this.tariffPrice = tariffPrice;
  }

  public String getFeatureNutzenBoxValue() {
    return featureNutzenBoxValue;
  }

  public void setFeatureNutzenBoxValue(String featureNutzenBoxValue) {
    this.featureNutzenBoxValue = featureNutzenBoxValue;
  }

  public String getTariffOptionValue() {
    return tariffOptionValue;
  }

  public void setTariffOptionValue(String tariffOptionValue) {
    this.tariffOptionValue = tariffOptionValue;
  }

  public BigDecimal getTariffOptionPrice() {
    return tariffOptionPrice;
  }

  public void setTariffOptionPrice(BigDecimal tariffOptionPrice) {
    this.tariffOptionPrice = tariffOptionPrice;
  }

  public boolean isInternetProtection() {
    return internetProtection;
  }

  public void setInternetProtection(boolean internetProtection) {
    this.internetProtection = internetProtection;
  }

  public BigDecimal getInternetProtectionPrice() {
    return internetProtectionPrice;
  }

  public void setInternetProtectionPrice(BigDecimal internetProtectionPrice) {
    this.internetProtectionPrice = internetProtectionPrice;
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

  public boolean isAdditionSim() {
    return additionSim;
  }

  public void setAdditionSim(boolean additionSim) {
    this.additionSim = additionSim;
  }

  public BigDecimal getAdditionSimPrice() {
    return additionSimPrice;
  }

  public void setAdditionSimPrice(BigDecimal additionSimPrice) {
    this.additionSimPrice = additionSimPrice;
  }

  public String getOptionValue() {
    return optionValue;
  }

  public void setOptionValue(String optionValue) {
    this.optionValue = optionValue;
  }

  public BigDecimal getOptionPrice() {
    return optionPrice;
  }

  public void setOptionPrice(BigDecimal optionPrice) {
    this.optionPrice = optionPrice;
  }

  public BigDecimal getFreeStreaming() {
    return freeStreaming;
  }

  public void setFreeStreaming(BigDecimal freeStreaming) {
    this.freeStreaming = freeStreaming;
  }

  public BigDecimal getConnectPlusDiscount() {
    return connectPlusDiscount;
  }

  public void setConnectPlusDiscount(BigDecimal connectPlusDiscount) {
    this.connectPlusDiscount = connectPlusDiscount;
  }

  public BigDecimal getConnectPlusBonus() {
    return connectPlusBonus;
  }

  public void setConnectPlusBonus(BigDecimal connectPlusBonus) {
    this.connectPlusBonus = connectPlusBonus;
  }

  @Override
  public String toString() {
    return "MobileTariffNew [tariffValue=" + tariffValue + ", tariffPrice=" + tariffPrice + ", featureNutzenBoxValue=" + featureNutzenBoxValue + ", tariffOptionValue=" + tariffOptionValue
        + ", tariffOptionPrice=" + tariffOptionPrice + ", internetProtection=" + internetProtection + ", internetProtectionPrice=" + internetProtectionPrice + ", cyberProtection=" + cyberProtection
        + ", cyberProtectionPrice=" + cyberProtectionPrice + ", a1Mastercard=" + a1Mastercard + ", a1MastercardPrice=" + a1MastercardPrice + ", a1XploreTvStreaming=" + a1XploreTvStreaming
        + ", a1XploreTvStreamingPrice=" + a1XploreTvStreamingPrice + ", a1XploreMusic=" + a1XploreMusic + ", a1XploreMusicPrice=" + a1XploreMusicPrice + ", additionSim=" + additionSim
        + ", additionSimPrice=" + additionSimPrice + ", optionValue=" + optionValue + ", optionPrice=" + optionPrice + ", freeStreaming=" + freeStreaming + ", connectPlusDiscount="
        + connectPlusDiscount + ", connectPlusBonus=" + connectPlusBonus + "]";
  }

}
