package at.a1ta.cuco.core.shared.dto.freeunits;

import java.io.Serializable;
import java.math.BigInteger;

public class FreeUnitsResult implements Serializable {
  private String name;
  private String description;
  private boolean isPulseUnit;
  private BigInteger minutesMaximum;
  private BigInteger minutesUsed;
  private BigInteger minutesUnused;

  public FreeUnitsResult() {}

  public FreeUnitsResult(String name, String description, boolean isPulseUnit) {
    this.name = name;
    this.description = description;
    this.isPulseUnit = isPulseUnit;
  }

  public FreeUnitsResult(String name, String description, boolean isPulseUnit, BigInteger minutesMaximum, BigInteger minutesUsed,
      BigInteger minutesUnused) {
    this.name = name;
    this.description = description;
    this.isPulseUnit = isPulseUnit;
    this.minutesMaximum = minutesMaximum;
    this.minutesUsed = minutesUsed;
    this.minutesUnused = minutesUnused;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getDescription() {
    return description;
  }

  public void setDescription(String description) {
    this.description = description;
  }

  public boolean isPulseUnit() {
    return isPulseUnit;
  }

  public void setPulseUnit(boolean isPulseUnit) {
    this.isPulseUnit = isPulseUnit;
  }

  public BigInteger getMinutesMaximum() {
    return minutesMaximum;
  }

  public void setMinutesMaximum(BigInteger minutesMaximum) {
    this.minutesMaximum = minutesMaximum;
  }

  public BigInteger getMinutesUsed() {
    return minutesUsed;
  }

  public void setMinutesUsed(BigInteger minutesUsed) {
    this.minutesUsed = minutesUsed;
  }

  public BigInteger getMinutesUnused() {
    return minutesUnused;
  }

  public void setMinutesUnused(BigInteger minutesUnused) {
    this.minutesUnused = minutesUnused;
  }
}