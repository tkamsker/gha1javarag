package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class TVBase implements Serializable {
  private static final long serialVersionUID = 1L;

  private TVType tvType;
  private BigDecimal tvTypePrice;
  private String countChannels; // Anzahl Sender
  private String oftenViewedChannels; // Meist gesehen
  private Integer countTVDevices;
  private Integer countMediaBoxes;

  private boolean sevenDaysReactivateWatch; // 7 Tage rueckwirkend fernsehen
  private BigDecimal sevenDaysReactivateWatchPrice;

  private boolean foreignLanguage; // Fremdsprachen TV
  private String foreignLanguageText;
  private BigDecimal foreignLanguagePrice;

  private boolean streamingOption;
  private BigDecimal streamingOptionPrice;

  private boolean hdTv;
  private BigDecimal hdTvPrice;

  private boolean onlineStorage; // Online Rekorder / Speicher
  private BigDecimal onlineStoragePrice;

  private boolean sky;
  private BigDecimal skyPrice;

  private boolean premiumTv;
  private BigDecimal premiumTvPrice;

  private boolean optionSelection;
  private String optionText;
  private BigDecimal optionPrice;

  private String comment;

  private BigDecimal sum;

  public TVType getTvType() {
    return tvType;
  }

  public void setTvType(TVType tvType) {
    this.tvType = tvType;
  }

  public BigDecimal getTvTypePrice() {
    return tvTypePrice;
  }

  public void setTvTypePrice(BigDecimal tvTypePrice) {
    this.tvTypePrice = tvTypePrice;
  }

  public String getCountChannels() {
    return countChannels;
  }

  public void setCountChannels(String countChannels) {
    this.countChannels = countChannels;
  }

  public String getOftenViewedChannels() {
    return oftenViewedChannels;
  }

  public void setOftenViewedChannels(String oftenViewedChannels) {
    this.oftenViewedChannels = oftenViewedChannels;
  }

  public Integer getCountTVDevices() {
    return countTVDevices;
  }

  public void setCountTVDevices(Integer countTVDevices) {
    this.countTVDevices = countTVDevices;
  }

  public Integer getCountMediaBoxes() {
    return countMediaBoxes;
  }

  public void setCountMediaBoxes(Integer countMediaBoxes) {
    this.countMediaBoxes = countMediaBoxes;
  }

  public boolean isSevenDaysReactivateWatch() {
    return sevenDaysReactivateWatch;
  }

  public void setSevenDaysReactivateWatch(boolean sevenDaysReactivateWatch) {
    this.sevenDaysReactivateWatch = sevenDaysReactivateWatch;
  }

  public BigDecimal getSevenDaysReactivateWatchPrice() {
    return sevenDaysReactivateWatchPrice;
  }

  public void setSevenDaysReactivateWatchPrice(BigDecimal sevenDaysReactivateWatchPrice) {
    this.sevenDaysReactivateWatchPrice = sevenDaysReactivateWatchPrice;
  }

  public boolean isForeignLanguage() {
    return foreignLanguage;
  }

  public void setForeignLanguage(boolean foreignLanguage) {
    this.foreignLanguage = foreignLanguage;
  }

  public String getForeignLanguageText() {
    return foreignLanguageText;
  }

  public void setForeignLanguageText(String foreignLanguageText) {
    this.foreignLanguageText = foreignLanguageText;
  }

  public BigDecimal getForeignLanguagePrice() {
    return foreignLanguagePrice;
  }

  public void setForeignLanguagePrice(BigDecimal foreignLanguagePrice) {
    this.foreignLanguagePrice = foreignLanguagePrice;
  }

  public boolean isStreamingOption() {
    return streamingOption;
  }

  public void setStreamingOption(boolean streamingOption) {
    this.streamingOption = streamingOption;
  }

  public BigDecimal getStreamingOptionPrice() {
    return streamingOptionPrice;
  }

  public void setStreamingOptionPrice(BigDecimal streamingOptionPrice) {
    this.streamingOptionPrice = streamingOptionPrice;
  }

  public boolean isHdTv() {
    return hdTv;
  }

  public void setHdTv(boolean hdTv) {
    this.hdTv = hdTv;
  }

  public BigDecimal getHdTvPrice() {
    return hdTvPrice;
  }

  public void setHdTvPrice(BigDecimal hdTvPrice) {
    this.hdTvPrice = hdTvPrice;
  }

  public boolean isOnlineStorage() {
    return onlineStorage;
  }

  public void setOnlineStorage(boolean onlineStorage) {
    this.onlineStorage = onlineStorage;
  }

  public BigDecimal getOnlineStoragePrice() {
    return onlineStoragePrice;
  }

  public void setOnlineStoragePrice(BigDecimal onlineStoragePrice) {
    this.onlineStoragePrice = onlineStoragePrice;
  }

  public boolean isSky() {
    return sky;
  }

  public void setSky(boolean sky) {
    this.sky = sky;
  }

  public BigDecimal getSkyPrice() {
    return skyPrice;
  }

  public void setSkyPrice(BigDecimal skyPrice) {
    this.skyPrice = skyPrice;
  }

  public boolean isPremiumTv() {
    return premiumTv;
  }

  public void setPremiumTv(boolean premiumTv) {
    this.premiumTv = premiumTv;
  }

  public BigDecimal getPremiumTvPrice() {
    return premiumTvPrice;
  }

  public void setPremiumTvPrice(BigDecimal premiumTvPrice) {
    this.premiumTvPrice = premiumTvPrice;
  }

  public boolean isOptionSelection() {
    return optionSelection;
  }

  public void setOptionSelection(boolean optionSelection) {
    this.optionSelection = optionSelection;
  }

  public String getOptionText() {
    return optionText;
  }

  public void setOptionText(String optionText) {
    this.optionText = optionText;
  }

  public BigDecimal getOptionPrice() {
    return optionPrice;
  }

  public void setOptionPrice(BigDecimal optionPrice) {
    this.optionPrice = optionPrice;
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
    return "TVBase [tvType=" + tvType + ", tvTypePrice=" + tvTypePrice + ", countChannels=" + countChannels + ", oftenViewedChannels=" + oftenViewedChannels + ", countTVDevices=" + countTVDevices
        + ", countMediaBoxes=" + countMediaBoxes + ", sevenDaysReactivateWatch=" + sevenDaysReactivateWatch + ", sevenDaysReactivateWatchPrice=" + sevenDaysReactivateWatchPrice + ", foreignLanguage="
        + foreignLanguage + ", foreignLanguageText=" + foreignLanguageText + ", foreignLanguagePrice=" + foreignLanguagePrice + ", streamingOption=" + streamingOption + ", streamingOptionPrice="
        + streamingOptionPrice + ", hdTv=" + hdTv + ", hdTvPrice=" + hdTvPrice + ", onlineStorage=" + onlineStorage + ", onlineStoragePrice=" + onlineStoragePrice + ", sky=" + sky + ", skyPrice="
        + skyPrice + ", premiumTv=" + premiumTv + ", premiumTvPrice=" + premiumTvPrice + ", optionSelection=" + optionSelection + ", optionText=" + optionText + ", optionPrice=" + optionPrice
        + ", comment=" + comment + ", sum=" + sum + "]";
  }

}
