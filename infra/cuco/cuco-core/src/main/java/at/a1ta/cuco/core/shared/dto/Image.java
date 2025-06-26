package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

public class Image implements Serializable {
  private Long id;
  private String uuser;
  private String filename;
  private String name;
  private Date creationDate;
  private Long imageSizeId;

  public Long getId() {
    return this.id;
  }

  public String getUuser() {
    return this.uuser;
  }

  public String getFilename() {
    return this.filename;
  }

  public String getName() {
    return this.name;
  }

  public Date getCreationDate() {
    return this.creationDate;
  }

  public Long getImageSizeId() {
    return this.imageSizeId;
  }

  public void setId(final Long id) {
    this.id = id;
  }

  public void setUuser(final String uuser) {
    this.uuser = uuser;
  }

  public void setFilename(final String filename) {
    this.filename = filename;
  }

  public void setName(final String name) {
    this.name = name;
  }

  public void setCreationDate(final Date creationDate) {
    this.creationDate = creationDate;
  }

  public void setImageSizeId(final Long imageSizeId) {
    this.imageSizeId = imageSizeId;
  }
}