package at.a1ta.cuco.core.service.cron;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import at.a1ta.bite.core.server.cron.AbstractCronJob;
import at.a1ta.bite.core.server.service.CorporateDirectorySynchronizationService;
import at.a1ta.bite.core.shared.EnvironmentProfiles;

@Profile(EnvironmentProfiles.TRUSTED)
@Component
public class LDAPSynchronizationJob extends AbstractCronJob {

  @Autowired
  private CorporateDirectorySynchronizationService cdService;

  @Override
  protected void process() {
    cdService.udpateAllUsers();
  }

  @Override
  protected String getJobId() {
    return "ldapSynchronization";
  }
}
