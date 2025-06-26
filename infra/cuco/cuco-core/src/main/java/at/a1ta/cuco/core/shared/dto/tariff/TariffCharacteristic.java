package at.a1ta.cuco.core.shared.dto.tariff;

import java.io.Serializable;

public class TariffCharacteristic implements Serializable {

  private Serializable id;
  private String name;
  private String code;
  private Price price;
  private boolean usedInSimulationCalculation;

  public Price getPrice() {
    return price;
  }

  /**
   * the same as getPrice().getGross() but with not-null check.
   * 
   * @return gross price value or null.
   */
  public Float getPriceGross() {
    return price != null ? price.getGross() : null;
  }

  /**
   * the same as getPrice().getNet() but with not-null check.
   * 
   * @return net price value or null.
   */
  public Float getPriceNet() {
    return price != null ? price.getNet() : null;
  }

  public void setPrice(Price price) {
    this.price = price;
  }

  public Serializable getId() {
    return id;
  }

  public void setId(Serializable id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getCode() {
    return code;
  }

  public void setCode(String code) {
    this.code = code;
  }

  public void setUsedInSimulationCalculation(boolean usedInSimulationCalculation) {
    this.usedInSimulationCalculation = usedInSimulationCalculation;
  }

  public boolean isUsedInSimulationCalculation() {
    return usedInSimulationCalculation;
  }

}
