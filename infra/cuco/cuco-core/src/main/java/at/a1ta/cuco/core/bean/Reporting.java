package at.a1ta.cuco.core.bean;

import java.io.Serializable;

public class Reporting implements Serializable, KeyableBean {
  private Long id;
  private String name;
  private String query;
  private boolean longRunning;
  private String tableName;

  @Override
  public Long getId() {
    return id;
  }

  public String getQuery() {
    return query;
  }

  public void setQuery(String query) {
    this.query = query;
  }

  public boolean isLongRunning() {
    return longRunning;
  }

  public void setLongRunning(boolean longrunning) {
    this.longRunning = longrunning;
  }

  public String getTableName() {
    return tableName;
  }

  public void setTableName(String tablename) {
    this.tableName = tablename;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public void setName(String name) {
    this.name = name;
  }

  public String getName() {
    return name;
  }
}
