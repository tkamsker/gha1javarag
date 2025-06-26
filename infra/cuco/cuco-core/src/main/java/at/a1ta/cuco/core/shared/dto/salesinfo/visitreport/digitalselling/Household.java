package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.digitalselling;

import java.io.Serializable;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;

@XmlAccessorType(XmlAccessType.FIELD)
public class Household implements Serializable {
  private static final long serialVersionUID = 1L;

  private HouseholdType type; // Typ des Haushalts
  private Integer size; // Größe
  private Integer floor; // Stockwerke
  private Integer persons; // Personen im haushalt
  private Integer devices; // Anzahl der Geräte
  private String mail; // Mailadresse
  private String phone; // Rückrufnummer
  private String noteText; // Freitextfeld

  public HouseholdType getType() {
    return type;
  }

  public void setType(HouseholdType type) {
    this.type = type;
  }

  public Integer getSize() {
    return size;
  }

  public void setSize(Integer size) {
    this.size = size;
  }

  public Integer getFloor() {
    return floor;
  }

  public void setFloor(Integer floor) {
    this.floor = floor;
  }

  public Integer getPersons() {
    return persons;
  }

  public void setPersons(Integer persons) {
    this.persons = persons;
  }

  public Integer getDevices() {
    return devices;
  }

  public void setDevices(Integer devices) {
    this.devices = devices;
  }

  public String getMail() {
    return mail;
  }

  public void setMail(String mail) {
    this.mail = mail;
  }

  public String getPhone() {
    return phone;
  }

  public void setPhone(String phone) {
    this.phone = phone;
  }

  public String getNoteText() {
    return noteText;
  }

  public void setNoteText(String noteText) {
    this.noteText = noteText;
  }

  @Override
  public String toString() {
    return "Household [type=" + type + ", size=" + size + ", floor=" + floor + ", persons=" + persons + ", devices=" + devices + ", mail=" + mail + ", phone=" + phone + ", noteText=" + noteText + "]";
  }

  @Override
  public int hashCode() {
    // TODO Auto-generated method stub
    return super.hashCode();
  }

  @Override
  public boolean equals(Object obj) {
    // TODO Auto-generated method stub
    return super.equals(obj);
  }

}
