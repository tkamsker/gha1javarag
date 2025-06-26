package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class MobilePhoneBase implements Serializable {
  private static final long serialVersionUID = 1L;

  private String mobilePhoneName;
  private MobilePhoneMainUseType mainUseType; // Hauptnutzung

  // Weitere Nutzung
  private boolean communication;
  private boolean socialMedia;
  private boolean photoVideo;
  private boolean streaming;
  private boolean gaming;
  private boolean navigation;
  private boolean shopping;

  private String mainUseComment;
  private String comment;

  private BigDecimal sum;

  public String getMobilePhoneName() {
    return mobilePhoneName;
  }

  public void setMobilePhoneName(String mobilePhoneName) {
    this.mobilePhoneName = mobilePhoneName;
  }

  public MobilePhoneMainUseType getMainUseType() {
    return mainUseType;
  }

  public void setMainUseType(MobilePhoneMainUseType mainUseType) {
    this.mainUseType = mainUseType;
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

  public String getMainUseComment() {
    return mainUseComment;
  }

  public void setMainUseComment(String mainUseComment) {
    this.mainUseComment = mainUseComment;
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
    return "MobilePhoneBase [mobilePhoneName=" + mobilePhoneName + ", mainUseType=" + mainUseType + ", communication=" + communication + ", socialMedia=" + socialMedia + ", photoVideo=" + photoVideo
        + ", streaming=" + streaming + ", gaming=" + gaming + ", navigation=" + navigation + ", shopping=" + shopping + ", mainUseComment=" + mainUseComment + ", comment=" + comment + ", sum=" + sum
        + "]";
  }

}
