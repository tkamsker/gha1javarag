package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class Music implements Serializable {
  private static final long serialVersionUID = 1L;

  private String usedMusicApps;
  private BigDecimal usedMusicAppsPrice;

  private MusicApp musicApp;
  private BigDecimal musicAppPrice;
  private String musicAppText;

  private boolean xMonthsFree;
  private String xMonthsFreeText;

  private String listenMusicLocationText;

  private String speakerName;
  private BigDecimal speakerPrice;
  private String speakerFeatureText;

  private MusicSpeakerType speakerType;

  private String headsetName;
  private BigDecimal headsetPrice;
  private String headsetFeatureText;

  private String commentOld;
  private String commentNew;

  private BigDecimal sum;

  public String getUsedMusicApps() {
    return usedMusicApps;
  }

  public void setUsedMusicApps(String usedMusicApps) {
    this.usedMusicApps = usedMusicApps;
  }

  public BigDecimal getUsedMusicAppsPrice() {
    return usedMusicAppsPrice;
  }

  public void setUsedMusicAppsPrice(BigDecimal usedMusicAppsPrice) {
    this.usedMusicAppsPrice = usedMusicAppsPrice;
  }

  public MusicApp getMusicApp() {
    return musicApp;
  }

  public void setMusicApp(MusicApp musicApp) {
    this.musicApp = musicApp;
  }

  public BigDecimal getMusicAppPrice() {
    return musicAppPrice;
  }

  public void setMusicAppPrice(BigDecimal musicAppPrice) {
    this.musicAppPrice = musicAppPrice;
  }

  public String getMusicAppText() {
    return musicAppText;
  }

  public void setMusicAppText(String musicAppText) {
    this.musicAppText = musicAppText;
  }

  public boolean isxMonthsFree() {
    return xMonthsFree;
  }

  public void setxMonthsFree(boolean xMonthsFree) {
    this.xMonthsFree = xMonthsFree;
  }

  public String getxMonthsFreeText() {
    return xMonthsFreeText;
  }

  public void setxMonthsFreeText(String xMonthsFreeText) {
    this.xMonthsFreeText = xMonthsFreeText;
  }

  public String getListenMusicLocationText() {
    return listenMusicLocationText;
  }

  public void setListenMusicLocationText(String listenMusicLocationText) {
    this.listenMusicLocationText = listenMusicLocationText;
  }

  public String getSpeakerName() {
    return speakerName;
  }

  public void setSpeakerName(String speakerName) {
    this.speakerName = speakerName;
  }

  public BigDecimal getSpeakerPrice() {
    return speakerPrice;
  }

  public void setSpeakerPrice(BigDecimal speakerPrice) {
    this.speakerPrice = speakerPrice;
  }

  public String getSpeakerFeatureText() {
    return speakerFeatureText;
  }

  public void setSpeakerFeatureText(String speakerFeatureText) {
    this.speakerFeatureText = speakerFeatureText;
  }

  public MusicSpeakerType getSpeakerType() {
    return speakerType;
  }

  public void setSpeakerType(MusicSpeakerType speakerType) {
    this.speakerType = speakerType;
  }

  public String getHeadsetName() {
    return headsetName;
  }

  public void setHeadsetName(String headsetName) {
    this.headsetName = headsetName;
  }

  public BigDecimal getHeadsetPrice() {
    return headsetPrice;
  }

  public void setHeadsetPrice(BigDecimal headsetPrice) {
    this.headsetPrice = headsetPrice;
  }

  public String getHeadsetFeatureText() {
    return headsetFeatureText;
  }

  public void setHeadsetFeatureText(String headsetFeatureText) {
    this.headsetFeatureText = headsetFeatureText;
  }

  public String getCommentOld() {
    return commentOld;
  }

  public void setCommentOld(String commentOld) {
    this.commentOld = commentOld;
  }

  public String getCommentNew() {
    return commentNew;
  }

  public void setCommentNew(String commentNew) {
    this.commentNew = commentNew;
  }

  public BigDecimal getSum() {
    return sum;
  }

  public void setSum(BigDecimal sum) {
    this.sum = sum;
  }

  @Override
  public String toString() {
    return "Music [usedMusicApps=" + usedMusicApps + ", usedMusicAppsPrice=" + usedMusicAppsPrice + ", musicApp=" + musicApp + ", musicAppPrice=" + musicAppPrice + ", musicAppText=" + musicAppText
        + ", xMonthsFree=" + xMonthsFree + ", xMonthsFreeText=" + xMonthsFreeText + ", listenMusicLocationText=" + listenMusicLocationText + ", speakerName=" + speakerName + ", speakerPrice="
        + speakerPrice + ", speakerFeatureText=" + speakerFeatureText + ", speakerType=" + speakerType + ", headsetName=" + headsetName + ", headsetPrice=" + headsetPrice + ", headsetFeatureText="
        + headsetFeatureText + ", commentOld=" + commentOld + ", commentNew=" + commentNew + ", sum=" + sum + "]";
  }

}
