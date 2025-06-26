package at.a1ta.cuco.core.shared.dto.product;

import java.math.BigDecimal;
import java.util.Date;

import at.a1ta.cuco.core.shared.dto.IndexationStatus;

public class CuCoComponentProductPrice extends CuCoProductPriceBase {

  private CuCoPrice price;
  private BigDecimal taxRate;
  private IndexationStatus idxStatus;
  private Date idxStartDate;
  private CuCoPrice basePrice;

  public CuCoPrice getPrice() {
    return price;
  }

  public void setPrice(CuCoPrice price) {
    this.price = price;
  }

  public BigDecimal getTaxRate() {
    return taxRate;
  }

  public void setTaxRate(BigDecimal taxRate) {
    this.taxRate = taxRate;
  }

  public IndexationStatus getIdxStatus() {
    return idxStatus;
  }

  public void setIdxStatus(IndexationStatus idxStatus) {
    this.idxStatus = idxStatus;
  }

  public Date getIdxStartDate() {
    return idxStartDate;
  }

  public void setIdxStartDate(Date idxStartDate) {
    this.idxStartDate = idxStartDate;
  }

  public CuCoPrice getBasePrice() {
    return basePrice;
  }

  public void setBasePrice(CuCoPrice basePrice) {
    this.basePrice = basePrice;
  }

}
