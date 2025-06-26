package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;
import java.math.BigDecimal;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class SummaryItem implements Serializable {
  private static final long serialVersionUID = 1L;

  private String name;
  private BigDecimal sumOld;
  private BigDecimal sumNew;

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
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

  public SummaryItem() {
    super();
  }

  public SummaryItem(String name, BigDecimal sumOld, BigDecimal sumNew) {
    super();
    this.name = name;
    this.sumOld = sumOld;
    this.sumNew = sumNew;
  }

  @Override
  public String toString() {
    return "SummaryItem [name=" + name + ", sumOld=" + sumOld + ", sumNew=" + sumNew + "]";
  }

}
