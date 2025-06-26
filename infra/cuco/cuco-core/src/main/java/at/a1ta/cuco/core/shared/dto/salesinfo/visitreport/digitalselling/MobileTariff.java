package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

@XmlAccessorType(XmlAccessType.FIELD)
public class MobileTariff implements Serializable {
  private static final long serialVersionUID = 1L;

  @XmlElement
  private MobileTariffOld mobileTariffOld;

  @XmlElement
  private MobileTariffNew mobileTariffNew;

  public MobileTariffOld getMobileTariffOld() {
    if (mobileTariffOld == null) {
      mobileTariffOld = new MobileTariffOld();
    }
    return mobileTariffOld;
  }

  public void setMobileTariffOld(MobileTariffOld mobileTariffOld) {
    this.mobileTariffOld = mobileTariffOld;
  }

  public MobileTariffNew getMobileTariffNew() {
    if (mobileTariffNew == null) {
      mobileTariffNew = new MobileTariffNew();
    }
    return mobileTariffNew;
  }

  public void setMobileTariffNew(MobileTariffNew mobileTariffNew) {
    this.mobileTariffNew = mobileTariffNew;
  }

  @Override
  public String toString() {
    return "MobileTariff [mobileTariffOld=" + mobileTariffOld + ", mobileTariffNew=" + mobileTariffNew + "]";
  }

}
