package at.a1ta.cuco.core.service;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.security.KeyStore;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.List;
import java.util.Queue;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutorService;

import javax.annotation.PreDestroy;
import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManagerFactory;

import org.java_websocket.WebSocket;
import org.java_websocket.handshake.ClientHandshake;
import org.java_websocket.server.DefaultSSLWebSocketServerFactory;
import org.java_websocket.server.WebSocketServer;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import at.a1ta.bite.core.server.service.LocalSettingService;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.shared.dto.CuCoGamificationLoginMessage;
import at.a1ta.cuco.core.shared.dto.GamificationCuCoMessages;
import at.a1ta.cuco.core.shared.dto.GamificationData;
import at.a1ta.cuco.core.shared.dto.GamificationMessage;
import at.a1ta.cuco.core.shared.dto.GamificationMessageComparator;
import at.a1ta.cuco.core.shared.dto.GamificationRequest;
import at.a1ta.cuco.core.shared.dto.GamificationResponse;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;

class GamificationWebsocketThread extends Thread {

  public GamificationWebsocketThread(Queue<CucoWebSocketWrapper> currentQueue, String threadSeqNumber, SettingService settingService, GamificationHttpService gamificationService) {
    super();
    this.currentQueue = currentQueue;
    this.threadSequenceNumber = threadSeqNumber;
    this.settingService = settingService;
    this.gamificationHttpService = gamificationService;
    setDaemon(true);
  }

  private static org.slf4j.Logger logger = LoggerFactory.getLogger("GAMIFICATION");
  private static org.slf4j.Logger genericLogger = LoggerFactory.getLogger(GamificationWebsocketThread.class.getName());
  private Queue<CucoWebSocketWrapper> currentQueue;
  private String threadSequenceNumber;
  private static ConcurrentHashMap<String, String> keyQidMap = new ConcurrentHashMap<String, String>();
  private static ConcurrentHashMap<String, Long> keyLastQueryTimeMap = new ConcurrentHashMap<String, Long>();
  private SettingService settingService;
  private GamificationHttpService gamificationHttpService;
  private static final String DEFAULT_QUERY = "{\"query\":\"query root($agentId:ID! $limit:Int!) "
      + "{ cucoMessages(agentId:$agentId, limit:$limit) { agentId messages { messageUid timestamp title message type url }}}\",\""
      + "variables\":{\"agentId\":\"#agentId#\", \"limit\":#limit#},\"operationName\":\"root\"}";
  private volatile boolean stop = false;

  private String trimResourceDesString(String input) {
    return input != null ? input.replaceAll("/", "") : null;
  }

  private GamificationResponse getGamificationMessages(String userName) {
    if (settingService != null && !settingService.getBooleanValue("gamification.gamificationEnabled", false)) {
      return null;
    }
    GamificationRequest request = new GamificationRequest();
    request.setAgentId(userName);
    request.setLimit(settingService != null ? settingService.getIntValue("gamification.Messagelimit", 30) : 30);
    request.setContentType("application/json");
    String queryString = settingService != null ? settingService.getValueOrDefault("gamification.queryString", DEFAULT_QUERY) : DEFAULT_QUERY;
    queryString = queryString.replace("#agentId#", request.getAgentId()).replace("#limit#", request.getLimit() + "");
    request.setQueryString(queryString);
    request.setApiKey(settingService != null ? settingService.getValueOrDefault("gamification.queryAPIKey", "") : "");
    GamificationResponse availableGamificationMessages = gamificationHttpService.getAvailableGamificationMessages(request,
        settingService != null ? settingService.getValueOrDefault("gamification.targetURL", "http://vlbotai002.at.inside:8085/graphql") : "http://vlbotai002.at.inside:8085/graphql");
    if (availableGamificationMessages != null && availableGamificationMessages.getMessages() != null && availableGamificationMessages.getMessages().size() > 0) {
      Collections.sort(availableGamificationMessages.getMessages(), new GamificationMessageComparator());
      for (GamificationMessage msg : availableGamificationMessages.getMessages()) {
        msg.setTimestampDateFormat(null);
      }
      availableGamificationMessages.getData().getCucoMessages().setMessages(availableGamificationMessages.getMessages());
    }

    return availableGamificationMessages;
  }

  public void stopNow() {
    this.stop = true;
    interrupt();
  }

  public int getNoOfActiveSessions() {
    return getCurrentQueue() != null ? getCurrentQueue().size() : 0;
  }

  @Override
  public void run() {
    while (!stop) {
      try {
        if (settingService != null && !settingService.getBooleanValue("gamification.gamificationEnabled", false)) {
          // do not stop thread,will be needed if toggle is turned on again
          logger.debug("GamificationInactive");
          continue;
        }
        long starttime = Calendar.getInstance().getTimeInMillis();
        if (getCurrentQueue() != null && getCurrentQueue().size() > 0) {
          logger.debug("checking session on queue " + currentQueue);
          int delayBetweenTwoRequests = Integer.parseInt(settingService.getValueOrDefault("gamification.gamificationInquiryDelayInSeconds", "30")) * 1000;
          ArrayList<CucoWebSocketWrapper> closedSessions = new ArrayList<CucoWebSocketWrapper>();
          for (CucoWebSocketWrapper session : getCurrentQueue()) {
            if (settingService != null && !settingService.getBooleanValue("gamification.gamificationEnabled", false)) {
              if (settingService == null) {
                logger.info("Gamification is disabled : settingService is null " + settingService);
              } else {
                logger.info("Gamification is disabled - check gamification.gamificationEnabled: " + settingService.getBooleanValue("gamification.gamificationEnabled", false));
              }
              break;
            }
            if (session.getSocket().isClosed() || session.getSocket().isClosing()) {
              closedSessions.add(session);
            } else {
              String sessionkey = trimResourceDesString(session.getSocket().getResourceDescriptor());
              if (sessionkey != null
                  && (!keyLastQueryTimeMap.keySet().contains(sessionkey) || (keyLastQueryTimeMap.keySet().contains(sessionkey) && (Calendar.getInstance().getTimeInMillis() - keyLastQueryTimeMap
                      .get(sessionkey)) >= delayBetweenTwoRequests))) {
                try {

                  GamificationResponse res = getGamificationMessages(session.getQid());
                  if (session.getSocket().isOpen() && res != null) {
                    session.getSocket().send(new Gson().toJson(res, GamificationResponse.class));
                    keyLastQueryTimeMap.put(sessionkey, Calendar.getInstance().getTimeInMillis());
                  }
                } catch (Exception ex) {
                  logger.error("Error while calling Gamification webservice for User session " + session != null ? keyQidMap.get(sessionkey) : "-" + " :" + ex.getMessage(), ex.getCause());
                  if (session != null) {
                    try {
                      keyLastQueryTimeMap.put(sessionkey, Calendar.getInstance().getTimeInMillis());
                      session.getSocket().send(new Gson().toJson(getGamificationResponseWithStatus("Error :" + ex.getMessage(), session != null ? session.getQid() : "")));
                    } catch (Exception e) {
                      logger.error("Error while sending error status to User session " + keyQidMap.get(sessionkey) + " :" + e.getMessage(), e.getCause());
                    }
                  }

                }

              }
            }
          }

          for (CucoWebSocketWrapper session : closedSessions) {
            releaseSession(session);
          }
          String msg = "Finished checking all sessions (" + getCurrentQueue().size() + ") of Thread Seq Number: " + getThreadSequenceNumber() + " in "
              + (Calendar.getInstance().getTimeInMillis() - starttime) / 1000 + " Seconds";
          logger.debug(msg);
        }
        sleep(5000);
      } catch (Exception e) {
        logger.error("Error in websocket threads " + " :" + e.getMessage(), e.getCause());
      }
    }

  }

  private void releaseSession(CucoWebSocketWrapper session) {
    String sessionKey = trimResourceDesString(session.getSocket().getResourceDescriptor());
    try {
      logger.info("Trying to close User Session " + " :" + sessionKey);
      keyQidMap.remove(sessionKey);
      getCurrentQueue().remove(session);
    } catch (Exception ex) {
      logger.error("Error while closing session " + " :" + sessionKey, ex);
    }
  }

  public Queue<CucoWebSocketWrapper> getCurrentQueue() {
    return currentQueue;
  }

  public void setCurrentQueue(Queue<CucoWebSocketWrapper> currentQueue) {
    this.currentQueue = currentQueue;
  }

  public String getThreadSequenceNumber() {
    return threadSequenceNumber;
  }

  public void setThreadSequenceNumber(String threadSequenceNumber) {
    this.threadSequenceNumber = threadSequenceNumber;
  }

  private GamificationResponse getGamificationResponseWithStatus(String status, String agentId) {
    GamificationResponse res = new GamificationResponse();
    res.setStatus(status);
    res.setUnreadMsgCount(0);
    res.setData(new GamificationData());
    res.getData().setCucoMessages(new GamificationCuCoMessages());
    res.getData().getCucoMessages().setAgentId(agentId);
    res.getData().getCucoMessages().setMessages(new ArrayList<GamificationMessage>());
    return res;
  }
}

@Component
public class CuCoGamificationPlainWebsocketEndPoint extends WebSocketServer {
  private static org.slf4j.Logger logger = LoggerFactory.getLogger("GAMIFICATION");
  private static org.slf4j.Logger genericLogger = LoggerFactory.getLogger(CuCoGamificationPlainWebsocketEndPoint.class.getName());
  private static Queue<CucoWebSocketWrapper> queue = new ConcurrentLinkedQueue<CucoWebSocketWrapper>();

  // will hold the threadPool queues, each queue will maintain equal number of sessions
  private static List<Queue<CucoWebSocketWrapper>> listOfSessionQueues = Collections.synchronizedList(new ArrayList<Queue<CucoWebSocketWrapper>>());
  // will hold all the threads to close them properly on the server shutdown
  private static List<GamificationWebsocketThread> gamificationThreads = Collections.synchronizedList(new ArrayList<GamificationWebsocketThread>());
  private static ConcurrentHashMap<String, String> keyQidMap = new ConcurrentHashMap<String, String>();
  @Autowired
  private SettingService settingService;
  @Autowired
  private GamificationHttpService gamificationHttpService;
  private LocalSettingService localSettingService;
  @Autowired
  private GamificationLocalService gamificationLocalService;
  private ExecutorService executorService;
  private int portNumber;

  @Autowired
  public void setSettingService(SettingService settingService) {
    this.settingService = settingService;
  }

  @Autowired
  public CuCoGamificationPlainWebsocketEndPoint(LocalSettingService localSettingService) {

    super(new InetSocketAddress(Integer.parseInt(localSettingService.getValue("websocket.portNo") == null ? "7480" : localSettingService.getValue("websocket.portNo"))));
    setLocalSettingService(localSettingService);
    setPortNumber(Integer.parseInt(getLocalSettingService().getValue("websocket.portNo") == null ? "7480" : getLocalSettingService().getValue("websocket.portNo")));
    logger.info("Starting Gamification Threads on port " + getPortNumber());
    genericLogger.info("Starting Gamification Threads on port " + getPortNumber());
    if (Boolean.valueOf(getLocalSettingService().getValue("websocket.enabledOnCurrentServer"))) {
      FileInputStream fis = null;
      try {

        if (Boolean.valueOf(getLocalSettingService().getValue("websocket.enableSSL"))) {
          KeyStore ks = KeyStore.getInstance(getLocalSettingService().getValue("websocket.keyStoreType"));
          File kf = new File(getLocalSettingService().getValue("websocket.keyStoreLocation"));
          fis = new FileInputStream(kf);
          ks.load(fis, getLocalSettingService().getValue("websocket.keyStoreKey").toCharArray());

          KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
          kmf.init(ks, getLocalSettingService().getValue("websocket.keyStoreKey").toCharArray());
          TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
          tmf.init(ks);

          SSLContext sslContext = null;
          sslContext = SSLContext.getInstance("TLS");
          sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

          setWebSocketFactory(new DefaultSSLWebSocketServerFactory(sslContext));

        }
        start();
      } catch (Exception e) {
        logger.error("Error while Starting Gamification Threads on port " + getPortNumber() + " :" + e.getMessage(), e.getCause(), e);
      } finally {
        if (fis != null) {
          try {
            fis.close();
          } catch (IOException e) {
            // do nothing
          }
        }
      }
    } else {
      String msg = "Gamification websocket will not be started, value of websocket.enabledOnCurrentServer is - "
          + Boolean.valueOf(getLocalSettingService().getValue("websocket.enabledOnCurrentServer"));
      logger.error(msg);
      genericLogger.error(msg);
    }
  }

  private void startThreads() {
    int threadPoolSize = getLocalSettingService().getValue("websocket.poolSize") != null ? Integer.parseInt(getLocalSettingService().getValue("websocket.poolSize")) : 30;
    logger.debug("Starting Gamification Threads with " + threadPoolSize + " Queues");
    executorService = java.util.concurrent.Executors.newFixedThreadPool(threadPoolSize);

    listOfSessionQueues.clear();
    gamificationThreads.clear();
    while (listOfSessionQueues.size() < threadPoolSize) {
      listOfSessionQueues.add(new ConcurrentLinkedQueue<CucoWebSocketWrapper>());
    }

    int index = 0;
    for (Queue<CucoWebSocketWrapper> queue : listOfSessionQueues) {
      GamificationWebsocketThread task = new GamificationWebsocketThread(queue, index + "", settingService, getGamificationHttpService());
      gamificationThreads.add(task);
      executorService.submit(task);
      index += 1;
    }
  }

  private int getQueueIndexWithMinimumSessions() {
    if (gamificationThreads.size() == 0) {
      return -1;
    }
    int index = 0;
    int minSize = gamificationThreads.get(0).getNoOfActiveSessions();
    for (int i = 0; i < gamificationThreads.size(); i++) {
      if (gamificationThreads.get(i).getNoOfActiveSessions() == 0) {
        index = i;
        minSize = gamificationThreads.get(i).getNoOfActiveSessions();
        break;
      }
      if (gamificationThreads.get(i).getNoOfActiveSessions() < minSize) {
        index = i;
        minSize = gamificationThreads.get(i).getNoOfActiveSessions();
      }
    }

    return index;

  }

  public void onClientMessage(WebSocket session, String messageJson) {
    if (settingService != null && !settingService.getBooleanValue("gamification.gamificationEnabled", false)) {
      session.close();
      // Gamification Disabled Do nothing.
      return;
    }
    logger.debug("received message from  User :" + messageJson);
    ObjectMapper mapper = new ObjectMapper();
    CuCoGamificationLoginMessage userMessage = null;
    String sessionKey = trimResourceDesString(session.getResourceDescriptor());
    try {
      userMessage = mapper.readValue(messageJson, CuCoGamificationLoginMessage.class);
      userMessage.setSessionKey(sessionKey);
      if (keyQidMap.containsKey(userMessage.getSessionKey())) {

        keyQidMap.put(userMessage.getSessionKey(), userMessage.getId());
        int queueIndexWithMinimumSessions = getQueueIndexWithMinimumSessions();
        if (queueIndexWithMinimumSessions < 0) {
          queue = new ConcurrentLinkedQueue<CucoWebSocketWrapper>();
          queue.add(new CucoWebSocketWrapper(session, userMessage.getId(), userMessage.getSessionKey()));
          listOfSessionQueues.add(queue);
        } else {
          if (gamificationThreads.get(queueIndexWithMinimumSessions).getNoOfActiveSessions() < (localSettingService.getValue("websocket.maxSessionsPerPool") != null ? Integer
              .parseInt(localSettingService.getValue("websocket.maxSessionsPerPool")) : 200)) {
            gamificationThreads.get(queueIndexWithMinimumSessions).getCurrentQueue().add(new CucoWebSocketWrapper(session, userMessage.getId(), userMessage.getSessionKey()));
          } else {
            logger.error("Session rejected due to very high number of active users." + sessionKey);
            session.close();
            return;
          }
        }
        GamificationResponse res = getGamificationResponseWithStatus("Success", userMessage.getId());
        session.send(new Gson().toJson(res, GamificationResponse.class));
        logger.info("Listener Started for User :" + userMessage.getId());
      } else {
        logger.error("Session closed due to invalid message sent by user " + sessionKey);
        session.close();
      }
    } catch (Exception ex) {
      session.close();
      logger.error("Error while initiating listner for user " + sessionKey + " :" + ex.getMessage(), ex.getCause());
    }

  }

  private String trimResourceDesString(String input) {
    return input != null ? input.replaceAll("/", "") : null;
  }

  private GamificationResponse getGamificationResponseWithStatus(String status, String agentId) {
    GamificationResponse res = new GamificationResponse();
    res.setStatus(status);
    res.setUnreadMsgCount(0);
    res.setData(new GamificationData());
    res.getData().setCucoMessages(new GamificationCuCoMessages());
    res.getData().getCucoMessages().setAgentId(agentId);
    res.getData().getCucoMessages().setMessages(new ArrayList<GamificationMessage>());
    return res;
  }

  @Override
  public void onClose(WebSocket session, int arg1, String arg2, boolean arg3) {
    logger.debug("User session closed" + trimResourceDesString(session.getResourceDescriptor()), arg1 + " " + arg2 + " " + arg3);
  }

  @Override
  public void onError(WebSocket session, Exception ex) {
    ex.printStackTrace();
    if (logger != null && session != null) {
      logger.error("Error for User session " + trimResourceDesString(session.getResourceDescriptor()) + " :" + ex.getMessage(), ex.getCause());
    }
  }

  @Override
  public void onMessage(WebSocket session, String message) {
    onClientMessage(session, message);
  }

  @Override
  public void onOpen(WebSocket session, ClientHandshake arg1) {
    String resourceDescriptor = trimResourceDesString(session.getResourceDescriptor());
    try {
      if ((settingService != null && !settingService.getBooleanValue("gamification.gamificationEnabled", false)) || resourceDescriptor == null || resourceDescriptor.isEmpty()) {
        // Gamification Disabled Do nothing.
        session.close();
        return;
      }
      if (resourceDescriptor.contains("printStatusInLogs")) {
        if (listOfSessionQueues.size() == 0) {
          logger.info("Gamification Listner is not yet started. Waiting for Client to Connect");
        } else {
          logger.info("Gamification Listner is started. Current Load Details are below:");
          logger.info("-----------------------  Queue Number   -----------------------  Number Of Sessions  --------------------");
          int index = 1;
          for (GamificationWebsocketThread thread : gamificationThreads) {
            logger.info("-----------------------       " + index + "       -----------------------         " + thread.getNoOfActiveSessions() + "   --------------------");
            index += 1;
          }
        }
        session.close();
        return;
      }
      if (listOfSessionQueues.size() == 0) {
        startThreads();
      }

      if (getGamificationLocalService().validateGamificationOneTimeToken(resourceDescriptor)) {
        logger.info("Token validated Successfully : " + resourceDescriptor);
        keyQidMap.put(resourceDescriptor, session.getRemoteSocketAddress() != null ? session.getRemoteSocketAddress().getHostName() : "-");
        GamificationResponse res = new GamificationResponse();
        res.setStatus("sessionKey:" + resourceDescriptor);
        session.send(new Gson().toJson(res, GamificationResponse.class));
      } else {
        logger.error("Token validation failed  : " + resourceDescriptor);
        session.close();
      }
    } catch (Exception e) {
      session.close();
      logger.error("Error while initiating User session " + session.getRemoteSocketAddress() + resourceDescriptor + " :" + e.getMessage(), e.getCause());
    }
  }

  @Override
  public void onStart() {
    logger.debug("Cuco Gamification Server Started at Port " + getPortNumber());
  }

  public GamificationHttpService getGamificationHttpService() {
    return gamificationHttpService;
  }

  @Autowired
  public void setGamificationHttpService(GamificationHttpService gamificationHttpService) {
    this.gamificationHttpService = gamificationHttpService;
  }

  @PreDestroy
  @Override
  public void stop() throws IOException, InterruptedException {
    super.stop();
    logger.info("Stopping Gamification threads");
    for (GamificationWebsocketThread thread : gamificationThreads) {
      try {
        thread.stopNow();
      } catch (Exception ex) {
        if (logger != null) {
          logger.error("Error while stopping threads", ex);
        }
      }
    }
    try {
      if (executorService != null) {
        executorService.shutdown();
        executorService.shutdownNow();
        logger.info("Gamification threads stopped");
      }
    } catch (Exception ex) {
      if (logger != null) {
        logger.error("Error while stopping threads", ex);
      }
    }
  }

  public LocalSettingService getLocalSettingService() {
    return localSettingService;
  }

  @Autowired
  public void setLocalSettingService(LocalSettingService localSettingService) {
    this.localSettingService = localSettingService;
  }

  public int getPortNumber() {
    return portNumber;
  }

  public void setPortNumber(int portNumber) {
    this.portNumber = portNumber;
  }

  public GamificationLocalService getGamificationLocalService() {
    return gamificationLocalService;
  }

  public void setGamificationLocalService(GamificationLocalService gamificationLocalService) {
    this.gamificationLocalService = gamificationLocalService;
  }
}

class CucoWebSocketWrapper {
  WebSocket socket;
  String qid;
  String Key;

  public CucoWebSocketWrapper(WebSocket socket, String qid, String key) {
    super();
    this.socket = socket;
    this.qid = qid;
    Key = key;
  }

  public WebSocket getSocket() {
    return socket;
  }

  public void setSocket(WebSocket socket) {
    this.socket = socket;
  }

  public String getQid() {
    return qid;
  }

  public void setQid(String qid) {
    this.qid = qid;
  }

  public String getKey() {
    return Key;
  }

  public void setKey(String key) {
    Key = key;
  }

}