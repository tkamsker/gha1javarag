package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

public class Turnover implements Serializable {
  public static final String TYPE_TA = "ta";
  public static final String TYPE_MK = "mk";

  private long partyId;
  private Date month;
  private float turnoverTa;
  private float marginTa;
  private float turnoverMk;
  private float marginMk;

  public long getPartyId() {
    return partyId;
  }

  public void setPartyId(long partyId) {
    this.partyId = partyId;
  }

  public Date getMonth() {
    return month;
  }

  public void setMonth(Date month) {
    this.month = month;
  }

  public float getTurnoverTa() {
    return turnoverTa;
  }

  public void setTurnoverTa(float turnoverTa) {
    this.turnoverTa = turnoverTa;
  }

  public float getMarginTa() {
    return marginTa;
  }

  public void setMarginTa(float marginTa) {
    this.marginTa = marginTa;
  }

  public float getTurnoverMk() {
    return turnoverMk;
  }

  public void setTurnoverMk(float turnoverMk) {
    this.turnoverMk = turnoverMk;
  }

  public float getMarginMk() {
    return marginMk;
  }

  public void setMarginMk(float marginMk) {
    this.marginMk = marginMk;
  }
}
