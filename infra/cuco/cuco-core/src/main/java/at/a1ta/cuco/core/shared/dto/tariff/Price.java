package at.a1ta.cuco.core.shared.dto.tariff;

import java.io.Serializable;

public class Price implements Serializable {

  private Float gross;
  private Float net;

  public Price() {}

  public Price(Float gross, Float net) {
    this.gross = gross;
    this.net = net;
  }

  public Float getGross() {
    return gross;
  }

  public void setGross(Float value) {
    this.gross = value;
  }

  public Float getNet() {
    return net;
  }

  public void setNet(Float value) {
    this.net = value;
  }

  @Override
  public String toString() {
    return "{Gross: " + gross + ", Net: " + net + "}";
  }
}
