package at.a1ta.cuco.core.shared.dto.salesinfo.visitreport.generic;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.salesinfo.SalesInfoNote;

public class GenericNote extends SalesInfoNote {
  private List<FileAttachment> fileAttachments;

  /**
   * Copy Constructor
   * 
   * @param genericNote a <code>GenericNote</code> object
   */
  public GenericNote(GenericNote genericNote) {
    super(genericNote);
    this.fileAttachments = genericNote.fileAttachments;
  }
  
  public GenericNote() {
    super();
    
  }
  

  public List<FileAttachment> getFileAttachments() {
    return fileAttachments;
  }

  public void setFileAttachments(List<FileAttachment> fileAttachments) {
    this.fileAttachments = fileAttachments;
  }

  @Override
  public String toString() {
    return "GenericReport [super.toString()=" + super.toString() + ", fileAttachments=" + fileAttachments + "]";
  }
}
