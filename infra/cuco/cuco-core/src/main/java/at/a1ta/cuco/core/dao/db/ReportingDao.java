package at.a1ta.cuco.core.dao.db;

import java.util.HashMap;
import java.util.List;

import at.a1ta.cuco.core.bean.Reporting;

public interface ReportingDao {

  public Reporting getReporting(long id);

  public List<Reporting> getAllReportings();

  public List<HashMap<String, Object>> executeReporting(String stmt);
}
