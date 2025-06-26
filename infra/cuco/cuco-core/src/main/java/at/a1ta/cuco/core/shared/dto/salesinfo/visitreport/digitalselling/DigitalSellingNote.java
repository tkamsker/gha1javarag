package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.math.BigDecimal;
import java.util.List;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

import at.a1ta.cuco.core.shared.dto.Attribute;
import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;

@XmlRootElement
@XmlAccessorType(XmlAccessType.FIELD)
public class DigitalSellingNote extends SalesInfoNote {
  private static final long serialVersionUID = 1L;

  @XmlTransient
  private DigitalSellingNote savedInstance;

  @XmlTransient
  private String content;

  @XmlElement
  private Household household;

  @XmlElement
  private InternetSpeed internetSpeed;

  @XmlElement
  private TV tv;

  @XmlElement
  private MobilePhone mobilePhone;

  @XmlElement
  private MobileTariff mobileTariff;

  @XmlElement
  private Music music;

  @XmlElement
  private Security security;

  @XmlElement
  private SmartHome smartHome;

  @XmlElement
  private Payment payment;

  @XmlElement
  private Services services;

  @XmlTransient
  private List<Attribute> attributes;

  @XmlElement
  private String comment;

  @XmlElement
  private BigDecimal sumOld;

  @XmlElement
  private BigDecimal sumNew;

  public DigitalSellingNote() {
    super();
  }

  public DigitalSellingNote(DigitalSellingNote note) {
    super(note);
    this.household = note.getHousehold();
    this.internetSpeed = note.getInternetSpeed();
    this.tv = note.getTv();
    this.mobilePhone = note.getMobilePhone();
    this.mobileTariff = note.getMobileTariff();
    this.music = note.getMusic();
    this.security = note.getSecurity();
    this.smartHome = note.getSmartHome();
    this.payment = note.getPayment();
    this.services = note.getServices();
    this.comment = note.getComment();
    this.sumOld = note.getSumOld();
    this.sumNew = note.getSumNew();
  }

  public Household getHousehold() {
    if (household == null) {
      household = new Household();
    }
    return household;
  }

  public void setHousehold(Household household) {
    this.household = household;
  }

  public InternetSpeed getInternetSpeed() {
    if (internetSpeed == null) {
      internetSpeed = new InternetSpeed();
    }
    return internetSpeed;
  }

  public void setInternetSpeed(InternetSpeed internetSpeed) {
    this.internetSpeed = internetSpeed;
  }

  public TV getTv() {
    if (tv == null) {
      tv = new TV();
    }
    return tv;
  }

  public void setTv(TV tv) {
    this.tv = tv;
  }

  public MobilePhone getMobilePhone() {
    if (mobilePhone == null) {
      mobilePhone = new MobilePhone();
    }
    return mobilePhone;
  }

  public void setMobilePhone(MobilePhone mobilePhone) {
    this.mobilePhone = mobilePhone;
  }

  public MobileTariff getMobileTariff() {
    if (mobileTariff == null) {
      mobileTariff = new MobileTariff();
    }
    return mobileTariff;
  }

  public void setMobileTariff(MobileTariff mobileTariff) {
    this.mobileTariff = mobileTariff;
  }

  public Music getMusic() {
    if (music == null) {
      music = new Music();
    }
    return music;
  }

  public void setMusic(Music music) {
    this.music = music;
  }

  public Security getSecurity() {
    if (security == null) {
      security = new Security();
    }
    return security;
  }

  public void setSecurity(Security security) {
    this.security = security;
  }

  public SmartHome getSmartHome() {
    if (smartHome == null) {
      smartHome = new SmartHome();
    }
    return smartHome;
  }

  public void setSmartHome(SmartHome smartHome) {
    this.smartHome = smartHome;
  }

  public Payment getPayment() {
    if (payment == null) {
      payment = new Payment();
    }
    return payment;
  }

  public void setPayment(Payment payment) {
    this.payment = payment;
  }

  public Services getServices() {
    if (services == null) {
      services = new Services();
    }
    return services;
  }

  public void setServices(Services services) {
    this.services = services;
  }

  public String getComment() {
    return comment;
  }

  public void setComment(String comment) {
    this.comment = comment;
  }

  public BigDecimal getSumOld() {
    return sumOld;
  }

  public void setSumOld(BigDecimal sumOld) {
    this.sumOld = sumOld;
  }

  public BigDecimal getSumNew() {
    return sumNew;
  }

  public void setSumNew(BigDecimal sumNew) {
    this.sumNew = sumNew;
  }

  @Override
  public String toString() {
    return "DigitalSellingNote [household=" + household + ", internetSpeed=" + internetSpeed + ", tv=" + tv + ", mobilePhone=" + mobilePhone + ", mobileTariff=" + mobileTariff + ", music=" + music
        + ", security=" + security + ", smartHome=" + smartHome + ", payment=" + payment + ", services=" + services + ", attributes=" + attributes + ", comment=" + comment + ", sumOld=" + sumOld
        + ", sumNew=" + sumNew + "]";
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = super.hashCode();
    result = prime * result + ((household == null) ? 0 : household.hashCode());
    result = prime * result + ((internetSpeed == null) ? 0 : internetSpeed.hashCode());
    result = prime * result + ((mobilePhone == null) ? 0 : mobilePhone.hashCode());
    result = prime * result + ((mobileTariff == null) ? 0 : mobileTariff.hashCode());
    result = prime * result + ((music == null) ? 0 : music.hashCode());
    result = prime * result + ((payment == null) ? 0 : payment.hashCode());
    result = prime * result + ((security == null) ? 0 : security.hashCode());
    result = prime * result + ((services == null) ? 0 : services.hashCode());
    result = prime * result + ((smartHome == null) ? 0 : smartHome.hashCode());
    result = prime * result + ((tv == null) ? 0 : tv.hashCode());
    result = prime * result + comment.hashCode();
    result = prime * result + sumOld.hashCode();
    result = prime * result + sumNew.hashCode();
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (!super.equals(obj)) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    DigitalSellingNote other = (DigitalSellingNote) obj;
    if (household == null) {
      if (other.household != null) {
        return false;
      }
    } else if (!household.equals(other.household)) {
      return false;
    }
    if (internetSpeed == null) {
      if (other.internetSpeed != null) {
        return false;
      }
    } else if (!internetSpeed.equals(other.internetSpeed)) {
      return false;
    }
    if (mobilePhone == null) {
      if (other.mobilePhone != null) {
        return false;
      }
    } else if (!mobilePhone.equals(other.mobilePhone)) {
      return false;
    }
    if (mobileTariff == null) {
      if (other.mobileTariff != null) {
        return false;
      }
    } else if (!mobileTariff.equals(other.mobileTariff)) {
      return false;
    }
    if (music == null) {
      if (other.music != null) {
        return false;
      }
    } else if (!music.equals(other.music)) {
      return false;
    }
    if (payment == null) {
      if (other.payment != null) {
        return false;
      }
    } else if (!payment.equals(other.payment)) {
      return false;
    }
    if (security == null) {
      if (other.security != null) {
        return false;
      }
    } else if (!security.equals(other.security)) {
      return false;
    }
    if (services == null) {
      if (other.services != null) {
        return false;
      }
    } else if (!services.equals(other.services)) {
      return false;
    }
    if (smartHome == null) {
      if (other.smartHome != null) {
        return false;
      }
    } else if (!smartHome.equals(other.smartHome)) {
      return false;
    }
    if (tv == null) {
      if (other.tv != null) {
        return false;
      }
    } else if (!tv.equals(other.tv)) {
      return false;
    }
    if (!comment.equals(other.comment)) {
      return false;
    }
    if (!sumOld.equals(other.sumOld)) {
      return false;
    }
    if (!sumNew.equals(other.sumNew)) {
      return false;
    }
    return true;
  }

  public DigitalSellingNote getSavedInstance() {
    if (savedInstance == null) {
      return new DigitalSellingNote(this);
    }
    return savedInstance;
  }

  public void setSavedInstance(DigitalSellingNote savedInstance) {
    this.savedInstance = savedInstance;
  }

  public String getContent() {
    return content;
  }

  public void setContent(String content) {
    this.content = content;
  }

  public List<Attribute> getAttributes() {
    return attributes;
  }

  public void setAttributes(List<Attribute> attributes) {
    this.attributes = attributes;
  }

}
