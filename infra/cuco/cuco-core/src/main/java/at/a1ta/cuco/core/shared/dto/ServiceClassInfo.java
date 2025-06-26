package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class ServiceClassInfo implements Serializable {

  /**
   * 
   */
  private static final long serialVersionUID = 1L;
  private int serviceClass = SERVICE_CLASS_LOADING;
  private String serviceClassText;
  public static final int SERVICE_CLASS_ERROR = 99;
  public static final int SERVICE_CLASS_LOADING = -1;
  public static final int SERVICE_CLASS_NOT_RECEIVED = 98;

  public ServiceClassInfo() {
    // default constructor to support GWT parsing
  }

  public ServiceClassInfo(int serviceClass, String serviceClassText) {
    this.serviceClass = serviceClass;
    this.serviceClassText = serviceClassText;
  }

  public int getServiceClass() {
    return serviceClass;
  }

  public void setServiceClass(int serviceClass) {
    this.serviceClass = serviceClass;
  }

  public String getServiceClassText() {
    return serviceClassText;
  }

  public void setServiceClassText(String serviceClassText) {
    this.serviceClassText = serviceClassText;
  }

}
