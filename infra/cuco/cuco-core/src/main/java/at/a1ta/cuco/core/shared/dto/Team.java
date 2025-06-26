package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import at.a1ta.bite.core.shared.dto.BiteUser;

public class Team implements Serializable {
  private Long id;
  private String name;
  private String description;
  private BiteUser creator;
  private Date createDate;
  private List<BiteUser> members = new ArrayList<BiteUser>();
  private List<Service> services = new ArrayList<Service>();

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
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

  public List<BiteUser> getMembers() {
    return members;
  }

  public void setMembers(List<BiteUser> members) {
    this.members = members;
  }

  public BiteUser getCreator() {
    return creator;
  }

  public void setCreator(BiteUser creator) {
    this.creator = creator;
  }

  public Date getCreateDate() {
    return createDate;
  }

  public void setCreateDate(Date createDate) {
    this.createDate = createDate;
  }

  public List<Service> getServices() {
    return services;
  }

  public void setServices(List<Service> services) {
    this.services = services;
  }
}
