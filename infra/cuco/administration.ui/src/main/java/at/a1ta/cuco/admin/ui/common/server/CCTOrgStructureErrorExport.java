package at.a1ta.cuco.admin.ui.common.server;

import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.poi.hssf.usermodel.HSSFWorkbook;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.CellStyle;
import org.apache.poi.ss.usermodel.Font;
import org.apache.poi.ss.usermodel.IndexedColors;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import at.a1ta.bite.core.server.service.TextService;
import at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement;

@Component
@Scope("prototype")
public class CCTOrgStructureErrorExport {

  private static String HEADER_STYLE = "header";
  private static String DATE_STYLE = "date";

  private TextService textService;
  private List<String> supervisorNotUserList = new ArrayList<String>();
  private List<String> userNotInDBList = new ArrayList<String>();
  private String fileName;

  private final Map<String, CellStyle> styles = new HashMap<String, CellStyle>();

  public void createExcelExport(final OutputStream response, ArrayList<CCTOrgStructureElement> mismatchedIds, TextService textService2, List<String> supervisorNotUserList,
      List<String> userNotInDBList, String fileName) throws IOException {
    this.textService = textService2;
    this.supervisorNotUserList = supervisorNotUserList;
    this.userNotInDBList = userNotInDBList;
    this.setFileName(fileName);
    Workbook wb = fileName.endsWith(".xls") ? new HSSFWorkbook() : new XSSFWorkbook();
    if (mismatchedIds.size() > 500) {
      wb = fileName.endsWith(".xls") ? new HSSFWorkbook() : new XSSFWorkbook();
    }
    createStyles(wb);

    Sheet sheet = wb.createSheet("errors");
    addHeaderRow(sheet);

    int rowIndex = 1;
    for (CCTOrgStructureElement cCTOrgID : mismatchedIds) {
      addCCTOrgStructureElementRow(sheet, rowIndex, cCTOrgID);
      rowIndex++;
    }

    sizeColumns(sheet);
    wb.write(response);
    response.flush();
  }

  private void addHeaderRow(Sheet sheet) {
    Row headerRow = sheet.createRow(0);
    addHeaderColumn(headerRow, 0, loadTextFromBundle("admin_exportUserId"));
    addHeaderColumn(headerRow, 1, loadTextFromBundle("admin_exportUserName"));
    addHeaderColumn(headerRow, 2, loadTextFromBundle("admin_exportUserRolle"));
    addHeaderColumn(headerRow, 3, loadTextFromBundle("admin_exportRole"));
    addHeaderColumn(headerRow, 4, loadTextFromBundle("admin_exportLevel"));
    addHeaderColumn(headerRow, 5, loadTextFromBundle("admin_exportTeam"));
    addHeaderColumn(headerRow, 6, loadTextFromBundle("admin_exportSAPId"));
    addHeaderColumn(headerRow, 7, loadTextFromBundle("admin_exportSupervisorID"));
    addHeaderColumn(headerRow, 8, loadTextFromBundle("admin_exportSupervisorName"));
    addHeaderColumn(headerRow, 9, loadTextFromBundle("admin_exportFailureReason"));
  }

  private String loadTextFromBundle(String key) {
    return textService.getByKey(key).getText();
  }

  private void addHeaderColumn(Row row, int index, String text) {
    Cell cell = row.createCell(index);
    cell.setCellStyle(styles.get(HEADER_STYLE));
    cell.setCellValue(text);
  }

  private void addCCTOrgStructureElementRow(Sheet sheet, int rowIndex, CCTOrgStructureElement cCTOrgStructureElement) {
    Row row = sheet.createRow(rowIndex);

    addCCTOrgStructureElementColumn(row, 0, cCTOrgStructureElement.getUserID());
    addCCTOrgStructureElementColumn(row, 1, cCTOrgStructureElement.getUser());
    addCCTOrgStructureElementColumn(row, 2, cCTOrgStructureElement.getRolle());
    addCCTOrgStructureElementColumn(row, 3, cCTOrgStructureElement.getRole());
    addCCTOrgStructureElementColumn(row, 4, cCTOrgStructureElement.getApprovalLevel());
    addCCTOrgStructureElementColumn(row, 5, cCTOrgStructureElement.getTeam());
    addCCTOrgStructureElementColumn(row, 6, cCTOrgStructureElement.getOrgId());
    addCCTOrgStructureElementColumn(row, 7, cCTOrgStructureElement.getSupervisorUserID());
    addCCTOrgStructureElementColumn(row, 8, cCTOrgStructureElement.getSupervisor());
    addCCTOrgStructureElementColumn(row, 9, getErrorMessage(cCTOrgStructureElement.getUserID(), cCTOrgStructureElement.getSupervisorUserID()));
  }

  private String getErrorMessage(String userID, String supervisorUserID) {
    String msg = "";
    if (userNotInDBList.contains(userID.toLowerCase())) {
      msg += textService.getByKeyWithDefaultText("admin_portletOrgStructureFailureUserNotInDB", "User Not available in CuCo DB :").getText() + userID + "\n";
    }
    if (supervisorUserID != null && userNotInDBList.contains(supervisorUserID.toLowerCase())) {
      if (msg.length() > 0) {
        msg += ", ";
      }
      msg += textService.getByKeyWithDefaultText("admin_portletOrgStructureFailureSupervisorNotInDB", "Supervisor Not available in CuCo DB :").getText() + supervisorUserID + "\n";
    }
    if (supervisorUserID != null && supervisorNotUserList.contains(supervisorUserID.toLowerCase())) {
      if (msg.length() > 0) {
        msg += ", ";
      }
      msg += textService.getByKeyWithDefaultText("admin_portletOrgStructureFailureSupervisorNotInUserList", "Supervisor Not available in User List :").getText() + supervisorUserID + "\n";
    }
    return msg;
  }

  private void addCCTOrgStructureElementColumn(Row row, int index, String value) {
    Cell cell = row.createCell(index);
    cell.setCellValue(value);
  }

  private void addCCTOrgStructureElementColumn(Row row, int index, int value) {
    Cell cell = row.createCell(index);
    cell.setCellValue(value);
  }

  private void createStyles(Workbook wb) {
    CellStyle style = wb.createCellStyle();
    Font headerFont = wb.createFont();
    headerFont.setBoldweight(Font.BOLDWEIGHT_BOLD);
    style.setAlignment(CellStyle.ALIGN_CENTER);
    style.setFillForegroundColor(IndexedColors.LIGHT_GREEN.getIndex());
    style.setFillPattern(CellStyle.SOLID_FOREGROUND);
    style.setFont(headerFont);
    styles.put(HEADER_STYLE, style);

    wb.getCreationHelper();
    style = wb.createCellStyle();
    style.setDataFormat(wb.getCreationHelper().createDataFormat().getFormat("dd.mm.yyyy"));
    styles.put(DATE_STYLE, style);
  }

  private void sizeColumns(Sheet sheet) {
    sheet.setColumnWidth(0, 16 * 256);
    sheet.setColumnWidth(1, 35 * 256);
    sheet.setColumnWidth(2, 35 * 256);
    sheet.setColumnWidth(3, 13 * 256);
    sheet.setColumnWidth(4, 13 * 256);
    sheet.setColumnWidth(5, 20 * 256);
    sheet.setColumnWidth(6, 15 * 256);
    sheet.setColumnWidth(7, 20 * 256);
    sheet.setColumnWidth(8, 35 * 256);
    sheet.setColumnWidth(9, 70 * 256);
  }

  @Autowired
  public void setTextService(TextService textService) {
    this.textService = textService;
  }

  public String getFileName() {
    return fileName;
  }

  public void setFileName(String fileName) {
    this.fileName = fileName;
  }

}
