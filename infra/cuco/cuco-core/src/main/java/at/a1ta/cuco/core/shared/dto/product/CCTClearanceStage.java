package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class CCTClearanceStage implements Serializable {
  private static final long serialVersionUID = 1L;
  private String productOfferingId;
  private String quoteNumber;
  private String login;
  private String name;
  private BiteUser user;
  private BiteUser defaultSupervisor;
  private String comments;
  private String email;
  private Date changeDate;
  private String status;
  private int orgLevel;
  private ArrayList<CCTOrgStructureElement> otherSupervisors = new ArrayList<CCTOrgStructureElement>();

  public String getProductOfferingId() {
    return productOfferingId;
  }

  public void setProductOfferingId(String productOfferingId) {
    this.productOfferingId = productOfferingId;
  }

  public String getQuoteNumber() {
    return quoteNumber;
  }

  public void setQuoteNumber(String quoteNumber) {
    this.quoteNumber = quoteNumber;
  }

  public String getLogin() {
    return login;
  }

  public void setLogin(String login) {
    this.login = login;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getComments() {
    return comments;
  }

  public void setComments(String comments) {
    this.comments = comments;
  }

  public String getEmail() {
    return email;
  }

  public void setEmail(String email) {
    this.email = email;
  }

  public Date getChangeDate() {
    return changeDate;
  }

  public void setChangeDate(Date changeDate) {
    this.changeDate = changeDate;
  }

  public String getStatus() {
    return status;
  }

  public void setStatus(String status) {
    this.status = status;
  }

  public int getOrgLevel() {
    return orgLevel;
  }

  public void setOrgLevel(int orgLevel) {
    this.orgLevel = orgLevel;
  }

  public static long getSerialversionuid() {
    return serialVersionUID;
  }

  public ArrayList<CCTOrgStructureElement> getOtherSupervisors() {
    return otherSupervisors;
  }

  public void setOtherSupervisors(ArrayList<CCTOrgStructureElement> otherSupervisors) {
    this.otherSupervisors = otherSupervisors;
  }

  public BiteUser getUser() {
    return user;
  }

  public void setUser(BiteUser user) {
    this.user = user;
  }

  public BiteUser getDefaultSupervisor() {
    return defaultSupervisor;
  }

  public void setDefaultSupervisor(BiteUser defaultSupervisor) {
    this.defaultSupervisor = defaultSupervisor;
  }

}
