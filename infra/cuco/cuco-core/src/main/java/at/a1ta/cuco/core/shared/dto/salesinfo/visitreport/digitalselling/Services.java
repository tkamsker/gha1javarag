package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

@XmlAccessorType(XmlAccessType.FIELD)
public class Services implements Serializable {
  private static final long serialVersionUID = 1L;

  @XmlElement
  private ServicesOld servicesOld;

  @XmlElement
  private ServicesNew servicesNew;

  public ServicesOld getServicesOld() {
    if (servicesOld == null) {
      servicesOld = new ServicesOld();
    }
    return servicesOld;
  }

  public void setServicesOld(ServicesOld servicesOld) {
    this.servicesOld = servicesOld;
  }

  public ServicesNew getServicesNew() {
    if (servicesNew == null) {
      servicesNew = new ServicesNew();
    }
    return servicesNew;
  }

  public void setServicesNew(ServicesNew servicesNew) {
    this.servicesNew = servicesNew;
  }

  @Override
  public String toString() {
    return "Services [servicesOld=" + servicesOld + ", servicesNew=" + servicesNew + "]";
  }

}
