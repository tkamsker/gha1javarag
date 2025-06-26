package at.a1ta.cuco.core.shared.dto.usagedata;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class UsageDetail implements Serializable {
  private static final long serialVersionUID = 1L;

  private static final int MOBILE_ATTR_COUNT = 14;

  private Date date;
  private String tarif;
  private Double value;
  private Double fee;

  public static ArrayList<UsageDetail> createFromVoiceUsage(List<VoiceUsage> usages) {
    ArrayList<UsageDetail> lst = new ArrayList<UsageDetail>(usages.size());
    for (VoiceUsage usage : usages) {
      lst.add(create(usage));
    }
    return lst;
  }

  private static UsageDetail create(VoiceUsage usage) {
    UsageDetail o = new UsageDetail();
    o.date = usage.getDate();
    o.tarif = usage.getZone();
    o.value = usage.getDuration();
    o.fee = usage.getConnectionFee();
    return o;
  }

  public static ArrayList<UsageDetail> createFromMobileUsage(List<MobileUsage> usages) {
    ArrayList<UsageDetail> lst = new ArrayList<UsageDetail>(usages.size() * MOBILE_ATTR_COUNT * 2);
    for (MobileUsage usage : usages) {
      lst.addAll(create(usage));
    }
    return lst;
  }

  private static ArrayList<UsageDetail> create(MobileUsage usage) {
    ArrayList<UsageDetail> lst = new ArrayList<UsageDetail>(MOBILE_ATTR_COUNT * 2);
    lst.add(create(usage, usage.getMou_ib_a_national(), usage.getChg_ib_a_national(), "National ins Festnetz"));
    lst.add(create(usage, usage.getMou_ib_a_mobilkom(), usage.getChg_ib_a_mobilkom(), "Mobilkom"));
    lst.add(create(usage, usage.getMou_ib_a_mobilbox(), usage.getChg_ib_a_mobilbox(), "Mobilbox"));
    lst.add(create(usage, usage.getMou_ib_a_services(), usage.getChg_ib_a_services(), "Servicenummern"));
    lst.add(create(usage, usage.getMou_ib_a_othermobiles_div(), usage.getChg_ib_a_othermobiles_div(), "andere Mobilnetze"));
    lst.add(create(usage, usage.getMou_ib_a_international(), usage.getChg_ib_a_international(), "Internationale Anrufe"));
    lst.add(create(usage, usage.getSms_a_sms(), usage.getChg_a_sms(), "SMS"));
    lst.add(create(usage, usage.getGbIbData(), usage.getChg_ib_data(), "Datenvolumen Inland"));
    lst.add(create(usage, usage.getGbObEuData(), usage.getChg_ob_eu_data(), "Datenvolumen EU"));
    lst.add(create(usage, usage.getGbObInternationalData(), usage.getChg_ob_international_data(), "Datenvolumen International"));

    return lst;
  }

  private static UsageDetail create(MobileUsage usage, Double minutes, Double fee, String tarifName) {
    UsageDetail o = new UsageDetail();
    o.date = usage.getDate();
    o.tarif = tarifName;
    o.value = minutes;
    o.fee = fee;
    return o;
  }

  public UsageDetail() {}

  public Date getDate() {
    return date;
  }

  public void setDate(Date date) {
    this.date = date;
  }

  public String getAttributeName() {
    return tarif;
  }

  public void setAttributeName(String attributeName) {
    this.tarif = attributeName;
  }

  public Double getMinutes() {
    return value;
  }

  public void setMinutes(Double minutes) {
    this.value = minutes;
  }

  public Double getFee() {
    return fee;
  }

  public void setFee(Double fee) {
    this.fee = fee;
  }
}
