package at.a1ta.cuco.core.dao.esb;

import java.rmi.RemoteException;

import at.a1ta.cuco.core.bean.PWUTokenResponse;
import at.a1ta.cuco.core.shared.dto.AccessToken;
import at.a1ta.cuco.core.shared.dto.PartnerCenterAccessTokenRequest;

import com.telekomaustriagroup.esb.landingpagedealer.OrderServiceFault;

public interface PartnerCenterLandingPageDao {

  public AccessToken getAccessToken(PartnerCenterAccessTokenRequest tokenRequest);

  public PWUTokenResponse validatePWUToken(String token) throws RemoteException, OrderServiceFault;

}
