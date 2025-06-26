package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;

public class ProductGroup implements Serializable {
  private Long id;
  private String code;
  private String name;
  private String description;
  private String anbLookup;
  private Date updateTs;
  private int nrNotes;
  private int nrNotesImported;
  private int nrSingleTurnarounds;
  private int nrReminders;
  private boolean ta;
  private boolean anb;
  private boolean notInterested;
  private ArrayList<RTCode> rtCodes = new ArrayList<RTCode>();

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getCode() {
    return code;
  }

  public void setCode(String code) {
    this.code = code;
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

  public String getAnbLookup() {
    return anbLookup;
  }

  public void setAnbLookup(String anbLookup) {
    this.anbLookup = anbLookup;
  }

  public Date getUpdateTs() {
    return updateTs;
  }

  public void setUpdateTs(Date updateTs) {
    this.updateTs = updateTs;
  }

  public void setNrNotes(int nrNotes) {
    this.nrNotes = nrNotes;
  }

  public int getNrNotes() {
    return nrNotes;
  }

  public int getNrNotesImported() {
    return nrNotesImported;
  }

  public void setNrNotesImported(int nrNotesImported) {
    this.nrNotesImported = nrNotesImported;
  }

  public void setNrSingleTurnarounds(int nrSingleTurnarounds) {
    this.nrSingleTurnarounds = nrSingleTurnarounds;
  }

  public int getNrSingleTurnarounds() {
    return this.nrSingleTurnarounds;
  }

  public int getNrReminders() {
    return nrReminders;
  }

  public void setNrReminders(int nrReminders) {
    this.nrReminders = nrReminders;
  }

  public boolean hasTa() {
    return ta;
  }

  public void setTa(boolean ta) {
    this.ta = ta;
  }

  public boolean hasAnb() {
    return anb;
  }

  public void setAnb(boolean anb) {
    this.anb = anb;
  }

  public ArrayList<RTCode> getRTCodes() {
    return rtCodes;
  }

  public void setRTCodes(ArrayList<RTCode> codes) {
    this.rtCodes = codes;
  }

  public void setNotInterested(boolean notInterested) {
    this.notInterested = notInterested;
  }

  public boolean isNotInterested() {
    return notInterested;
  }

  @Override
  public String toString() {
    return name;
  }
}
