package at.a1ta.cuco.core.service.impl;

import java.rmi.RemoteException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;
import org.springframework.util.StringUtils;

import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.Setting;
import at.a1ta.cuco.core.bean.PWUTokenResponse;
import at.a1ta.cuco.core.dao.esb.PartnerCenterLandingPageDao;
import at.a1ta.cuco.core.service.AccessTokenService;
import at.a1ta.cuco.core.shared.dto.AccessToken;
import at.a1ta.cuco.core.shared.dto.PartnerCenterAccessTokenRequest;

import com.telekomaustriagroup.esb.landingpagedealer.OrderServiceFault;

@Service
public class AccessTokenServiceImpl implements AccessTokenService {

  private static final Logger logger = LoggerFactory.getLogger(AccessTokenServiceImpl.class);

  private PartnerCenterLandingPageDao landingPageDao;
  private SettingService settingService;

  @Override
  public AccessToken getAccessTokenForPartnerCenter(PartnerCenterAccessTokenRequest request) {
    configureRequestWithDefaultsIfNotSet(request);
    try {
      return landingPageDao.getAccessToken(request);
    } catch (EsbException e) {
      logger.error("Unable to load access token for PartnerCenter", e);
    }
    return AccessToken.NONE;
  }

  private void configureRequestWithDefaultsIfNotSet(PartnerCenterAccessTokenRequest request) {
    appendSourceSystemConfigurationIfNotSet(request);
    appendProcessIdConfigurationIfNotSet(request);
  }

  private void appendProcessIdConfigurationIfNotSet(PartnerCenterAccessTokenRequest request) {
    if (!StringUtils.hasText(request.getProcessId())) {
      request.setProcessId(retrieveSettingValue("processId"));
    }
  }

  private void appendSourceSystemConfigurationIfNotSet(PartnerCenterAccessTokenRequest request) {
    if (!StringUtils.hasText(request.getSourceSystem())) {
      request.setSourceSystem(retrieveSettingValue("frontEndSystem"));
    }
  }

  private String retrieveSettingValue(String keyPart) {
    final String fullKey = LANDING_PAGE_DEALER_SETTING_PREFIX + "." + keyPart;
    Setting setting = settingService.getSetting(fullKey);
    Assert.notNull(setting, "Setting for '" + fullKey + "' must not be null.");

    return setting.getValue();
  }

  @Override
  public PWUTokenResponse validatePWUToken(String token) throws RemoteException, OrderServiceFault {
    return landingPageDao.validatePWUToken(token);
  }

  @Autowired
  public void setLandingPageDao(PartnerCenterLandingPageDao landingPageDao) {
    this.landingPageDao = landingPageDao;
  }

  @Autowired
  public void setConfigurationService(SettingService settingService) {
    this.settingService = settingService;
  }
}
