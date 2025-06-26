package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.FileItemFactory;
import org.apache.commons.fileupload.FileUploadException;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.config.AutowireCapableBeanFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.support.WebApplicationContextUtils;

import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.AuthInfo;
import at.a1ta.bite.core.shared.AuthorityHelper;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.bite.ui.server.util.SessionAbstraction;
import at.a1ta.cuco.core.service.UserShopAssignmentService;
import at.a1ta.cuco.core.shared.dto.Auth;
import at.a1ta.cuco.core.shared.dto.UserShopAssignment;
import at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine;

@Component
public class UserShopAssignmentUploadServlet extends HttpServlet {

  @Autowired
  private UserShopAssignmentService userShopAssignmentService;
  @Autowired
  private SettingService settingService;
  private static final long MAX_FILE_SIZE = 12582912; // data length in bytes

  private static final String FILE_NO_CSV = "Es können nur CSV-Dateien hochgeladen werden!";
  private static final String FILE_EMPTY = "Die hochgeladene Datei ist leer!";
  private static final String FILE_TOO_LARGE = "Die hochgeladene Datei ist zu groß!";
  private static final String FILE_OK = "Datei ist OK!";
  private static final String FILE_ERROR = "Dateifehler!";
  private static final String PARSE_ERROR = "Einlesefehler!";
  private static final String RIGHTS_ERROR = "Berechtigungsfehler!";
  private static final String RIGHTS_MISSING = "Sie haben keine Berechtigung zum Upload einer Datei!";
  private static final String USER_UNKNOWN = "Der User ist im CuCo nicht bekannt!";
  private String comma = ";";

  @Override
  public void init() throws ServletException {
    super.init();

    WebApplicationContext ctx = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());
    AutowireCapableBeanFactory beanFactory = ctx.getAutowireCapableBeanFactory();
    beanFactory.autowireBean(this);
  }

  @Override
  protected void service(HttpServletRequest request, javax.servlet.http.HttpServletResponse response) throws ServletException, IOException {

    try {
      comma = settingService.getSetting("admin_importusershopdata_fileseperator").getValue();
      userShopAssignmentService.purgeLogEntries();
      if (!ensureAuthority(request, Auth.USERSHOPASSIGNMENTUPLOADDOWNLOAD)) {
        userShopAssignmentService.insertLogEntry(new UserShopAssignmentLogLine("ALL", RIGHTS_ERROR + " " + RIGHTS_MISSING));
        response.sendError(401, RIGHTS_ERROR + " " + RIGHTS_MISSING);
        return;
      }

    } catch (Exception ex) {
      response.sendError(401, RIGHTS_ERROR + " " + RIGHTS_MISSING + " Exception: " + ex.toString());
      return;
    }

    try {

      ArrayList<String> users = new ArrayList<String>(userShopAssignmentService.getUserNamesForAssignments());

      FileItem fileItem = readParameters(request);
      if (fileItem != null) {
        String checkResult = validateFile(fileItem);
        if (checkResult == FILE_OK) {
          try {
            userShopAssignmentService.purgeUserShopAssignments();
            InputStreamReader input = new InputStreamReader(fileItem.getInputStream());
            BufferedReader reader = new BufferedReader(input);
            String line = reader.readLine();

            while (line != null) {
              String[] tokens = line.split(comma);
              if (tokens.length == 2) {
                if (tokens[0].length() > 1 && tokens[1].length() > 1) {

                  if (users.contains(tokens[0].toUpperCase())) {
                    userShopAssignmentService.insertUserShopAssignment(new UserShopAssignment(tokens[0], tokens[1]));
                  } else {
                    userShopAssignmentService.insertLogEntry(new UserShopAssignmentLogLine(tokens[0], PARSE_ERROR + " " + USER_UNKNOWN));
                  }

                } else {
                  String username = "ALL";
                  String errorText = line;
                  errorText = (errorText.length() < 180) ? errorText : errorText.substring(0, 179);
                  userShopAssignmentService.insertLogEntry(new UserShopAssignmentLogLine(username, PARSE_ERROR + " " + " Folgende Zeile ist ungültig: " + errorText));
                }
              } else {
                String username = "ALL";
                String errorText = line;
                errorText = (errorText.length() < 180) ? errorText : errorText.substring(0, 179);

                if (tokens.length > 1 && tokens[0].length() > 1) {
                  username = tokens[0];
                }

                userShopAssignmentService.insertLogEntry(new UserShopAssignmentLogLine(username, PARSE_ERROR + " " + " Folgende Zeile ist ungültig: " + errorText));
              }

              line = reader.readLine();
            }
          } catch (Exception ex) {
            String errorText = ex.toString();
            errorText = (errorText.length() < 180) ? errorText : errorText.substring(0, 179);
            userShopAssignmentService.insertLogEntry(new UserShopAssignmentLogLine("ALL", PARSE_ERROR + " " + errorText));
          }

        } else {
          userShopAssignmentService.insertLogEntry(new UserShopAssignmentLogLine("ALL", FILE_ERROR + " " + checkResult));
        }

      } else {
        userShopAssignmentService.insertLogEntry(new UserShopAssignmentLogLine("ALL", FILE_ERROR + " " + FILE_EMPTY));
      }

    } catch (FileUploadException ex) {
      String errorText = ex.toString();
      errorText = (errorText.length() < 180) ? errorText : errorText.substring(0, 179);
      userShopAssignmentService.insertLogEntry(new UserShopAssignmentLogLine("ALL", FILE_ERROR + " " + errorText));
    }

  };

  private FileItem readParameters(HttpServletRequest request) throws FileUploadException {
    FileItemFactory factory = new DiskFileItemFactory();
    ServletFileUpload upload = new ServletFileUpload(factory);

    List<?> items = upload.parseRequest(request);
    Iterator<?> it = items.iterator();
    if (it.hasNext()) {
      FileItem item = (FileItem) it.next();
      return item;
    }
    return null;
  }

  protected String validateFile(FileItem fileItem) {
    if (!fileItem.getName().substring(fileItem.getName().lastIndexOf(".") + 1).equalsIgnoreCase("csv")) {
      return FILE_NO_CSV;
    } else if (fileItem.get().length == 0) {
      return FILE_EMPTY;
    } else if (fileItem.get().length > MAX_FILE_SIZE) {
      return FILE_TOO_LARGE;
    } else {
      return FILE_OK;
    }
  }

  private boolean ensureAuthority(HttpServletRequest request, AuthInfo authority) {
    HttpSession session = request.getSession();
    boolean isAuthenticated = isAuthenticated(session);

    UserInfo userInfo;
    if (isAuthenticated) {
      userInfo = (UserInfo) session.getAttribute(SessionAbstraction.USERINFO);
      return AuthorityHelper.hasAuthority(userInfo, authority);
    }
    return false;
  }

  private boolean isAuthenticated(HttpSession session) {
    Object attribute = session.getAttribute(SessionAbstraction.USERINFO);
    return attribute != null;
  }

}