package at.a1ta.cuco.core.bean;

import java.io.Serializable;

public class PWUTokenResponse implements Serializable {
  private String a1Login;
  private String orderId;
  private String retailerId;
  private String token;
  private String firstName;
  private String lastName;
  private long invokationDuration = -1;
  private String partyId;

  public String getA1Login() {
    return a1Login;
  }

  public void setA1Login(String a1Login) {
    this.a1Login = a1Login;
  }

  public String getOrderId() {
    return orderId;
  }

  public void setOrderId(String orderId) {
    this.orderId = orderId;
  }

  public String getRetailerId() {
    return retailerId;
  }

  public void setRetailerId(String retailerId) {
    this.retailerId = retailerId;
  }

  public String getToken() {
    return token;
  }

  public void setToken(String token) {
    this.token = token;
  }

  public long getInvokationDuration() {
    return invokationDuration;
  }

  public void setInvokationDuration(long invokationDuration) {
    this.invokationDuration = invokationDuration;
  }

  public String getFirstName() {
    return firstName;
  }

  public void setFirstName(String firstName) {
    this.firstName = firstName;
  }

  public String getLastName() {
    return lastName;
  }

  public void setLastName(String lastName) {
    this.lastName = lastName;
  }

  @Override
  public String toString() {
    return "PWUTokenResponse [a1Login=" + a1Login + ", orderId=" + orderId + ", retailerId=" + retailerId + ", token=" + token + ", firstname=" + firstName + ", lastname=" + lastName + ", invokationDuration=" + invokationDuration + "]";
  }

  public String getPartyId() {
    return partyId;
  }

  public void setPartyId(String partyId) {
    this.partyId = partyId;
  }
}
