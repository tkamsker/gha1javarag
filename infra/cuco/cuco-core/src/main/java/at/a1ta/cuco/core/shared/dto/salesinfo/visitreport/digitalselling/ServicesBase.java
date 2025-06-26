package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class ServicesBase implements Serializable {
  private static final long serialVersionUID = 1L;

  private boolean eScooter;
  private BigDecimal eScooterPrice;

  private boolean vacuumRobot; // Staubsaugerroboter
  private BigDecimal vacuumRobotPrice;

  private boolean toothbrush;
  private BigDecimal toothbrushPrice;

  private boolean remoteToys;
  private BigDecimal remoteToysPrice;

  private boolean speaker;
  private BigDecimal speakerPrice;

  private boolean headset;
  private BigDecimal headsetPrice;

  private String usedGadgetText;

  private BigDecimal sum;
  private String comment;

  public boolean iseScooter() {
    return eScooter;
  }

  public void seteScooter(boolean eScooter) {
    this.eScooter = eScooter;
  }

  public BigDecimal geteScooterPrice() {
    return eScooterPrice;
  }

  public void seteScooterPrice(BigDecimal eScooterPrice) {
    this.eScooterPrice = eScooterPrice;
  }

  public boolean isVacuumRobot() {
    return vacuumRobot;
  }

  public void setVacuumRobot(boolean vacuumRobot) {
    this.vacuumRobot = vacuumRobot;
  }

  public BigDecimal getVacuumRobotPrice() {
    return vacuumRobotPrice;
  }

  public void setVacuumRobotPrice(BigDecimal vacuumRobotPrice) {
    this.vacuumRobotPrice = vacuumRobotPrice;
  }

  public boolean isToothbrush() {
    return toothbrush;
  }

  public void setToothbrush(boolean toothbrush) {
    this.toothbrush = toothbrush;
  }

  public BigDecimal getToothbrushPrice() {
    return toothbrushPrice;
  }

  public void setToothbrushPrice(BigDecimal toothbrushPrice) {
    this.toothbrushPrice = toothbrushPrice;
  }

  public boolean isRemoteToys() {
    return remoteToys;
  }

  public void setRemoteToys(boolean remoteToys) {
    this.remoteToys = remoteToys;
  }

  public BigDecimal getRemoteToysPrice() {
    return remoteToysPrice;
  }

  public void setRemoteToysPrice(BigDecimal remoteToysPrice) {
    this.remoteToysPrice = remoteToysPrice;
  }

  public boolean isSpeaker() {
    return speaker;
  }

  public void setSpeaker(boolean speaker) {
    this.speaker = speaker;
  }

  public BigDecimal getSpeakerPrice() {
    return speakerPrice;
  }

  public void setSpeakerPrice(BigDecimal speakerPrice) {
    this.speakerPrice = speakerPrice;
  }

  public boolean isHeadset() {
    return headset;
  }

  public void setHeadset(boolean headset) {
    this.headset = headset;
  }

  public BigDecimal getHeadsetPrice() {
    return headsetPrice;
  }

  public void setHeadsetPrice(BigDecimal headsetPrice) {
    this.headsetPrice = headsetPrice;
  }

  public String getUsedGadgetText() {
    return usedGadgetText;
  }

  public void setUsedGadgetText(String usedGadgetText) {
    this.usedGadgetText = usedGadgetText;
  }

  public BigDecimal getSum() {
    return sum;
  }

  public void setSum(BigDecimal sum) {
    this.sum = sum;
  }

  public String getComment() {
    return comment;
  }

  public void setComment(String comment) {
    this.comment = comment;
  }

  @Override
  public String toString() {
    return "ServicesBase [eScooter=" + eScooter + ", eScooterPrice=" + eScooterPrice + ", vacuumRobot=" + vacuumRobot + ", vacuumRobotPrice=" + vacuumRobotPrice + ", toothbrush=" + toothbrush
        + ", toothbrushPrice=" + toothbrushPrice + ", remoteToys=" + remoteToys + ", remoteToysPrice=" + remoteToysPrice + ", speaker=" + speaker + ", speakerPrice=" + speakerPrice + ", headset="
        + headset + ", headsetPrice=" + headsetPrice + ", usedGadgetText=" + usedGadgetText + ", sum=" + sum + ", comment=" + comment + "]";
  }

}
