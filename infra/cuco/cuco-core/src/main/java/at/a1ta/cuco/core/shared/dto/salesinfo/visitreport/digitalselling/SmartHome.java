package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

@XmlAccessorType(XmlAccessType.FIELD)
public class SmartHome implements Serializable {
  private static final long serialVersionUID = 1L;

  @XmlElement
  private SmartHomeOld smartHomeOld;

  @XmlElement
  private SmartHomeNew smartHomeNew;

  public SmartHomeOld getSmartHomeOld() {
    if (smartHomeOld == null) {
      smartHomeOld = new SmartHomeOld();
    }
    return smartHomeOld;
  }

  public void setSmartHomeOld(SmartHomeOld smartHomeOld) {
    this.smartHomeOld = smartHomeOld;
  }

  public SmartHomeNew getSmartHomeNew() {
    if (smartHomeNew == null) {
      smartHomeNew = new SmartHomeNew();
    }
    return smartHomeNew;
  }

  public void setSmartHomeNew(SmartHomeNew smartHomeNew) {
    this.smartHomeNew = smartHomeNew;
  }

  @Override
  public String toString() {
    return "SmartHome [smartHomeOld=" + smartHomeOld + ", smartHomeNew=" + smartHomeNew + "]";
  }
}
