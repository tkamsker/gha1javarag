package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

@XmlAccessorType(XmlAccessType.FIELD)
public class Security implements Serializable {
  private static final long serialVersionUID = 1L;

  @XmlElement
  private SecurityOld securityOld;

  @XmlElement
  private SecurityNew securityNew;

  public SecurityOld getSecurityOld() {
    if (securityOld == null) {
      securityOld = new SecurityOld();
    }
    return securityOld;
  }

  public void setSecurityOld(SecurityOld securityOld) {
    this.securityOld = securityOld;
  }

  public SecurityNew getSecurityNew() {
    if (securityNew == null) {
      securityNew = new SecurityNew();
    }
    return securityNew;
  }

  public void setSecurityNew(SecurityNew securityNew) {
    this.securityNew = securityNew;
  }

  @Override
  public String toString() {
    return "Security [securityOld=" + securityOld + ", securityNew=" + securityNew + "]";
  }

}
