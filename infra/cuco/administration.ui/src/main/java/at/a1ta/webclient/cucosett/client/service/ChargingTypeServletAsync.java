package at.a1ta.webclient.cucosett.client.service;

import java.util.List;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.cuco.core.shared.dto.ChargingType;

public interface ChargingTypeServletAsync {
  public void getAllChargingTypes(AsyncCallback<List<ChargingType>> callback);
}
