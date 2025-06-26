package at.a1ta.cuco.core.shared.dto.product;

import java.util.Date;

public class CuCoProdPriceAlterations extends CuCoComponentProductPrice {
  public enum ProdPriceAlterationType {
    RECURRING_DISCOUNT, ONETIME_DISCOUNT, ALLOWANCE
  }

  public CuCoProdPriceAlterations() {
    super();
  }

  String frequency;
  String UnitOfMeasure;
  ProdPriceAlterationType alterationType = ProdPriceAlterationType.RECURRING_DISCOUNT;
  int allowanceValue;
  CuCoPrice alteredPriceAfterDiscount;
  String parentPriceId;
  private Date discountStartDate;
  private Date discountEndDate;

  public CuCoProdPriceAlterations(ProdPriceAlterationType alterationType) {
    super();
    this.alterationType = alterationType;
  }

  public String getFrequency() {
    return frequency;
  }

  public void setFrequency(String frequency) {
    this.frequency = frequency;
  }

  public String getUnitOfMeasure() {
    return UnitOfMeasure;
  }

  public void setUnitOfMeasure(String unitOfMeasure) {
    UnitOfMeasure = unitOfMeasure;
  }

  public ProdPriceAlterationType getAlterationType() {
    return alterationType;
  }

  public void setAlterationType(ProdPriceAlterationType alterationType) {
    this.alterationType = alterationType;
  }

  public int getAllowanceValue() {
    return allowanceValue;
  }

  public void setAllowanceValue(int allowanceValue) {
    this.allowanceValue = allowanceValue;
  }

  public CuCoPrice getAlteredPriceAfterDiscount() {
    return alteredPriceAfterDiscount;
  }

  public void setAlteredPriceAfterDiscount(CuCoPrice alteredPriceAfterDiscount) {
    this.alteredPriceAfterDiscount = alteredPriceAfterDiscount;
  }

  public String getParentPriceId() {
    return parentPriceId;
  }

  public void setParentPriceId(String parentPriceId) {
    this.parentPriceId = parentPriceId;
  }

  public Date getDiscountStartDate() {
    return discountStartDate;
  }

  public void setDiscountStartDate(Date discountStartDate) {
    this.discountStartDate = discountStartDate;
  }

  public Date getDiscountEndDate() {
    return discountEndDate;
  }

  public void setDiscountEndDate(Date discountEndDate) {
    this.discountEndDate = discountEndDate;
  }
}
