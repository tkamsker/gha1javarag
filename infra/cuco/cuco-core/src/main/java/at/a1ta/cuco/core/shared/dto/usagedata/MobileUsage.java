package at.a1ta.cuco.core.shared.dto.usagedata;

import java.io.Serializable;
import java.util.Date;

public class MobileUsage implements Serializable {
  private static final long serialVersionUID = 1L;

  private Date date;

  private Double duration;
  private Double connectionFees;
  private Double upload;
  private Double download;

  private Double gbIbData;
  private Double gbObEuData;
  private Double gbObInternationalData;

  private Double chg_ib_data;
  private Double chg_ob_eu_data;
  private Double chg_ob_international_data;

  // Minuten
  private Double mou_ib_a_othermobiles_div;
  private Double mou_ib_a_international;
  private Double mou_ib_a_national;
  private Double mou_ib_a_mobilkom;
  private Double mou_ib_a_mobilbox;
  private Double mou_ib_a_services;
  private Double sms_a_sms;

  // Euro
  private Double chg_ib_a_othermobiles_div;
  private Double chg_ib_a_international;
  private Double chg_ib_a_national;
  private Double chg_ib_a_mobilkom;
  private Double chg_ib_a_mobilbox;
  private Double chg_ib_a_services;
  private Double chg_a_sms;

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

  public Double getConnectionFees() {
    return connectionFees;
  }

  public void setConnectionFees(Double connectionFees) {
    this.connectionFees = connectionFees;
  }

  public Double getUpload() {
    return upload;
  }

  public void setUpload(Double upload) {
    this.upload = upload;
  }

  public Double getDownload() {
    return download;
  }

  public void setDownload(Double download) {
    this.download = download;
  }

  public Double getMou_ib_a_othermobiles_div() {
    return mou_ib_a_othermobiles_div;
  }

  public void setMou_ib_a_othermobiles_div(Double mou_ib_a_othermobiles_div) {
    this.mou_ib_a_othermobiles_div = mou_ib_a_othermobiles_div;
  }

  public Double getMou_ib_a_international() {
    return mou_ib_a_international;
  }

  public void setMou_ib_a_international(Double mou_ib_a_international) {
    this.mou_ib_a_international = mou_ib_a_international;
  }

  public Double getMou_ib_a_national() {
    return mou_ib_a_national;
  }

  public void setMou_ib_a_national(Double mou_ib_a_national) {
    this.mou_ib_a_national = mou_ib_a_national;
  }

  public Double getMou_ib_a_mobilkom() {
    return mou_ib_a_mobilkom;
  }

  public void setMou_ib_a_mobilkom(Double mou_ib_a_mobilkom) {
    this.mou_ib_a_mobilkom = mou_ib_a_mobilkom;
  }

  public Double getMou_ib_a_mobilbox() {
    return mou_ib_a_mobilbox;
  }

  public void setMou_ib_a_mobilbox(Double mou_ib_a_mobilbox) {
    this.mou_ib_a_mobilbox = mou_ib_a_mobilbox;
  }

  public Double getMou_ib_a_services() {
    return mou_ib_a_services;
  }

  public void setMou_ib_a_services(Double mou_ib_a_services) {
    this.mou_ib_a_services = mou_ib_a_services;
  }

  public Double getSms_a_sms() {
    return sms_a_sms;
  }

  public void setSms_a_sms(Double sms_a_sms) {
    this.sms_a_sms = sms_a_sms;
  }

  public Double getChg_ib_a_othermobiles_div() {
    return chg_ib_a_othermobiles_div;
  }

  public void setChg_ib_a_othermobiles_div(Double chg_ib_a_othermobiles_div) {
    this.chg_ib_a_othermobiles_div = chg_ib_a_othermobiles_div;
  }

  public Double getChg_ib_a_international() {
    return chg_ib_a_international;
  }

  public void setChg_ib_a_international(Double chg_ib_a_international) {
    this.chg_ib_a_international = chg_ib_a_international;
  }

  public Double getChg_ib_a_national() {
    return chg_ib_a_national;
  }

  public void setChg_ib_a_national(Double chg_ib_a_national) {
    this.chg_ib_a_national = chg_ib_a_national;
  }

  public Double getChg_ib_a_mobilkom() {
    return chg_ib_a_mobilkom;
  }

  public void setChg_ib_a_mobilkom(Double chg_ib_a_mobilkom) {
    this.chg_ib_a_mobilkom = chg_ib_a_mobilkom;
  }

  public Double getChg_ib_a_mobilbox() {
    return chg_ib_a_mobilbox;
  }

  public void setChg_ib_a_mobilbox(Double chg_ib_a_mobilbox) {
    this.chg_ib_a_mobilbox = chg_ib_a_mobilbox;
  }

  public Double getChg_ib_a_services() {
    return chg_ib_a_services;
  }

  public void setChg_ib_a_services(Double chg_ib_a_services) {
    this.chg_ib_a_services = chg_ib_a_services;
  }

  public Double getChg_a_sms() {
    return chg_a_sms;
  }

  public void setChg_a_sms(Double chg_a_sms) {
    this.chg_a_sms = chg_a_sms;
  }

  public Double getGbIbData() {
    return gbIbData;
  }

  public void setGbIbData(Double gbIbData) {
    this.gbIbData = gbIbData;
  }

  public Double getGbObEuData() {
    return gbObEuData;
  }

  public void setGbObEuData(Double gbObEuData) {
    this.gbObEuData = gbObEuData;
  }

  public Double getGbObInternationalData() {
    return gbObInternationalData;
  }

  public void setGbObInternationalData(Double gbObInternationalData) {
    this.gbObInternationalData = gbObInternationalData;
  }

  public Double getChg_ib_data() {
    return chg_ib_data;
  }

  public void setChg_ib_data(Double chg_ib_data) {
    this.chg_ib_data = chg_ib_data;
  }

  public Double getChg_ob_eu_data() {
    return chg_ob_eu_data;
  }

  public void setChg_ob_eu_data(Double chg_ob_eu_data) {
    this.chg_ob_eu_data = chg_ob_eu_data;
  }

  public Double getChg_ob_international_data() {
    return chg_ob_international_data;
  }

  public void setChg_ob_international_data(Double chg_ob_international_data) {
    this.chg_ob_international_data = chg_ob_international_data;
  }

}
