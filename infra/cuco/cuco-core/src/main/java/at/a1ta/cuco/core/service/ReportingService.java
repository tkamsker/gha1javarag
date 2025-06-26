package at.a1ta.cuco.core.service;

import java.util.HashMap;
import java.util.List;

import at.a1ta.cuco.core.bean.File;
import at.a1ta.cuco.core.bean.Reporting;

public interface ReportingService {

  public Reporting getReporting(int id);

  public List<Reporting> getAllReportings();

  public List<HashMap<String, Object>> executeReporting(long id);

  public File exportReportAsExcel(Long id);
}
