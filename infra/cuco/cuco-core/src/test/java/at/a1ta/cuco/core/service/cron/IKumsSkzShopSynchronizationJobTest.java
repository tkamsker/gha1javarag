package at.a1ta.cuco.core.service.cron;

import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import at.a1ta.bite.core.server.dao.CronjobConfigurationDao;
import at.a1ta.bite.core.server.service.KumsCommonService;

@Ignore
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(locations = {"classpath:testApplicationContext-cuco-core.xml"})
public class IKumsSkzShopSynchronizationJobTest {

  @Autowired
  KumsCommonService kumsCommonService;

  @Autowired
  CronjobConfigurationDao cronjobConfigurationDao;

  @Test
  public void runJobTest() {
    KumsSkzShopSynchronizationJob job = new KumsSkzShopSynchronizationJob();
    job.setKumsCommonService(kumsCommonService);
    job.setCronjobConfigurationDao(cronjobConfigurationDao);
    job.run();
  }

}
