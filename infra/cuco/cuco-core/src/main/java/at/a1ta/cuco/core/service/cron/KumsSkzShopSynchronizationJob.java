package at.a1ta.cuco.core.service.cron;

import java.rmi.RemoteException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import at.a1ta.bite.core.server.cron.AbstractCronJob;
import at.a1ta.bite.core.server.service.KumsCommonService;
import at.a1ta.bite.core.shared.EnvironmentProfiles;

@Profile(EnvironmentProfiles.TRUSTED)
@Component
public class KumsSkzShopSynchronizationJob extends AbstractCronJob {

  private static final Logger logger = LoggerFactory.getLogger(KumsSkzShopSynchronizationJob.class);

  private KumsCommonService kumsCommonService;

  @Override
  protected void process() {
    try {
      logger.debug("Starting Shop Synchronization...");
      kumsCommonService.updateSkzShops();
      logger.debug("Shop Synchronization finished.");
    } catch (RemoteException e) {
      logger.error("Shop Synchronization failed: ", e);
    }

  }

  @Override
  protected String getJobId() {
    return "kumsSkzShopSynchronization";
  }

  @Autowired
  public void setKumsCommonService(KumsCommonService kumsCommonService) {
    this.kumsCommonService = kumsCommonService;
  }
}
