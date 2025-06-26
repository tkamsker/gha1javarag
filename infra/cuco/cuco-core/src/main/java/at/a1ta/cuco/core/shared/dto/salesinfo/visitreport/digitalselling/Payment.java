package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;

@XmlAccessorType(XmlAccessType.FIELD)
public class Payment implements Serializable {
  private static final long serialVersionUID = 1L;

  @XmlElement
  private PaymentOld paymentOld;

  @XmlElement
  private PaymentNew paymentnNew;

  public PaymentOld getPaymentOld() {
    if (paymentOld == null) {
      paymentOld = new PaymentOld();
    }
    return paymentOld;
  }

  public void setPaymentOld(PaymentOld paymentOld) {
    this.paymentOld = paymentOld;
  }

  public PaymentNew getPaymentNew() {
    if (paymentnNew == null) {
      paymentnNew = new PaymentNew();
    }
    return paymentnNew;
  }

  public void setPaymentnNew(PaymentNew paymentnNew) {
    this.paymentnNew = paymentnNew;
  }

  @Override
  public String toString() {
    return "Payment [paymentOld=" + paymentOld + ", paymentnNew=" + paymentnNew + "]";
  }

}
