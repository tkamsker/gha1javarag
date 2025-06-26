package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.generic;

import java.io.Serializable;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class FileAttachment implements Serializable {

  /**
   * Copy Constructor
   * 
   * @param fileAttachment a <code>FileAttachment</code> object
   */
  public FileAttachment(FileAttachment fileAttachment) {
    this.salesInfoNoteId = fileAttachment.salesInfoNoteId;
    this.fileAttachmentId = fileAttachment.fileAttachmentId;
    this.fileName = fileAttachment.fileName;
    this.creationUser = fileAttachment.creationUser;
    this.creationTimestamp = fileAttachment.creationTimestamp;
    this.checked = fileAttachment.checked;
  }

  public FileAttachment() {
    super();
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + (checked ? 1231 : 1237);
    result = prime * result + ((creationTimestamp == null) ? 0 : creationTimestamp.hashCode());
    result = prime * result + ((creationUser == null) ? 0 : creationUser.hashCode());
    result = prime * result + (int) (fileAttachmentId ^ (fileAttachmentId >>> 32));
    result = prime * result + ((fileName == null) ? 0 : fileName.hashCode());
    result = prime * result + (int) (salesInfoNoteId ^ (salesInfoNoteId >>> 32));
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (obj == null) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    FileAttachment other = (FileAttachment) obj;
    if (checked != other.checked) {
      return false;
    }
    if (creationTimestamp == null) {
      if (other.creationTimestamp != null) {
        return false;
      }
    } else if (!creationTimestamp.equals(other.creationTimestamp)) {
      return false;
    }
    if (creationUser == null) {
      if (other.creationUser != null) {
        return false;
      }
    } else if (!creationUser.equals(other.creationUser)) {
      return false;
    }
    if (fileAttachmentId != other.fileAttachmentId) {
      return false;
    }
    if (fileName == null) {
      if (other.fileName != null) {
        return false;
      }
    } else if (!fileName.equals(other.fileName)) {
      return false;
    }
    if (salesInfoNoteId != other.salesInfoNoteId) {
      return false;
    }
    return true;
  }

  private long salesInfoNoteId;
  private long fileAttachmentId;
  private String fileName;
  private BiteUser creationUser;
  private Date creationTimestamp;

  private boolean checked = false;

  public long getSalesInfoNoteId() {
    return salesInfoNoteId;
  }

  public void setSalesInfoNoteId(long salesInfoNoteId) {
    this.salesInfoNoteId = salesInfoNoteId;
  }

  public long getFileAttachmentId() {
    return fileAttachmentId;
  }

  public void setFileAttachmentId(long fileAttachmentId) {
    this.fileAttachmentId = fileAttachmentId;
  }

  public String getFileName() {
    return fileName;
  }

  public void setFileName(String fileName) {
    this.fileName = fileName;
  }

  public BiteUser getCreationUser() {
    return creationUser;
  }

  public void setCreationUser(BiteUser creationUser) {
    this.creationUser = creationUser;
  }

  public Date getCreationTimestamp() {
    return creationTimestamp;
  }

  public void setCreationTimestamp(Date creationTimestamp) {
    this.creationTimestamp = creationTimestamp;
  }

  @Override
  public String toString() {
    return "FileAttachment [fileAttachmentId=" + fileAttachmentId + ", fileName=" + fileName + ", creationUser=" + creationUser + ", creationTimestamp=" + creationTimestamp + "]";
  }

  public boolean isChecked() {
    return checked;
  }

  public void setChecked(boolean checked) {
    this.checked = checked;
  }

}
