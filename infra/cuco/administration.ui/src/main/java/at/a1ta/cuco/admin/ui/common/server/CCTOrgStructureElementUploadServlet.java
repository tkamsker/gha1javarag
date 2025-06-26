package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.FileItemFactory;
import org.apache.commons.fileupload.FileUploadException;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;
import org.apache.commons.lang.StringUtils;
import org.apache.poi.ss.usermodel.Cell;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.WorkbookFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.config.AutowireCapableBeanFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.support.WebApplicationContextUtils;

import at.a1ta.bite.core.server.service.RoleService;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.server.service.TextService;
import at.a1ta.bite.core.shared.AuthorityHelper;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.ui.server.util.SessionAbstraction;
import at.a1ta.cuco.core.service.CCTOrgStructureElementService;
import at.a1ta.cuco.core.shared.dto.Auth;
import at.a1ta.cuco.core.shared.dto.product.CCTOrgStructureElement;

@Component
public class CCTOrgStructureElementUploadServlet extends HttpServlet {
  private static final long serialVersionUID = 1L;

  @Autowired
  private SettingService settingService;

  private static final String RIGHTS_ERROR = "Berechtigungsfehler!";
  private static final String RIGHTS_MISSING = "Sie haben keine Berechtigung zum Upload einer Datei!";
  private static final String CONTENT_DISPOSITION = "Content-Disposition";
  private static final String ATTACHMENT_FILENAME = "attachment; filename=";
  private static List<String> allUsersInDB = new ArrayList<String>();
  private List<String> supervisorNotUserList = new ArrayList<String>();
  private List<String> userNotInDBList = new ArrayList<String>();

  @Autowired
  public CCTOrgStructureElementService cCTOrgStructureElementService;
  private CCTOrgStructureErrorExport cCTOrgStructureErrorExport = new CCTOrgStructureErrorExport();
  private String uploadPath = System.getProperty("java.io.tmpdir");
  @Autowired
  private TextService textService;
  @Autowired
  private RoleService roleService;
  private String filename;
  private static final Logger logger = LoggerFactory.getLogger(CCTOrgStructureElementUploadServlet.class);

  @Override
  public void init() throws ServletException {
    super.init();

    WebApplicationContext ctx = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());
    AutowireCapableBeanFactory beanFactory = ctx.getAutowireCapableBeanFactory();
    beanFactory.autowireBean(this);
    uploadPath = getServletContext().getInitParameter("file-upload") != null ? getServletContext().getInitParameter("file-upload") : System.getProperty("java.io.tmpdir");
  }

  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    ServletOutputStream out = response.getOutputStream();
    response.setHeader("Content-Type", "text/html");
    try {
      if (!ensureAuthority(request)) {
        response.sendError(401, textService.getByKeyWithDefaultText("admin_portletOrgStructureMissingRights", RIGHTS_ERROR + RIGHTS_MISSING + "- Quote Clearance Administration").getText());
      } else {
        readParameters(request, response, out);
      }

    } catch (Exception ex) {
      String errorText = ex.toString();
      errorText = (errorText.length() < 180) ? errorText : errorText.substring(0, 179);
      logger.error(ex.getMessage(), ex);
      response.sendError(402, textService.getByKeyWithDefaultText("admin_portletOrgStructureUnknownErrorMessage", "Unknown Error While Processing Entries : " + ex.getMessage()).getText());
    } finally {
      out.flush();
      out.close();
    }
  }

  private List<String> headerArrayList() {
    String defaultHeadersList = "User ID,User Name,Rolle,Bereich,Stufe,Team,SAP ORG ID,Vorgesetzter User ID,Vorgesetzter Name";
    String[] headersList = settingService.getValueOrDefault("mariposa.admin.cctOrgStructureElementUploadFileHeaderList", defaultHeadersList).split(",");
    return new LinkedList<String>(Arrays.asList(headersList));
  }

  private FileItem readParameters(HttpServletRequest request, HttpServletResponse response, ServletOutputStream out) throws FileUploadException, IOException {
    FileItemFactory factory = new DiskFileItemFactory();
    ServletFileUpload upload = new ServletFileUpload(factory);

    List<?> items = upload.parseRequest(request);
    Iterator<?> it = items.iterator();
    if (it.hasNext()) {
      FileItem item = (FileItem) it.next();
      try {
        if (item.getName() != null || item.getName().endsWith(".xls") || item.getName().endsWith(".xlsx")) {
          String readFileStatus = readFile(item, response, out);
          logger.info("OrgStructure Import status: " + readFileStatus);
          out.println(readFileStatus);
        }
      } catch (Exception ex) {
        logger.error(ex.getMessage(), ex);
        response.sendError(404, textService.getByKeyWithDefaultText("admin_portletOrgStructureUnknownErrorMessage", "Unknown Error While Processing Entries : " + ex.getMessage()).getText());
      }

    }
    return null;
  }

  private String readFile(FileItem item, HttpServletResponse response, ServletOutputStream out) throws Exception {
    allUsersInDB.clear();
    supervisorNotUserList.clear();
    userNotInDBList.clear();
    List<String> headers = new ArrayList<String>();
    ArrayList<CCTOrgStructureElement> cctOrglist = new ArrayList<CCTOrgStructureElement>();
    ArrayList<String> userId = new ArrayList<String>();
    ArrayList<String> superviserId = new ArrayList<String>();
    filename = item.getName();
    File excelFile = new File(uploadPath + File.separator + getFileName());
    item.write(excelFile);

    org.apache.poi.ss.usermodel.Workbook wbook = WorkbookFactory.create(excelFile);

    if (wbook.getNumberOfSheets() == 1) {
      org.apache.poi.ss.usermodel.Sheet sheet = wbook.getSheetAt(0);
      Row row = sheet.getRow(0);
      for (Cell cell : row) {
        headers.add(cell.toString());
      }

      if (checkHeaders(headers)) {
        for (int i = 1; i <= sheet.getLastRowNum(); i++) {
          row = sheet.getRow(i);
          Cell cellUserIdAndSupId = row.getCell(0);
          if (!(userId.contains(cellUserIdAndSupId.toString().toLowerCase())) && (cellUserIdAndSupId.toString().trim().length() > 0)) {
            userId.add(cellUserIdAndSupId.toString().toLowerCase());

          }
          cellUserIdAndSupId = row.getCell(7);
          if (cellUserIdAndSupId != null && (cellUserIdAndSupId.toString().trim().length() > 0) && !(superviserId.contains(cellUserIdAndSupId.toString().toLowerCase()))) {
            superviserId.add(cellUserIdAndSupId.toString().toLowerCase());
          }
        }

        ArrayList<CCTOrgStructureElement> unmatchedsheets = new ArrayList<CCTOrgStructureElement>();
        ArrayList<String> unmatchedUsers = new ArrayList<String>();
        if (checkWhetherAllColumnsArePresent(headerArrayList(), headers)) {
          unmatchedUsers.addAll(checkUsers(userId, superviserId));
          if (unmatchedUsers.isEmpty()) {
            for (int i = 1; i <= sheet.getLastRowNum(); i++) {
              CCTOrgStructureElement cctOrg = new CCTOrgStructureElement();
              row = sheet.getRow(i);
              cctOrg.setUserID(row.getCell(0).toString().trim());
              cctOrg.setUser(row.getCell(1).toString().trim());
              if (row.getCell(2) != null && !row.getCell(2).getStringCellValue().trim().isEmpty()) {
                cctOrg.setRolle(row.getCell(2).toString().trim());
              } else {
                return textService.getByKeyWithDefaultText("admin_portletOrgStructureBlankRolleEntryFailureErrorMessage",
                    "Each entry in the 'Rolle' column is mandatory, an empty value was found in the Rolle column. Please add value and try again.").getText();
              }
              cctOrg.setRole(row.getCell(3).toString().trim());
              cctOrg.setApprovalLevel((int) (row.getCell(4).getNumericCellValue()));
              cctOrg.setTeam(row.getCell(5).toString().trim());
              row.getCell(6).setCellType(Cell.CELL_TYPE_STRING);
              cctOrg.setOrgId(row.getCell(6).getStringCellValue());
              cctOrg.setSupervisorUserID(row.getCell(7) != null ? row.getCell(7).toString().trim() : " ");
              cctOrg.setSupervisor(row.getCell(8) != null ? row.getCell(8).toString().trim() : " ");
              cctOrglist.add(cctOrg);
            }
            orgStructureSubmit(cctOrglist);
            return "Success: " + textService.getByKeyWithDefaultText("admin_portletOrgStructureSuccessMessage", "Die Organisationstruktur wurde erfolgreich übernommen").getText();
          } else {
            unmatchedsheets.addAll(sheetForDownload(unmatchedUsers, sheet));
            return streamErrorExcelFile(response, unmatchedsheets, out, response);
          }
        } else {
          String missingColumnErrorMessage = textService.getByKeyWithDefaultText("admin_portletOrgStructureFailureMissingHeader",
              "Error processing the organization structure file: required column is missing").getText();
          return missingColumnErrorMessage.replace("[0]", StringUtils.join(checkWhichColumnIsMissing(headers), ", "));
        }
      } else {
        return textService.getByKeyWithDefaultText("admin_portletOrgStructureFailureHeadersMismatch",
            "Error While Processing Entries : Header mismatch,Allowed Headers User ID,User Name,Rolle,Bereich,Stufe,Team,SAP ORG ID,Vorgesetzter User ID,Vorgesetzter Name").getText();
      }
    } else {
      return textService.getByKeyWithDefaultText("admin_portletOrgStructureFailureMultipleSheetsInXLS", "Error While Processing Entries : More than one sheet in XLS").getText();

    }
  }

  public ArrayList<CCTOrgStructureElement> sheetForDownload(ArrayList<String> unmatchedUsersIds, Sheet sheet) {
    ArrayList<CCTOrgStructureElement> sheetElements = new ArrayList<CCTOrgStructureElement>();
    Row row;
    for (int i = 1; i <= sheet.getLastRowNum(); i++) {
      CCTOrgStructureElement rowelements = new CCTOrgStructureElement();
      row = sheet.getRow(i);
      if (unmatchedUsersIds.contains(row.getCell(0).toString().toLowerCase()) || (row.getCell(7) != null && unmatchedUsersIds.contains(row.getCell(7).toString().toLowerCase()))) {
        rowelements.setUserID(row.getCell(0).toString());
        rowelements.setUser(row.getCell(1).getStringCellValue());
        rowelements.setRolle(row.getCell(2) != null ? row.getCell(2).toString().trim() : " ");
        rowelements.setRole(row.getCell(3).getStringCellValue());
        rowelements.setApprovalLevel((int) row.getCell(4).getNumericCellValue());
        rowelements.setTeam(row.getCell(5).getStringCellValue());
        row.getCell(6).setCellType(Cell.CELL_TYPE_STRING);
        rowelements.setOrgId(row.getCell(6).getStringCellValue());
        rowelements.setSupervisorUserID(row.getCell(7) != null ? row.getCell(7).toString() : " ");
        rowelements.setSupervisor(row.getCell(8) != null ? row.getCell(8).toString() : " ");
        sheetElements.add(rowelements);
      }
    }
    return sheetElements;
  }

  private void orgStructureSubmit(ArrayList<CCTOrgStructureElement> cctOrglist) {
    cCTOrgStructureElementService.updateCCTOrg(cctOrglist);

  }

  public String generateExcelFileName() {
    if (filename == null) {
      return null;
    }
    int slash = filename.lastIndexOf('\\');
    if (slash == -1) {
      slash = filename.lastIndexOf('/');
      return "errors_" + filename.substring(slash + 1);
    }
    return "errors_" + filename.substring(slash + 1);
  }

  public String getFileName() {
    if (filename == null) {
      return null;
    }
    int slash = filename.lastIndexOf('\\');
    if (slash == -1) {
      slash = filename.lastIndexOf('/');
      return filename.substring(slash + 1);
    }
    return filename.substring(slash + 1);
  }

  private String streamErrorExcelFile(final HttpServletResponse response, final ArrayList<CCTOrgStructureElement> unmatchedsheet, ServletOutputStream out, HttpServletResponse response2)
      throws IOException {
    try {
      response.setContentType(getFileName().endsWith(".xls") ? "application/vnd.ms-excel" : "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
      response.setHeader(CONTENT_DISPOSITION, ATTACHMENT_FILENAME + generateExcelFileName());
      cCTOrgStructureErrorExport.createExcelExport(out, unmatchedsheet, textService, supervisorNotUserList, userNotInDBList, getFileName());
    } catch (Exception e) {
      logger.error(e.getMessage(), e);
      return textService.getByKeyWithDefaultText("admin_portletOrgStructureErrorReportGenerationFailure", "There are failures while generating Error report. Please contact support.").getText();
    }
    return textService.getByKeyWithDefaultText("admin_portletOrgStructureFailureReportMessage", "Error While Processing Entries : Please refer downloaded Error report").getText();

  }

  private ArrayList<String> checkUsers(ArrayList<String> userList, ArrayList<String> superviserList) {
    ArrayList<String> rejectedUserList = new ArrayList<String>();
    for (String superviser : superviserList) {
      if (!userList.contains(superviser)) {
        supervisorNotUserList.add(superviser);
        rejectedUserList.add(superviser);
      }
    }
    allUsersInDB.addAll(cCTOrgStructureElementService.getAllUsers());
    for (String user : userList) {
      if (allUsersInDB.contains(user.trim())) {
        continue;
      } else {
        userNotInDBList.add(user.toLowerCase());
        rejectedUserList.add(user.toLowerCase());
      }
    }
    return rejectedUserList;
  }

  private boolean checkHeaders(List<String> headers) {
    for (String header : headers) {
      if (headerArrayList().contains(header)) {
        continue;
      } else {
        return false;
      }
    }
    return true;
  }

  private boolean checkWhetherAllColumnsArePresent(List<String> one, List<String> two) {
    if (one == null && two == null) {
      return true;
    }

    if (one == null || two == null) {
      return false;
    }
    if (one.size() != two.size()) {
      return false;
    }

    // to avoid messing the order of the lists we will use a copy
    one = new ArrayList<String>(one);
    two = new ArrayList<String>(two);

    Collections.sort(one);
    Collections.sort(two);
    return one.equals(two);
  }

  private List<String> checkWhichColumnIsMissing(List<String> headers) {
    List<String> tempList = new ArrayList<String>();
    tempList.addAll(headerArrayList());
    tempList.removeAll(headers);
    return tempList;
  }

  private boolean ensureAuthority(HttpServletRequest request) {
    HttpSession session = request.getSession();
    if (session.getAttribute(SessionAbstraction.USERINFO) != null) {
      return AuthorityHelper.hasAuthority((UserInfo) session.getAttribute(SessionAbstraction.USERINFO), Auth.QUOTE_CLEARANCE_ADMIN);
    }
    return false;
  }

}
