package at.a1ta.webclient.cucosett.server;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.DateFormat;
import java.text.NumberFormat;
import java.util.List;
import java.util.Locale;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.config.AutowireCapableBeanFactory;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.support.WebApplicationContextUtils;

import at.a1ta.bite.core.server.dao.AuthorityDao;
import at.a1ta.bite.core.server.dao.PersonDao;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.security.Authority;
import at.a1ta.cuco.core.service.ServiceService;
import at.a1ta.cuco.core.service.TeamService;
import at.a1ta.cuco.core.shared.dto.Auth;
import at.a1ta.cuco.core.shared.dto.Service;
import at.a1ta.cuco.core.shared.dto.Team;

@WebServlet(name = "pastExport", urlPatterns = {"/pastExport"})
public class PastExportServlet extends HttpServlet {

  @Autowired
  private ServiceService serviceService;

  @Autowired
  private PersonDao personDao;

  @Autowired
  private TeamService teamService;

  @Autowired
  private AuthorityDao authDao;

  @Override
  public void init() throws ServletException {
    super.init();
    WebApplicationContext ctx = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());
    AutowireCapableBeanFactory beanFactory = ctx.getAutowireCapableBeanFactory();
    beanFactory.autowireBean(this);
  }

  @Override
  public void service(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    response.setContentType("text/csv");
    PrintWriter writer = response.getWriter();

    DateFormat format = DateFormat.getDateInstance(DateFormat.MEDIUM);
    NumberFormat nformat = NumberFormat.getNumberInstance(Locale.GERMAN);

    if (request.getParameter("what").equals("services")) {
      writer.write("Dienstleistung;");
      writer.write("Gültig von;");
      writer.write("Gültig bis;");
      writer.write("Kosten;");
      writer.write("ProduktCode;");
      writer.write("Verrechnungsart;");
      writer.write("Gutschriftsart;");
      writer.write("Multiplikator;");
      writer.write("Produkt;");
      writer.write("Grund1;");
      writer.write("Grund2;");
      writer.write("Grund3;");
      writer.write("Resultat;\n");
      for (Service s : serviceService.getAllServices()) {
        writer.write(s.getName() + ";");
        writer.write(s.getValidity().getValidFrom() == null ? ";" : format.format(s.getValidity().getValidFrom()) + ";");
        writer.write(s.getValidity().getValidUntil() == null ? ";" : format.format(s.getValidity().getValidUntil()) + ";");
        writer.write(nformat.format(s.getCosts()) + ";");
        writer.write(s.getProductCode() + ";");
        writer.write(s.getChargingType().getName() + ";");
        writer.write(s.getCreditType().getName() + ";");
        writer.write(s.getMulti().toString() + ";");
        writer.write(s.getProduct() + ";");
        writer.write(s.getReason1() + ";");
        writer.write(s.getReason2() + ";");
        writer.write(s.getReason3() + ";");
        writer.write(s.getResult() + ";");
        writer.write("\n");
      }
      String disposition = "attachment; fileName=PastServices.csv";
      response.setHeader("Content-Disposition", disposition);
    } else if (request.getParameter("what").equals("agents")) {
      writer.write("Name;");
      writer.write("NTAccount;");
      writer.write("Team;");
      writer.write("Administrator;");
      writer.write("FBAdministrator;");
      writer.write("Abwesend;\n");
      for (BiteUser user : teamService.getAllUsers(Auth.PAST_GULA_CREATE)) {
        writer.write(user.getName() + ";");
        writer.write(user.getUsername() + ";");
        Team t = teamService.getTeamForUser(user.getId());
        writer.write(t == null ? ";" : (t.getName() + ";"));

        List<Authority> auths = authDao.getAuthoritiesForUser(user.getId());
        writer.write(containsAuthority(auths, Auth.PAST_TEAM_ASSIGN_SERVICE) ? "Ja;" : ";");
        writer.write(containsAuthority(auths, Auth.PAST_TEAM_ASSIGN_USER) ? "Ja;" : ";");
        writer.write(personDao.getPerson(user.getUsername()).isAbsent() ? "Ja;" : ";");
        writer.write("\n");
      }
      String disposition = "attachment; fileName=PastAgents.csv";
      response.setHeader("Content-Disposition", disposition);
    } else {
      response.setContentType("text");
      writer.write("Please call with: what=services or what=agents");
    }

    writer.close();
  }

  private boolean containsAuthority(List<Authority> auths, Auth authority) {
    for (Authority auth : auths) {
      if (auth.getName().equals(authority.getName())) {
        return true;
      }
    }
    return false;
  }

}
