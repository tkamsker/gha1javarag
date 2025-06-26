package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

@XmlAccessorType(XmlAccessType.FIELD)
public class InternetSpeed implements Serializable {
  private static final long serialVersionUID = 1L;

  @XmlElement
  private InternetSpeedOld internetSpeedOld;

  @XmlElement
  private InternetSpeedNew internetSpeedNew;

  public InternetSpeedOld getInternetSpeedOld() {
    if (internetSpeedOld == null) {
      internetSpeedOld = new InternetSpeedOld();
    }
    return internetSpeedOld;
  }

  public void setInternetSpeedOld(InternetSpeedOld internetSpeedOld) {
    this.internetSpeedOld = internetSpeedOld;
  }

  public InternetSpeedNew getInternetSpeedNew() {
    if (internetSpeedNew == null) {
      internetSpeedNew = new InternetSpeedNew();
    }
    return internetSpeedNew;
  }

  public void setInternetSpeedNew(InternetSpeedNew internetSpeedNew) {
    this.internetSpeedNew = internetSpeedNew;
  }

  @Override
  public String toString() {
    return "InternetSpeed [internetSpeedOld=" + internetSpeedOld + ", internetSpeedNew=" + internetSpeedNew + "]";
  }

}
