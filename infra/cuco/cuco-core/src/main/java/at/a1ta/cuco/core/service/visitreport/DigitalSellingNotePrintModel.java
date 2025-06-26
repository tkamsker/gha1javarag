package at.a1ta.cuco.core.service.visitreport;

import java.io.Serializable;

public class DigitalSellingNotePrintModel implements Serializable {

  private String title;
  private String priceOld;
  private String noteOld;
  private String priceNew;
  private String noteNew;

  public DigitalSellingNotePrintModel(String title, String priceOld, String noteOld, String priceNew, String noteNew) {
    super();
    this.title = title;
    this.priceOld = priceOld;
    this.noteOld = noteOld;
    this.priceNew = priceNew;
    this.noteNew = noteNew;
  }

  public String getTitle() {
    return title;
  }

  public void setTitle(String title) {
    this.title = title;
  }

  public String getPriceOld() {
    return priceOld;
  }

  public void setPriceOld(String priceOld) {
    this.priceOld = priceOld;
  }

  public String getNoteOld() {
    return noteOld;
  }

  public void setNoteOld(String noteOld) {
    this.noteOld = noteOld;
  }

  public String getPriceNew() {
    return priceNew;
  }

  public void setPriceNew(String priceNew) {
    this.priceNew = priceNew;
  }

  public String getNoteNew() {
    return noteNew;
  }

  public void setNoteNew(String noteNew) {
    this.noteNew = noteNew;
  }

}
