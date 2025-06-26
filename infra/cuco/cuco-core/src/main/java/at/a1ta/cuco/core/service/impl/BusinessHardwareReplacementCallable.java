package at.a1ta.cuco.core.service.impl;

import java.util.concurrent.Callable;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import at.a1ta.cuco.core.dao.esb.BusinessHardwareReplacementDao;
import at.a1ta.cuco.core.shared.dto.mobilpoints.BusinessHardwareReplacement;

@Component
public class BusinessHardwareReplacementCallable implements Callable<BusinessHardwareReplacement> {
  private static final Logger logger = LoggerFactory.getLogger(MobilPointsCallable.class);
  private long billingAccountNumber;

  private BusinessHardwareReplacementDao businessHardwareReplacementDao;

  @Override
  public BusinessHardwareReplacement call() {
    try {
      return businessHardwareReplacementDao.getBusinessHardwareReplacement(billingAccountNumber);
    } catch (Exception e) {
      logger.error("Error during loading Business Hardware Replacement", e);
      return null;
    }
  }

  public void setBillingAccountNumber(long billingAccountNumber) {
    this.billingAccountNumber = billingAccountNumber;
  }

  @Autowired
  public void setBusinessHardwareReplacementDao(BusinessHardwareReplacementDao businessHardwareReplacementDao) {
    this.businessHardwareReplacementDao = businessHardwareReplacementDao;
  }
}
