package at.a1ta.cuco.core.service;

import java.rmi.RemoteException;

import at.a1ta.cuco.core.bean.PWUTokenResponse;
import at.a1ta.cuco.core.shared.dto.AccessToken;
import at.a1ta.cuco.core.shared.dto.PartnerCenterAccessTokenRequest;

import com.telekomaustriagroup.esb.landingpagedealer.OrderServiceFault;

public interface AccessTokenService {

  String LANDING_PAGE_DEALER_SETTING_PREFIX = "at.telekom.esb.LandingPageDealer.createTokenForOrderDataRequest";

  AccessToken getAccessTokenForPartnerCenter(PartnerCenterAccessTokenRequest request);

  PWUTokenResponse validatePWUToken(String token) throws RemoteException, OrderServiceFault;

}
