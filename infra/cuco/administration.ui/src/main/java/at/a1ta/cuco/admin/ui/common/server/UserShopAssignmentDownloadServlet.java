package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.ArrayList;

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
import at.a1ta.cuco.core.shared.dto.UserShopAssignmentLogLine;

@Component
public class UserShopAssignmentDownloadServlet extends HttpServlet {

  @Autowired
  private UserShopAssignmentService userShopAssignmentService;
  @Autowired
  private SettingService settingService;
  private String comma = ";";

  @Override
  public void init() throws ServletException {
    super.init();

    WebApplicationContext ctx = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());
    AutowireCapableBeanFactory beanFactory = ctx.getAutowireCapableBeanFactory();
    beanFactory.autowireBean(this);
  }

  @Override
  public void service(ServletRequest request, ServletResponse response) throws ServletException, IOException {
    if (!ensureAuthority((HttpServletRequest) request, Auth.USERSHOPASSIGNMENTUPLOADDOWNLOAD)) {
      ((HttpServletResponse) response).sendError(401, "Sind haben keine Berechtigung zum Download der Datei!");
      return;
    }

    try {
      comma = settingService.getSetting("admin_importusershopdata_fileseperator").getValue();
      ArrayList<UserShopAssignmentLogLine> logdata = new ArrayList<UserShopAssignmentLogLine>(userShopAssignmentService.getLogEntries());

      for (UserShopAssignmentLogLine line : logdata) {
        StringBuilder str = new StringBuilder();

        if (line != null && line.getUsername() != null && line.getLogText() != null) {
          str.append(line.getUsername()).append(comma).append(line.getLogText()).append("\n");
        } else if (line != null && line.getUsername() != null && line.getLogText() == null) {
          str.append(line.getUsername()).append(comma).append("\n");
        } else if (line != null && line.getUsername() == null && line.getLogText() != null) {
          str.append(comma).append(line.getLogText()).append("\n");
        } else {
          str.append("" + comma + "\n");
        }

        response.getWriter().append(str.toString());
      }

      ((HttpServletResponse) response).setHeader("Content-Disposition", "attachment; filename=logdata.csv");
      response.setContentType("text/csv");
      response.getOutputStream().flush();
      response.getOutputStream().close();

    } catch (Exception ex) {
      return;
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

  @Autowired
  public void setSettingService(SettingService service) {
    this.settingService = service;
  }
}
