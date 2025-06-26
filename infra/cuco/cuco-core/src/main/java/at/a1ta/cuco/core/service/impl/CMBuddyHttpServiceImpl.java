package at.a1ta.cuco.core.service.impl;

import java.io.IOException;

import org.apache.commons.lang3.StringUtils;
import org.apache.http.Header;
import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.google.gson.Gson;

import at.a1ta.bite.core.server.service.LocalSettingService;
import at.a1ta.cuco.core.service.CMBuddyHttpService;
import at.a1ta.cuco.core.shared.dto.CMBuddyLogin;

@Service
public class CMBuddyHttpServiceImpl implements CMBuddyHttpService {

  private HttpClient httpClient;

  private LocalSettingService localSettingService;

  private static final Logger logger = LoggerFactory.getLogger(CMBuddyHttpServiceImpl.class);

  public CMBuddyHttpServiceImpl() {
    if (httpClient == null) {
      this.httpClient = new DefaultHttpClient();
    }
  }

  @Override
  public String getBuddyLink(Long partyId) {
    if (partyId == null) {
      return null;
    }
    String token = getToken();
    if (token == null) {
      return null;
    }

    if (checkParty(token, partyId)) {
      String toolUrl = this.localSettingService.getValue("cm_buddy.tool.url");
      return generateUrl(toolUrl, partyId);
    }
    return null;
  }

  private String getToken() {
    CMBuddyLogin login = getLoginData();
    Gson gson = new Gson();
    HttpEntity entity = new StringEntity(gson.toJson(login), ContentType.APPLICATION_JSON);

    String endpoint = this.localSettingService.getValue("cm_buddy.api.login.url");
    HttpPost postRequest = new HttpPost(endpoint);
    postRequest.setHeader("Accept", "application/json");
    postRequest.setEntity(entity);

    try {
      HttpResponse httpResponse = httpClient.execute(postRequest);
      Header[] headers = httpResponse.getAllHeaders();
      for (Header header : headers) {
        if ("Token".equalsIgnoreCase(header.getName())) {
          String token = header.getValue();
          postRequest.releaseConnection();
          return token;
        }
      }
      logger.warn("No token available from CM Buddy login");
    } catch (ClientProtocolException e) {
      logger.error("Error during CM Buddy login", e);
    } catch (IOException e) {
      logger.error("Error during CM Buddy login", e);
    }
    postRequest.releaseConnection();

    return null;
  }

  private CMBuddyLogin getLoginData() {
    CMBuddyLogin login = new CMBuddyLogin();
    String username = this.localSettingService.getValue("cm_buddy.api.login.username");
    login.setUsername(username);
    String password = this.localSettingService.getValue("cm_buddy.api.login.password");
    login.setPassword(password);
    return login;
  }

  private boolean checkParty(String token, Long partyId) {
    String endpoint = this.localSettingService.getValue("cm_buddy.api.check.url");
    HttpGet getRequest = new HttpGet(generateUrl(endpoint, partyId));
    getRequest.setHeader("Authorization", token);

    try {
      HttpResponse httpResponse = httpClient.execute(getRequest);
      if (httpResponse.getStatusLine().getStatusCode() == 200) {
        getRequest.releaseConnection();
        return true;
      }
      getRequest.releaseConnection();
      logger.info("Party not available in CM Buddy tool, got status " + httpResponse.getStatusLine().getStatusCode());
      return false;
    } catch (ClientProtocolException e) {
      logger.error("Error during CM Buddy check", e);
    } catch (IOException e) {
      logger.error("Error during CM Buddy check", e);
    }
    getRequest.releaseConnection();
    return false;
  }

  private String generateUrl(String endpoint, Long partyId) {
    return StringUtils.replace(endpoint, "{partyId}", partyId.toString());
  }

  @Autowired
  public void setLocalSettingService(LocalSettingService localSettingService) {
    this.localSettingService = localSettingService;
  }
}
