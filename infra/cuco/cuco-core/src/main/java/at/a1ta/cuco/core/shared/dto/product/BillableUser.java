package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;

public class BillableUser implements Serializable {
  private static final long serialVersionUID = 1L;
  private String userName;

  public BillableUser() {
    // Do Nothing because default constructor.
  }

  public BillableUser(String userName) {
    this.userName = userName;
  }

  public String getUserName() {
    return userName;
  }

  public void setUserName(String userName) {
    this.userName = userName;
  }

  @Override
  public String toString() {
    return userName;
  }
}
