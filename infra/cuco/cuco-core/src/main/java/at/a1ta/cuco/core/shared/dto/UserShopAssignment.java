package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class UserShopAssignment implements Serializable {
  
  private String userName; 
  private String shopID;
  
  public UserShopAssignment() 
  {
    this.userName = "";
    this.shopID = "";
  }
  
  public UserShopAssignment(String userName, String shopID) {
    this.userName = userName; 
    this.shopID = shopID;
  }
  
  public String getUserName() {
    return userName;
  }
  public void setUserName(String userName) {
    this.userName = userName;
  }
  public String getShopID() {
    return shopID;
  }
  public void setShopID(String shopID) {
    this.shopID = shopID;
  } 
}
