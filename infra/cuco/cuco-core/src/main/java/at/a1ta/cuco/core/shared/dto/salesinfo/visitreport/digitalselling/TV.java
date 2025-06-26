package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

@XmlAccessorType(XmlAccessType.FIELD)
public class TV implements Serializable {
  private static final long serialVersionUID = 1L;

  @XmlElement
  private TVOld tvOld;

  @XmlElement
  private TVNew tvNew;

  public TVOld getTvOld() {
    if (tvOld == null) {
      tvOld = new TVOld();
    }
    return tvOld;
  }

  public void setTvOld(TVOld tvOld) {
    this.tvOld = tvOld;
  }

  public TVNew getTvNew() {
    if (tvNew == null) {
      tvNew = new TVNew();
    }
    return tvNew;
  }

  public void setTvNew(TVNew tvNew) {
    this.tvNew = tvNew;
  }

  @Override
  public String toString() {
    return "TV [tvOld=" + tvOld + ", tvNew=" + tvNew + "]";
  }

}
