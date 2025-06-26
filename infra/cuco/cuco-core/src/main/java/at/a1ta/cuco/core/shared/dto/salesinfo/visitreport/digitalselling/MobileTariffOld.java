package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class MobileTariffOld extends MobileTariffBase {
  private static final long serialVersionUID = 1L;

  private String tariffValue;
  private BigDecimal tariffPrice;

  private MobileTariffMainUseType mainUseType;
  private String mainUseTypeComment;

  // Weitere Nutzung
  private boolean communication;
  private boolean socialMedia;
  private boolean photoVideo;
  private boolean streaming;
  private boolean gaming;
  private boolean navigation;
  private boolean shopping;

  private boolean internetProtection; // Internetschutz
  private BigDecimal internetProtectionPrice;

  private boolean cyberProtection; // Cyberschutz
  private BigDecimal cyberProtectionPrice;

  private boolean creditCard; // Kreditkarte;
  private BigDecimal creditCardPrice;

  private boolean videoStreaming; // Videostreaming
  private BigDecimal videoStreamingPrice;

  private boolean musicStreaming; // Musikstreaming
  private BigDecimal musicStreamingPrice;

  private boolean additionalSim; // Zusatz SIM
  private BigDecimal additionalSimPrice;

  private String optionValue;
  private BigDecimal optionPrice;

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

  public MobileTariffMainUseType getMainUseType() {
    return mainUseType;
  }

  public void setMainUseType(MobileTariffMainUseType mainUseType) {
    this.mainUseType = mainUseType;
  }

  public String getMainUseTypeComment() {
    return mainUseTypeComment;
  }

  public void setMainUseTypeComment(String mainUseTypeComment) {
    this.mainUseTypeComment = mainUseTypeComment;
  }

  public boolean isCommunication() {
    return communication;
  }

  public void setCommunication(boolean communication) {
    this.communication = communication;
  }

  public boolean isSocialMedia() {
    return socialMedia;
  }

  public void setSocialMedia(boolean socialMedia) {
    this.socialMedia = socialMedia;
  }

  public boolean isPhotoVideo() {
    return photoVideo;
  }

  public void setPhotoVideo(boolean photoVideo) {
    this.photoVideo = photoVideo;
  }

  public boolean isStreaming() {
    return streaming;
  }

  public void setStreaming(boolean streaming) {
    this.streaming = streaming;
  }

  public boolean isGaming() {
    return gaming;
  }

  public void setGaming(boolean gaming) {
    this.gaming = gaming;
  }

  public boolean isNavigation() {
    return navigation;
  }

  public void setNavigation(boolean navigation) {
    this.navigation = navigation;
  }

  public boolean isShopping() {
    return shopping;
  }

  public void setShopping(boolean shopping) {
    this.shopping = shopping;
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

  public boolean isAdditionalSim() {
    return additionalSim;
  }

  public void setAdditionalSim(boolean additionalSim) {
    this.additionalSim = additionalSim;
  }

  public BigDecimal getAdditionalSimPrice() {
    return additionalSimPrice;
  }

  public void setAdditionalSimPrice(BigDecimal additionalSimPrice) {
    this.additionalSimPrice = additionalSimPrice;
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

  @Override
  public String toString() {
    return "MobileTariffOld [tariffValue=" + tariffValue + ", tariffPrice=" + tariffPrice + ", mainUseType=" + mainUseType + ", mainUseTypeComment=" + mainUseTypeComment + ", communication="
        + communication + ", socialMedia=" + socialMedia + ", photoVideo=" + photoVideo + ", streaming=" + streaming + ", gaming=" + gaming + ", navigation=" + navigation + ", shopping=" + shopping
        + ", internetProtection=" + internetProtection + ", internetProtectionPrice=" + internetProtectionPrice + ", cyberProtection=" + cyberProtection + ", cyberProtectionPrice="
        + cyberProtectionPrice + ", creditCard=" + creditCard + ", creditCardPrice=" + creditCardPrice + ", videoStreaming=" + videoStreaming + ", videoStreamingPrice=" + videoStreamingPrice
        + ", musicStreaming=" + musicStreaming + ", musicStreamingPrice=" + musicStreamingPrice + ", additionalSim=" + additionalSim + ", additionalSimPrice=" + additionalSimPrice + ", optionValue="
        + optionValue + ", optionPrice=" + optionPrice + "]";
  }

}
