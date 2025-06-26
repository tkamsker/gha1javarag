package at.a1ta.webclient.cucosett.client.service;

import java.util.List;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.cuco.core.shared.dto.ChargingType;

@RemoteServiceRelativePath("cuco/chargingType.rpc")
public interface ChargingTypeServlet extends RemoteService {
  public List<ChargingType> getAllChargingTypes();
}
