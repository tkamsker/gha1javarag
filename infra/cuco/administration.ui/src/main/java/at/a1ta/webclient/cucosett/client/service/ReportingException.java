package at.a1ta.webclient.cucosett.client.service;

import java.io.Serializable;

public class ReportingException extends RuntimeException implements Serializable {

  public ReportingException() {
    super();
  }

  public ReportingException(String string) {
    super(string);
  }

}
