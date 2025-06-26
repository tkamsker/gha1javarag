package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class CCTSupervisorSelect implements Serializable {
  private static final long serialVersionUID = 1L;
  private String superVisor; // mitarbeiter
  private int approvalLevel; // stufe
  private String release; // freigabe
  private String date;
  private String comment;

  public String getSuperVisor() {
    return superVisor;
  }

  public void setSuperVisor(String superVisor) {
    this.superVisor = superVisor;
  }

  public int getApprovalLevel() {
    return approvalLevel;
  }

  public void setApprovalLevel(int approvalLevel) {
    this.approvalLevel = approvalLevel;
  }

  public String getRelease() {
    return release;
  }

  public void setRelease(String release) {
    this.release = release;
  }

  public String getDate() {
    return date;
  }

  public void setDate(String date) {
    this.date = date;
  }

  public String getComment() {
    return comment;
  }

  public void setComment(String comment) {
    this.comment = comment;
  }

  public static long getSerialversionuid() {
    return serialVersionUID;
  }

}
