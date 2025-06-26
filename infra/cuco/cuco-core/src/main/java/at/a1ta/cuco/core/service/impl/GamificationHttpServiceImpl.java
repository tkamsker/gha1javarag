package at.a1ta.cuco.core.service.impl;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.impl.conn.PoolingClientConnectionManager;
import org.apache.http.impl.conn.SchemeRegistryFactory;
import org.apache.http.util.EntityUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.data.cusco.http.CusCoMessageFormatter;
import at.a1ta.cuco.core.service.GamificationHttpService;
import at.a1ta.cuco.core.service.GamificationLocalService;
import at.a1ta.cuco.core.shared.dto.GamificationMessage;
import at.a1ta.cuco.core.shared.dto.GamificationRequest;
import at.a1ta.cuco.core.shared.dto.GamificationResponse;

import com.google.gson.Gson;

@Service
public class GamificationHttpServiceImpl implements GamificationHttpService {

  private static final int DEFAULT_MAX_CONNECTIONS = 5;
  private static final int DEFAULT_MAX_CONNECTIONS_PER_ROUTE = 5;
  private HttpClient httpClient;
  @Autowired
  private GamificationLocalService gamificationLocalService;

  @Autowired
  private SettingService settingService;

  private static final Logger logger = LoggerFactory.getLogger(GamificationHttpServiceImpl.class);

  private final SimpleDateFormat SIMPLE_DATE_FORMAT = new SimpleDateFormat("EEE MMM dd yyyy HH:mm:ss 'GMT'Z (z)", Locale.US);

  public GamificationHttpServiceImpl() {
    this(DEFAULT_MAX_CONNECTIONS, DEFAULT_MAX_CONNECTIONS_PER_ROUTE, null);
  }

  public GamificationHttpServiceImpl(int maxTotalConnections, int maxConnectionPerRoute) {
    this(maxTotalConnections, maxConnectionPerRoute, null);
  }

  public GamificationHttpServiceImpl(int maxTotalConnections, int maxConnectionPerRoute, CusCoMessageFormatter formatter) {
    PoolingClientConnectionManager conMan = new PoolingClientConnectionManager(SchemeRegistryFactory.createDefault());
    conMan.setMaxTotal(maxTotalConnections);
    conMan.setDefaultMaxPerRoute(maxConnectionPerRoute);
    this.httpClient = new DefaultHttpClient(conMan);
  }

  public GamificationHttpServiceImpl(HttpClient httpClient) {
    if (httpClient == null) {
      PoolingClientConnectionManager conMan = new PoolingClientConnectionManager(SchemeRegistryFactory.createDefault());
      conMan.setMaxTotal(DEFAULT_MAX_CONNECTIONS);
      conMan.setDefaultMaxPerRoute(DEFAULT_MAX_CONNECTIONS_PER_ROUTE);
      this.httpClient = new DefaultHttpClient(conMan);
    } else {
      this.httpClient = httpClient;
    }
  }

  @Override
  public GamificationResponse getAvailableGamificationMessages(final GamificationRequest message, final String endpoint) {
    HttpPost postRequest = new HttpPost(endpoint);
    HttpResponse httpResponse = null;
    GamificationResponse response = new GamificationResponse();
    if (!settingService.getBooleanValue("gamification.gamificationEnabled", false)) {
      return response;
    }
    try {
      postRequest.addHeader("content-type", "application/json");
      HttpEntity entity = new StringEntity(message.getQueryString(), ContentType.APPLICATION_JSON);
      postRequest.setEntity(entity);
      httpResponse = httpClient.execute(postRequest);
      response.setStatus(Integer.toString(httpResponse.getStatusLine().getStatusCode()));
      String responseData = EntityUtils.toString(httpResponse.getEntity(), "UTF-8");
      logger.debug(responseData);
      GamificationResponse parsedResponse = new Gson().fromJson(responseData, GamificationResponse.class);
      if (settingService.getBooleanValue("gamification.gamificationLocalHistoryEnabled", true) && parsedResponse != null && parsedResponse.getMessages().size() > 0) {
        Map<String, GamificationMessage> alreadyStoredMessages = gamificationLocalService.getAlreadyStoredMessages((ArrayList<GamificationMessage>) parsedResponse.getMessages(), message.getAgentId());
        List<GamificationMessage> newMessages = new ArrayList<GamificationMessage>();
        List<GamificationMessage> alreadyStoredUnreadMessages = new ArrayList<GamificationMessage>();
        for (GamificationMessage msg : parsedResponse.getMessages()) {
          if (msg.getTimestamp() != null) {
            try {
              msg.setTimestampDateFormat(SIMPLE_DATE_FORMAT.parse(msg.getTimestamp()));
            } catch (Exception ex) {
              // do nothing.
            }
          }
          msg.setReadByAgent(false);
          if (alreadyStoredMessages.containsKey(msg.getMessageUid())) {
            msg.setReadByAgent(alreadyStoredMessages.get(msg.getMessageUid()).isReadByAgent());
            if (!msg.isReadByAgent()) {
              alreadyStoredUnreadMessages.add(msg);
            }
          } else {
            newMessages.add(msg);
          }
        }
        parsedResponse.setUnreadMsgCount(newMessages.size() + alreadyStoredUnreadMessages.size());
        gamificationLocalService.addAllMessagesToCuCoDB((ArrayList<GamificationMessage>) newMessages, message.getAgentId());
      }
      return parsedResponse == null ? response : parsedResponse;
    } catch (Exception e) {
      logger.error("Error while retrieving Gamification Info For User " + message.getAgentId() + " :" + e.getMessage(), e.getCause());
      throw new RuntimeException(e.getMessage(), e);
    } finally {
      if (httpResponse != null && httpResponse.getEntity() != null) {
        try {
          EntityUtils.consume(httpResponse.getEntity());
        } catch (IOException e) {
          logger.error("Error while consuming HTTP Response for User " + message.getAgentId() + " :" + e.getMessage(), e.getCause());
        }
      }
      postRequest.releaseConnection();
    }
  }

}
