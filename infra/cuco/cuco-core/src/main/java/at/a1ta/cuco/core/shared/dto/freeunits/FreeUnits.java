package at.a1ta.cuco.core.shared.dto.freeunits;

import java.io.Serializable;
import java.math.BigInteger;

@SuppressWarnings("serial")
public class FreeUnits implements Serializable {
  public static final String ACCUMULATOR_UNIT_MIN = "Min";
  private static final String ACCUMULATOR_UNIT_SEC = "Sec";
  private static final String ACCUMULATOR_UNIT_MSEC = "Msec";
  private static final String ACCUMULATOR_UNIT_PULSE = "Pulse";

  private static final BigInteger ACCUMULATOR_MIN_DIVIDE = BigInteger.valueOf(1);
  private static final BigInteger ACCUMULATOR_SEC_DIVIDE = BigInteger.valueOf(60);
  private static final BigInteger ACCUMULATOR_MSEC_DIVIDE = BigInteger.valueOf(60000);
  private static final BigInteger ACCUMULATOR_DEFAULT_DIVIDE = ACCUMULATOR_MIN_DIVIDE;

  private String tnvId;
  private String sidId;
  private String productDescription;
  private BigInteger maximumValue;
  private String unit;
  private BigInteger usedValue;
  private String lastUpdateDate;

  public FreeUnits() {}

  public FreeUnits(final String unit, final long usedValue, final long maximumValue) {
    this.unit = unit;
    this.usedValue = BigInteger.valueOf(usedValue);
    this.maximumValue = BigInteger.valueOf(maximumValue);
  }

  public String getTnvId() {
    return tnvId;
  }

  public void setTnvId(final String tnvId) {
    this.tnvId = tnvId;
  }

  public String getSidId() {
    return sidId;
  }

  public void setSidId(final String sidId) {
    this.sidId = sidId;
  }

  public String getProductDescription() {
    return productDescription;
  }

  public void setProductDescription(final String productDescription) {
    this.productDescription = productDescription;
  }

  public BigInteger getMaximumValue() {
    return maximumValue;
  }

  public void setMaximumValue(final BigInteger maximumValue) {
    this.maximumValue = maximumValue;
  }

  public String getUnit() {
    return unit;
  }

  public void setUnit(final String unit) {
    this.unit = unit;
  }

  public BigInteger getUsedValue() {
    return usedValue;
  }

  public void setUsedValue(final BigInteger usedValue) {
    this.usedValue = usedValue;
  }

  public String getLastUpdateDate() {
    return lastUpdateDate;
  }

  public void setLastUpdateDate(final String lastUpdateDate) {
    this.lastUpdateDate = lastUpdateDate;
  }

  public BigInteger getUsedMinutes() {
    return calculateMinutesValue(unit, usedValue);
  }

  public BigInteger getMaximumMinutes() {
    return calculateMinutesValue(unit, maximumValue);
  }

  public BigInteger getUnusedMinutes() {
    return calculateMinutesValue(unit, maximumValue.subtract(usedValue));
  }

  public void addUsed(final BigInteger value) {
    this.usedValue = this.usedValue.add(value);
  }

  public void addMaximum(final BigInteger value) {
    this.maximumValue = this.maximumValue.add(value);
  }

  public boolean hasPulseUnit() {
    return ACCUMULATOR_UNIT_PULSE.equalsIgnoreCase(unit);
  }

  private static BigInteger calculateMinutesValue(String unit, BigInteger value) {
    if (ACCUMULATOR_UNIT_MIN.equalsIgnoreCase(unit)) {
      return value.divide(ACCUMULATOR_MIN_DIVIDE);
    } else if (ACCUMULATOR_UNIT_SEC.equalsIgnoreCase(unit)) {
      return value.divide(ACCUMULATOR_SEC_DIVIDE);
    } else if (ACCUMULATOR_UNIT_MSEC.equalsIgnoreCase(unit)) {
      return value.divide(ACCUMULATOR_MSEC_DIVIDE);
    } else if (ACCUMULATOR_UNIT_PULSE.equalsIgnoreCase(unit) || unit == null) {
      return BigInteger.ZERO; // hence: will not manipulate any sum
    } else {
      return value.divide(ACCUMULATOR_DEFAULT_DIVIDE);
    }
  }
}
