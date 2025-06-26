package at.a1ta.cuco.core.shared.dto.salesinfo.salesconvnote;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class ProductHistoryItem implements Serializable {

  private Long id;
  private Long productNoteId;
  private String note;
  private BiteUser creationUser;
  private Date creationDate;

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public String getNote() {
    return note;
  }

  public void setNote(String note) {
    this.note = note;
  }

  public Long getProductNoteId() {
    return productNoteId;
  }

  public void setProductNoteId(Long productNoteId) {
    this.productNoteId = productNoteId;
  }

  public BiteUser getCreationUser() {
    return creationUser;
  }

  public void setCreationUser(BiteUser creationUser) {
    this.creationUser = creationUser;
  }

  public Date getCreationDate() {
    return creationDate;
  }

  public void setCreationDate(Date creationDate) {
    this.creationDate = creationDate;
  }

}
