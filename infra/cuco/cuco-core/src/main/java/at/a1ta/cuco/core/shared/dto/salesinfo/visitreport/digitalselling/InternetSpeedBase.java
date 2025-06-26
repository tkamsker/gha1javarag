package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class InternetSpeedBase implements Serializable {
  private static final long serialVersionUID = 1L;

  private InternetType internetType; // Typ des Internets
  private BigDecimal internetTypePrice;
  private InternetSpeedType internetSpeedType; // Type der Internetgeschwindigkeit
  private BigDecimal internetSpeedPrice;
  private InternetSpeedMainUseType mainUseType; // Hauptnutzung

  // Weitere Nutzung
  private boolean netflix;
  private boolean surfMail;
  private boolean socialMedia;
  private boolean youtube;
  private boolean gaming;

  private String comment;

  private BigDecimal sum;

  public InternetType getInternetType() {
    return internetType;
  }

  public void setInternetType(InternetType internetType) {
    this.internetType = internetType;
  }

  public BigDecimal getInternetTypePrice() {
    return internetTypePrice;
  }

  public void setInternetTypePrice(BigDecimal internetTypePrice) {
    this.internetTypePrice = internetTypePrice;
  }

  public InternetSpeedType getInternetSpeedType() {
    return internetSpeedType;
  }

  public void setInternetSpeedType(InternetSpeedType internetSpeedType) {
    this.internetSpeedType = internetSpeedType;
  }

  public BigDecimal getInternetSpeedPrice() {
    return internetSpeedPrice;
  }

  public void setInternetSpeedPrice(BigDecimal internetSpeedPrice) {
    this.internetSpeedPrice = internetSpeedPrice;
  }

  public InternetSpeedMainUseType getMainUseType() {
    return mainUseType;
  }

  public void setMainUseType(InternetSpeedMainUseType mainUseType) {
    this.mainUseType = mainUseType;
  }

  public boolean isNetflix() {
    return netflix;
  }

  public void setNetflix(boolean netflix) {
    this.netflix = netflix;
  }

  public boolean isSurfMail() {
    return surfMail;
  }

  public void setSurfMail(boolean surfMail) {
    this.surfMail = surfMail;
  }

  public boolean isSocialMedia() {
    return socialMedia;
  }

  public void setSocialMedia(boolean socialMedia) {
    this.socialMedia = socialMedia;
  }

  public boolean isYoutube() {
    return youtube;
  }

  public void setYoutube(boolean youtube) {
    this.youtube = youtube;
  }

  public boolean isGaming() {
    return gaming;
  }

  public void setGaming(boolean gaming) {
    this.gaming = gaming;
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
    return "InternetSpeedBase [internetType=" + internetType + ", internetTypePrice=" + internetTypePrice + ", internetSpeedType=" + internetSpeedType + ", internetSpeedPrice=" + internetSpeedPrice
        + ", mainUseType=" + mainUseType + ", netflix=" + netflix + ", surfMail=" + surfMail + ", socialMedia=" + socialMedia + ", youtube=" + youtube + ", gaming=" + gaming + ", comment=" + comment
        + ", sum=" + sum + "]";
  }

}
