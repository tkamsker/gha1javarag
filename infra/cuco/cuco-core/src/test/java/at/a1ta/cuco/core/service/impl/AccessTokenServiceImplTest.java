package at.a1ta.cuco.core.service.impl;

import java.util.UUID;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.Setting;
import at.a1ta.cuco.core.dao.esb.PartnerCenterLandingPageDao;
import at.a1ta.cuco.core.service.AccessTokenService;
import at.a1ta.cuco.core.shared.dto.AccessToken;
import at.a1ta.cuco.core.shared.dto.PartnerCenterAccessTokenRequest;

@RunWith(MockitoJUnitRunner.class)
public class AccessTokenServiceImplTest {

  private static final String DEFAULT_SOURCE_SYSTEM = "CuCo";
  private static final String DEFAULT_TARGET_SYSTEM = "Black";
  private static final String DEFAULT_PORCESS_ID = "Next";

  @Mock
  private PartnerCenterLandingPageDao daoMock;

  @Mock
  private SettingService settingsMock;

  private AccessTokenServiceImpl service;

  @Before
  public void setUp() {
    service = new AccessTokenServiceImpl();
    service.setLandingPageDao(daoMock);
    service.setConfigurationService(settingsMock);
  }

  @Test
  public void testGetAccessTokenForPartnerCenter() {
    Mockito.when(daoMock.getAccessToken(Matchers.any(PartnerCenterAccessTokenRequest.class))).thenReturn(createDefaultAccessToken());

    PartnerCenterAccessTokenRequest request = createPartnerCenterAccessTokenRequest("43 664 88603737", DEFAULT_SOURCE_SYSTEM,
        DEFAULT_PORCESS_ID);
    AccessToken token = service.getAccessTokenForPartnerCenter(request);

    Assert.assertNotNull(token);
    Mockito.verifyZeroInteractions(settingsMock);
    Mockito.verify(daoMock, Mockito.times(1)).getAccessToken(Matchers.any(PartnerCenterAccessTokenRequest.class));
  }

  @Test(expected = IllegalArgumentException.class)
  public void testGetAccessTokenForPartnerCenterWithoutSourceSystemSet() {
    PartnerCenterAccessTokenRequest request = createPartnerCenterAccessTokenRequest("43 664 88603737", "", DEFAULT_PORCESS_ID);
    service.getAccessTokenForPartnerCenter(request);
  }

  @Test
  public void testGetAccessTokenForPartnerCenterWithSourceSystemFallback() {
    String settingsKey = AccessTokenService.LANDING_PAGE_DEALER_SETTING_PREFIX + ".frontEndSystem";

    Mockito.when(daoMock.getAccessToken(Matchers.any(PartnerCenterAccessTokenRequest.class))).thenReturn(createDefaultAccessToken());
    Mockito.when(settingsMock.getSetting(settingsKey)).thenReturn(createSetting("key", DEFAULT_SOURCE_SYSTEM));

    PartnerCenterAccessTokenRequest request = createPartnerCenterAccessTokenRequest("43 664 88603737", "", DEFAULT_PORCESS_ID);
    AccessToken token = service.getAccessTokenForPartnerCenter(request);

    Assert.assertNotNull(token);
    Mockito.verify(settingsMock, Mockito.times(1)).getSetting(Matchers.eq(settingsKey));
    Mockito.verify(daoMock, Mockito.times(1)).getAccessToken(Matchers.any(PartnerCenterAccessTokenRequest.class));
  }

  @Test(expected = IllegalArgumentException.class)
  public void testGetAccessTokenForPartnerCenterWithoutProcessIdSet() {
    PartnerCenterAccessTokenRequest request = createPartnerCenterAccessTokenRequest("43 664 88603737", DEFAULT_SOURCE_SYSTEM, "");
    service.getAccessTokenForPartnerCenter(request);
  }

  @Test
  public void testGetAccessTokenForPartnerCenterWithProcessIdFallback() {
    String settingsKey = AccessTokenService.LANDING_PAGE_DEALER_SETTING_PREFIX + ".processId";

    Mockito.when(daoMock.getAccessToken(Matchers.any(PartnerCenterAccessTokenRequest.class))).thenReturn(createDefaultAccessToken());
    Mockito.when(settingsMock.getSetting(settingsKey)).thenReturn(createSetting("key", DEFAULT_SOURCE_SYSTEM));

    PartnerCenterAccessTokenRequest request = createPartnerCenterAccessTokenRequest("43 664 88603737", DEFAULT_SOURCE_SYSTEM, "");
    AccessToken token = service.getAccessTokenForPartnerCenter(request);

    Assert.assertNotNull(token);
    Mockito.verify(settingsMock, Mockito.times(1)).getSetting(Matchers.eq(settingsKey));
    Mockito.verify(daoMock, Mockito.times(1)).getAccessToken(Matchers.any(PartnerCenterAccessTokenRequest.class));
  }

  @Test
  public void testGetAccessTokenForPartnerCenterWhenESBThrowsException() {
    Mockito.when(daoMock.getAccessToken(Matchers.any(PartnerCenterAccessTokenRequest.class))).thenThrow(
        new EsbException("exception message"));
    PartnerCenterAccessTokenRequest request = createPartnerCenterAccessTokenRequest("43 664 88603737", DEFAULT_SOURCE_SYSTEM,
        DEFAULT_PORCESS_ID);
    AccessToken token = service.getAccessTokenForPartnerCenter(request);

    Assert.assertEquals(AccessToken.NONE, token);
  }

  private PartnerCenterAccessTokenRequest createPartnerCenterAccessTokenRequest(String phone, String sourceSystem, String processId) {
    PartnerCenterAccessTokenRequest request = new PartnerCenterAccessTokenRequest();

    request.setSourceSystem(sourceSystem);
    String[] msisdnParts = phone.split(" ");
    request.setCountryCode(msisdnParts[0]);
    request.setNationalDestinationCode(msisdnParts[1]);
    request.setSubscriberNumber(msisdnParts[2]);
    request.setProcessId(processId);

    return request;
  }

  private Setting createSetting(String key, String value) {
    Setting setting = new Setting();
    setting.setKey(key);
    setting.setValue(value);
    return setting;
  }

  private AccessToken createDefaultAccessToken() {
    return new AccessToken(DEFAULT_TARGET_SYSTEM, UUID.randomUUID().toString());
  }
}
