package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class CCTOrgStructureElement implements Serializable {
  private static final long serialVersionUID = 1L;
  private String userID;
  private int approvalLevel;
  private String supervisorUserID;
  private String user;
  private String supervisor;
  private BiteUser userDetails;
  private BiteUser supervisorDetails;
  private String team;
  private String role;
  private String orgId;
  private String rolle;

  @Override
  public String toString() {
    return userID + " " + approvalLevel + " " + supervisorUserID;
  }

  public String getSupervisor() {
    return supervisor;
  }

  public void setSupervisor(String string) {
    this.supervisor = string;
  }

  public String getUserID() {
    return userID;
  }

  public void setUserID(String userID) {
    this.userID = userID;
  }

  public int getApprovalLevel() {
    return approvalLevel;
  }

  public void setApprovalLevel(int i) {
    this.approvalLevel = i;
  }

  public String getSupervisorUserID() {
    return supervisorUserID;
  }

  public void setSupervisorUserID(String supervisorUserID) {
    this.supervisorUserID = supervisorUserID;
  }

  public static long getSerialversionuid() {
    return serialVersionUID;
  }

  public String getUser() {
    return user;
  }

  public void setUser(String user) {
    this.user = user;
  }

  public String getTeam() {
    return team;
  }

  public void setTeam(String team) {
    this.team = team;
  }

  public String getRole() {
    return role;
  }

  public void setRole(String role) {
    this.role = role;
  }

  public String getOrgId() {
    return orgId;
  }

  public void setOrgId(String orgId) {
    this.orgId = orgId;
  }

  public BiteUser getUserDetails() {
    return userDetails;
  }

  public void setUserDetails(BiteUser userDetails) {
    this.userDetails = userDetails;
  }

  public BiteUser getSupervisorDetails() {
    return supervisorDetails;
  }

  public void setSupervisorDetails(BiteUser supervisorDetails) {
    this.supervisorDetails = supervisorDetails;
  }

  public String getRolle() {
    return rolle;
  }

  public void setRolle(String rolle) {
    this.rolle = rolle;
  }

}
