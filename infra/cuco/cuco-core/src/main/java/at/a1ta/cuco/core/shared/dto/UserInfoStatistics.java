package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class UserInfoStatistics implements Serializable {
  private int nrOfCustomers;
  private int nrOfExpiringBindings;
  private int nrOfQuotes;
  private int nrOfTasks;
  private int nrOfOpenToDos;

  public int getNrOfCustomers() {
    return nrOfCustomers;
  }

  public void setNrOfCustomers(int nrOfCustomers) {
    this.nrOfCustomers = nrOfCustomers;
  }

  public int getNrOfExpiringBindings() {
    return nrOfExpiringBindings;
  }

  public void setNrOfExpiringBindings(int nrOfExpiringBindings) {
    this.nrOfExpiringBindings = nrOfExpiringBindings;
  }

  public int getNrOfQuotes() {
    return nrOfQuotes;
  }

  public void setNrOfQuotes(int nrOfQuotes) {
    this.nrOfQuotes = nrOfQuotes;
  }

  public int getNrOfTasks() {
    return nrOfTasks;
  }

  public void setNrOfTasks(int nrOfTasks) {
    this.nrOfTasks = nrOfTasks;
  }

  public int getNrOfOpenToDos() {
    return nrOfOpenToDos;
  }

  public void setNrOfOpenToDos(int nrOfOpenToDos) {
    this.nrOfOpenToDos = nrOfOpenToDos;
  }

}
