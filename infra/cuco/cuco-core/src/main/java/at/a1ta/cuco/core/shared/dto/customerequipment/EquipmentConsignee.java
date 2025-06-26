package at.a1ta.cuco.core.shared.dto.customerequipment;

import java.io.Serializable;

public class EquipmentConsignee implements Serializable {
  private String id;
  private String summaryShort;
  private String summary;
  private long partyId;

  private String title;
  private String name1;
  private String name2;
  private String plz;
  private String city;
  private String street;
  private String houseNumber;
  private String consignee;

  public String getSummaryShort() {
    return summaryShort;
  }

  public void setSummaryShort(String summaryShort) {
    this.summaryShort = summaryShort;
  }

  public void setSummary(String summary) {
    this.summary = summary;
  }

  public String getSummary() {
    return summary;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public long getPartyId() {
    return partyId;
  }

  public void setPartyId(long partyId) {
    this.partyId = partyId;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public String getName1() {
    return name1;
  }

  public void setName1(String name1) {
    this.name1 = name1;
  }

  public String getName2() {
    return name2;
  }

  public void setName2(String name2) {
    this.name2 = name2;
  }

  public String getPlz() {
    return plz;
  }

  public void setPlz(String plz) {
    this.plz = plz;
  }

  public String getCity() {
    return city;
  }

  public void setCity(String city) {
    this.city = city;
  }

  public String getStreet() {
    return street;
  }

  public void setStreet(String street) {
    this.street = street;
  }

  public String getHouseNumber() {
    return houseNumber;
  }

  public void setHouseNumber(String houseNumber) {
    this.houseNumber = houseNumber;
  }

  public String getConsignee() {
    return consignee;
  }

  public void setConsignee(String consignee) {
    this.consignee = consignee;
  }

  @Override
  public boolean equals(Object obj) {
    if (obj instanceof EquipmentConsignee) {
      return id != null && id.equals(((EquipmentConsignee) obj).getId());
    }
    return false;
  }

  @Override
  public int hashCode() {
    return id == null ? 0 : id.hashCode();
  }
}
