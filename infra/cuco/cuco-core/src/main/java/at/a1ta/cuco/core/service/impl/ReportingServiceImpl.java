package at.a1ta.cuco.core.service.impl;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.HashMap;
import java.util.List;

import org.apache.poi.hssf.usermodel.HSSFCell;
import org.apache.poi.hssf.usermodel.HSSFRow;
import org.apache.poi.hssf.usermodel.HSSFSheet;
import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.DataFormat;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.bean.File;
import at.a1ta.cuco.core.bean.File.MIMEType;
import at.a1ta.cuco.core.bean.Reporting;
import at.a1ta.cuco.core.dao.db.ReportingDao;
import at.a1ta.cuco.core.service.ReportingService;

@Service
public class ReportingServiceImpl implements ReportingService {

  private static final Logger logger = LoggerFactory.getLogger(ReportingServiceImpl.class);

  @Autowired
  private ReportingDao reportingDao;

  @Override
  public Reporting getReporting(int id) {
    return reportingDao.getReporting(id);
  }

  @Override
  public List<Reporting> getAllReportings() {
    return reportingDao.getAllReportings();
  }

  @Override
  public List<HashMap<String, Object>> executeReporting(long id) {
    logger.info("User executes report " + id);

    Reporting reporting = reportingDao.getReporting(id);
    if (reporting.isLongRunning()) {
      String query = "select * from custc." + reporting.getTableName();
      return reportingDao.executeReporting(query);
    }
    return reportingDao.executeReporting(reporting.getQuery());
  }

  @Override
  public File exportReportAsExcel(Long id) {
    List<HashMap<String, Object>> data = executeReporting(id);

    HSSFWorkbook workbook = new HSSFWorkbook();
    HSSFSheet sheet = workbook.createSheet("Report");

    DataFormat format = workbook.createDataFormat();
    CellStyle style = workbook.createCellStyle();
    style.setDataFormat(format.getFormat("0.00"));

    int rowIdx = 0;
    int colIdx = 0;

    // Header
    HSSFRow row = sheet.createRow(rowIdx);
    if (data.size() > 0) {
      for (String key : data.get(0).keySet()) {
        HSSFCell cell = row.createCell(colIdx, HSSFCell.CELL_TYPE_STRING);
        cell.setCellValue(key);
        colIdx++;
      }
      colIdx = 0;
      rowIdx++;

      for (HashMap<String, Object> datum : data) {
        row = sheet.createRow(rowIdx);
        for (String key : datum.keySet()) {
          Object val = datum.get(key);
          if (val != null) {
            HSSFCell cell = row.createCell(colIdx, getCellTypeForValue(val));
            if (val instanceof Integer) {
              cell.setCellValue((Integer) val);
            } else if (val instanceof Long) {
              cell.setCellValue((Long) val);
            } else if (val instanceof Float) {
              cell.setCellValue((Float) val);
              cell.setCellStyle(style);
            } else if (val instanceof Double) {
              cell.setCellValue((Double) val);
              cell.setCellStyle(style);
            } else if (val instanceof BigInteger) {
              cell.setCellValue(((BigInteger) val).doubleValue());
            } else if (val instanceof BigDecimal) {
              cell.setCellValue(((BigDecimal) val).doubleValue());
              cell.setCellStyle(style);
            } else {
              cell.setCellValue(val.toString());
            }
          }
          colIdx++;
        }
        colIdx = 0;
        rowIdx++;
      }

      for (int i = 0; i < data.get(0).size(); i++) {
        sheet.autoSizeColumn(i);
      }
    } else {
      HSSFCell cell = row.createCell(colIdx, HSSFCell.CELL_TYPE_STRING);
      cell.setCellValue("No data found.");
    }

    File file = new File("export.xls", MIMEType.XLS);
    ByteArrayOutputStream bos = new ByteArrayOutputStream();
    try {
      workbook.write(bos);
    } catch (IOException e) {
      throw new RuntimeException(e);
    }
    file.setContent(bos.toByteArray());
    return file;
  }

  private int getCellTypeForValue(Object object) {
    if (object instanceof Long || object instanceof Double || object instanceof Float || object instanceof Integer || object instanceof BigInteger || object instanceof BigDecimal) {
      return HSSFCell.CELL_TYPE_NUMERIC;
    }
    return HSSFCell.CELL_TYPE_STRING;
  }
}
