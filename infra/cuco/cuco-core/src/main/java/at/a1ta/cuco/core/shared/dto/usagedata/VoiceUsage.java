package at.a1ta.cuco.core.shared.dto.usagedata;

import java.io.Serializable;
import java.util.Date;

public class VoiceUsage implements Serializable {
  private Date date;
  private Double duration;
  private Double connectionFee;
  private String zone;
  private String timeType;
  private String provider;

  public Date getDate() {
    return date;
  }

  public void setDate(Date date) {
    this.date = date;
  }

  public Double getDuration() {
    return duration;
  }

  public void setDuration(Double duration) {
    this.duration = duration;
  }

  public Double getConnectionFee() {
    return connectionFee;
  }

  public void setConnectionFee(Double connectionFee) {
    this.connectionFee = connectionFee;
  }

  public String getZone() {
    return zone;
  }

  public void setZone(String zone) {
    this.zone = zone;
  }

  public String getTimeType() {
    return timeType;
  }

  public void setTimeType(String timeType) {
    this.timeType = timeType;
  }

  public void setProvider(String provider) {
    this.provider = provider;
  }

  public String getProvider() {
    return provider;
  }

}