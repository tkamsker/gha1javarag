package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

@XmlAccessorType(XmlAccessType.FIELD)
public class MobilePhone implements Serializable {
  private static final long serialVersionUID = 1L;

  @XmlElement
  private MobilePhoneOld mobilePhoneOld;

  @XmlElement
  private MobilePhoneNew mobilePhoneNew;

  public MobilePhoneOld getMobilePhoneOld() {
    if (mobilePhoneOld == null) {
      mobilePhoneOld = new MobilePhoneOld();
    }
    return mobilePhoneOld;
  }

  public void setMobilePhoneOld(MobilePhoneOld mobilePhoneOld) {
    this.mobilePhoneOld = mobilePhoneOld;
  }

  public MobilePhoneNew getMobilePhoneNew() {
    if (mobilePhoneNew == null) {
      this.mobilePhoneNew = new MobilePhoneNew();
    }
    return mobilePhoneNew;
  }

  public void setMobilePhoneNew(MobilePhoneNew mobilePhoneNew) {
    this.mobilePhoneNew = mobilePhoneNew;
  }

  @Override
  public String toString() {
    return "MobilePhone [mobilePhoneOld=" + mobilePhoneOld + ", mobilePhoneNew=" + mobilePhoneNew + "]";
  }

}
