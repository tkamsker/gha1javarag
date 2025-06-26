package at.a1ta.webclient.cucosett.server;

import javax.servlet.annotation.WebServlet;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.ui.server.servlet.SpringRemoteServiceServlet;
import at.a1ta.cuco.core.service.ChargingTypeService;
import at.a1ta.cuco.core.shared.dto.ChargingType;
import at.a1ta.webclient.cucosett.client.service.ChargingTypeServlet;

@WebServlet(name = "chargingType", urlPatterns = {"/admin/cuco/chargingType.rpc"})
public class ChargingTypeServletImpl extends SpringRemoteServiceServlet implements ChargingTypeServlet {
  @Autowired
  private ChargingTypeService chargingTypeService;

  @Override
  public List<ChargingType> getAllChargingTypes() {
    return chargingTypeService.getAllChargingTypes();
  }
}
