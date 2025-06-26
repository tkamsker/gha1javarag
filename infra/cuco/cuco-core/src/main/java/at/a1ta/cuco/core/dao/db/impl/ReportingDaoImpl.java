package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.bean.Reporting;
import at.a1ta.cuco.core.dao.db.ReportingDao;

public class ReportingDaoImpl extends AbstractDao implements ReportingDao {

  @Override
  public Reporting getReporting(long id) {
    return performObjectQuery("Reporting.get", id);
  }

  @Override
  public List<Reporting> getAllReportings() {
    return performListQuery("Reporting.get");
  }

  @Override
  public List<HashMap<String, Object>> executeReporting(String stmt) {
    return performListQuery("Reporting.execute", stmt);
  }
}
