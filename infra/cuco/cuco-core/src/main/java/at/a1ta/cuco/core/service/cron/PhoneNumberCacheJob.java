package at.a1ta.cuco.core.service.cron;

import javax.annotation.PostConstruct;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.orm.ibatis.support.SqlMapClientDaoSupport;
import org.springframework.stereotype.Component;

import at.a1ta.bite.core.server.cron.AbstractCronJob;
import at.a1ta.cuco.core.dao.db.PhoneNumberDao;

@Component
public class PhoneNumberCacheJob extends AbstractCronJob {
  private static final Logger logger = LoggerFactory.getLogger(PhoneNumberCacheJob.class);

  @Autowired
  private PhoneNumberDao phoneNumberDao;

  @Override
  protected void process() {
    flushAndCache();
  }

  @Override
  protected String getJobId() {
    return "phonenumber.cache";
  }

  @PostConstruct
  private void flushAndCache() {
    try {
      final long start = System.currentTimeMillis();

      ((SqlMapClientDaoSupport) phoneNumberDao).getSqlMapClient().flushDataCache();

      phoneNumberDao.getCountryCodes();
      phoneNumberDao.getOnkzs();
      phoneNumberDao.getSpecialOnkzs();

      final long duration = System.currentTimeMillis() - start;
      logger.debug("Executed queries for caching phone numbers results in " + duration + " msec.");
    } catch (Exception e) {
      logger.error("Error during executing queries for caching phone number results", e);
    }
  }
}
