package at.a1ta.cuco.core.shared.dto.tariff;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class ContributionMargin implements Serializable {

  public static final ContributionMargin UNKNOWN = new ContributionMargin(new Price(Float.NaN, Float.NaN), Indicator.UNKNOWN) {

    @Override
    public void setIndicator(Indicator indicator) {}

    @Override
    public void setValue(Price value) {}

  };

  public enum Indicator {
    RED, GREEN, YELLOW, UNKNOWN;

    public static Indicator forValue(String value) {
      if (value == null || "".equals(value)) {
        return UNKNOWN;
      }

      return Indicator.valueOf(value.toUpperCase());
    }
  }

  private Price value;
  private Indicator indicator;
  private Price invoiceAmountChange;
  private Price averageInvoiceAmount;
  private Price simulatedInvoiceAmount;
  private Integer subscriberAmount;
  private List<String> subscribers;

  public ContributionMargin() {
    super();
  }

  public ContributionMargin(Price value, Indicator indicator) {
    this(value, indicator, null);
  }

  public ContributionMargin(Price value, Indicator indicator, Price invoiceAmountChange) {
    super();
    this.value = value;
    this.indicator = indicator;
    this.invoiceAmountChange = invoiceAmountChange;
  }

  public Price getValue() {
    return value;
  }

  public void setValue(Price value) {
    this.value = value;
  }

  public Indicator getIndicator() {
    return indicator;
  }

  public void setIndicator(Indicator indicator) {
    this.indicator = indicator;
  }

  public void setInvoiceAmountChange(Price invoiceAmountChange) {
    this.invoiceAmountChange = invoiceAmountChange;
  }

  public Price getInvoiceAmountChange() {
    return invoiceAmountChange;
  }

  public void setAverageInvoiceAmount(Price averageInvoiceAmount) {
    this.averageInvoiceAmount = averageInvoiceAmount;
  }

  public Price getAverageInvoiceAmount() {
    return averageInvoiceAmount;
  }

  public Price getSimulatedInvoiceAmount() {
    return simulatedInvoiceAmount;
  }

  public void setSimulatedInvoiceAmount(Price simulatedInvoiceAmount) {
    this.simulatedInvoiceAmount = simulatedInvoiceAmount;
  }

  /**
   * the same as getValue().getGross() but with not-null check.
   * 
   * @return gross value or null.
   */
  public Float getValueGross() {
    return value != null ? value.getGross() : null;
  }

  /**
   * the same as getValue().getNet() but with not-null check.
   * 
   * @return net value or null.
   */
  public Float getValueNet() {
    return value != null ? value.getNet() : null;
  }

  /**
   * the same as getInvoiceAmountChange().getGross() but with not-null check.
   * 
   * @return gross value of InvoiceAmountChange or null.
   */
  public Float getInvoiceAmountChangeGross() {
    return invoiceAmountChange != null ? invoiceAmountChange.getGross() : null;
  }

  /**
   * the same as getInvoiceAmountChange().getNet() but with not-null check.
   * 
   * @return net value of InvoiceAmountChange or null.
   */
  public Float getInvoiceAmountChangeNet() {
    return invoiceAmountChange != null ? invoiceAmountChange.getNet() : null;
  }

  /**
   * the same as getAverageInvoiceAmount().getGross() but with not-null check.
   * 
   * @return gross value of AverageInvoiceAmount or null.
   */
  public Float getAverageInvoiceAmountGross() {
    return averageInvoiceAmount != null ? averageInvoiceAmount.getGross() : null;
  }

  /**
   * the same as getAverageInvoiceAmount().getNet() but with not-null check.
   * 
   * @return net value of AverageInvoiceAmount or null.
   */
  public Float getAverageInvoiceAmountNet() {
    return averageInvoiceAmount != null ? averageInvoiceAmount.getNet() : null;
  }

  public void setSubscribers(List<String> subscribers) {
    this.subscribers = subscribers;
  }

  public Integer getSubscriberAmount() {
    return subscriberAmount;
  }

  public boolean hasSubscriptions() {
    return subscriberAmount != null && subscriberAmount.intValue() > 0;
  }

  public void setSubscriberAmount(Integer subscriberAmount) {
    this.subscriberAmount = subscriberAmount;
  }

  public List<String> getSubscribers() {
    return subscribers != null ? new ArrayList<String>(subscribers) : new ArrayList<String>(0);
  }
}
