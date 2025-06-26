package at.a1ta.cuco.core.shared.dto.product;

import java.util.ArrayList;
import java.util.List;

public class CuCoProdPriceCharge extends CuCoComponentProductPrice {
  public CuCoProdPriceCharge(ProdPriceChargeType chargeType) {
    super();
    this.chargeType = chargeType;
  }

  public CuCoProdPriceCharge() {
    super();
  }

  public enum ProdPriceChargeType {
    RECURRING, SIMPLE_USAGE, ONE_TIME, ACCOUNT_DISCOUNT
  }

  String frequency;
  String UnitOfMeasure;
  ProdPriceChargeType chargeType = ProdPriceChargeType.RECURRING;

  private List<CuCoProdPriceAlterations> alterations = new ArrayList<CuCoProdPriceAlterations>();

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

  public ProdPriceChargeType getChargeType() {
    return chargeType;
  }

  public void setChargeType(ProdPriceChargeType chargeType) {
    this.chargeType = chargeType;
  }

  public List<CuCoProdPriceAlterations> getAlterations() {
    return alterations;
  }

  public void setAlterations(List<CuCoProdPriceAlterations> alterations) {
    this.alterations = alterations;
  }

  public void addToAlterations(CuCoProdPriceAlterations cuCoProdPriceAlterations) {
    if (this.alterations == null) {
      this.alterations = new ArrayList<CuCoProdPriceAlterations>();
    }
    this.alterations.add(cuCoProdPriceAlterations);
  }
}
