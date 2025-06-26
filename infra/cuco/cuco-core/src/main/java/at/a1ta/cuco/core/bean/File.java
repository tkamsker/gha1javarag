package at.a1ta.cuco.core.bean;

import java.io.Serializable;

public class File implements Serializable {
  private static final long serialVersionUID = 1L;

  public enum MIMEType {
    //@formatter:off
    PNG("image/png"), 
    CSV("text/csv"), 
    PDF("application/pdf"), 
    XLS("application/x-excel"), 
    XLSX("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"), 
    XML("application/xml");
    //@formatter:on

    private String value;

    private MIMEType(String value) {
      this.value = value;
    }

    public String getValue() {
      return value;
    }
  }

  private String filename;
  private byte[] content;
  private MIMEType mimeType;

  public File() {}

  public File(String filename, MIMEType mimeType) {
    this.filename = filename;
    this.mimeType = mimeType;
  }

  public String getFilename() {
    return filename;
  }

  public void setFilename(String filename) {
    this.filename = filename;
  }

  public byte[] getContent() {
    return content;
  }

  public void setContent(byte[] content) {
    this.content = content;
  }

  public MIMEType getMimeType() {
    return mimeType;
  }

  public void setMimeType(MIMEType mimeType) {
    this.mimeType = mimeType;
  }
}
