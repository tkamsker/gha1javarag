package at.a1ta.cuco.core.shared.dto.usagedata;

import java.io.Serializable;
import java.util.Date;

public class InetUsage implements Serializable {
  private Date date;
  private long duration;
  private long uploadVolume;
  private long downloadVolume;
  private double subscriptionFee;
  private double variableFee;
  private double highUsageFee;
  private long transferVolumeOverrun;

  public Date getDate() {
    return date;
  }

  public void setDate(Date date) {
    this.date = date;
  }

  public long getDuration() {
    return duration;
  }

  public void setDuration(long duration) {
    this.duration = duration;
  }

  public long getUploadVolume() {
    return uploadVolume;
  }

  public void setUploadVolume(long uploadVolume) {
    this.uploadVolume = uploadVolume;
  }

  public long getDownloadVolume() {
    return downloadVolume;
  }

  public void setDownloadVolume(long downloadVolume) {
    this.downloadVolume = downloadVolume;
  }

  public double getSubscriptionFee() {
    return subscriptionFee;
  }

  public void setSubscriptionFee(double subscriptionFee) {
    this.subscriptionFee = subscriptionFee;
  }

  public double getVariableFee() {
    return variableFee;
  }

  public void setVariableFee(double variableFee) {
    this.variableFee = variableFee;
  }

  public double getHighUsageFee() {
    return highUsageFee;
  }

  public void setHighUsageFee(double highUsageFee) {
    this.highUsageFee = highUsageFee;
  }

  public long getTransferVolumeOverrun() {
    return transferVolumeOverrun;
  }

  public void setTransferVolumeOverrun(long transferVolumeOverrun) {
    this.transferVolumeOverrun = transferVolumeOverrun;
  }
}
