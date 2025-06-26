package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.annotation.WebServlet;
import java.math.BigDecimal;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Map;

import com.extjs.gxt.ui.client.data.BaseModelData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.core.server.service.UserTrackingService;
import at.a1ta.bite.ui.server.servlet.AuthenticationServlet;
import at.a1ta.cuco.admin.ui.common.client.service.SystemTrackingServlet;

@WebServlet(name = "systemTracking", urlPatterns = {"/admin/cuco/systemTracking.rpc"})
public class SystemTrackingServletImpl extends AuthenticationServlet implements SystemTrackingServlet {
  private static final Logger logger = LoggerFactory.getLogger(SystemTrackingServletImpl.class);

  @Autowired
  private UserTrackingService userTrackingService;

  @Override
  public ArrayList<BaseModelData> loadAnalysis4logon() {
    final Calendar calEnd = Calendar.getInstance();
    final Calendar calStart = Calendar.getInstance();
    final Date end;
    final Date start;

    calStart.add(Calendar.MONTH, -1);
    start = calStart.getTime();
    end = calEnd.getTime();
    return convertToModelData(userTrackingService.loadAnalysis4logon(start, end));
  }

  @Override
  public ArrayList<BaseModelData> loadAnalysis4customerRequest() {
    final Calendar calEnd = Calendar.getInstance();
    final Calendar calStart = Calendar.getInstance();
    final Date end;
    final Date start;

    calStart.add(Calendar.MONTH, -1);
    start = calStart.getTime();
    end = calEnd.getTime();
    return convertToModelData(userTrackingService.loadAnalysis4customerLoad(start, end));
  }

  @Override
  public ArrayList<BaseModelData> loadDetails4date(String dateString, String uuser) {
    try {
      Date date = new SimpleDateFormat("dd.MM.yyyy").parse(dateString);
      return convertToModelData(userTrackingService.loadDetails4date(date, uuser));
    } catch (ParseException e) {
      logger.error("Error during parsing date " + dateString + " for loading system trackig data for user " + uuser, e);
    }
    return null;
  }

  private ArrayList<BaseModelData> convertToModelData(List<Map<String, Object>> result) {

    ArrayList<BaseModelData> models = new ArrayList<BaseModelData>(result.size());
    for (Map<String, Object> map : result) {
      BaseModelData model = new BaseModelData();
      model.set("date", map.get("OCCURANCE_DATE"));
      if (map.get("OCCURANCES_DISTINCT") != null) {
        model.set("distinct", Long.valueOf(((BigDecimal) map.get("OCCURANCES_DISTINCT")).longValue()));
      }
      if (map.get("OCCURANCES_TOTAL") != null) {
        model.set("total", Long.valueOf(((BigDecimal) map.get("OCCURANCES_TOTAL")).longValue()));
      }

      model.set("uuser", map.get("UUSER"));
      model.set("name", map.get("USERNAME"));
      model.set("action", map.get("ACTION_TYPE"));
      model.set("operation", map.get("VAL_1"));
      models.add(model);
    }
    return models;
  }
}
