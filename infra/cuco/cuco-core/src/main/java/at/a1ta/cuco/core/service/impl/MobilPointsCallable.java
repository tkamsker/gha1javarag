package at.a1ta.cuco.core.service.impl;

import java.util.concurrent.Callable;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Scope;
import org.springframework.stereotype.Component;

import at.a1ta.cuco.core.dao.esb.MobilPointsDao;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;
import at.a1ta.cuco.core.shared.dto.mobilpoints.MobilPoints;

@Component
@Scope("prototype")
public class MobilPointsCallable implements Callable<MobilPoints> {
  private static Logger logger = LoggerFactory.getLogger(MobilPointsCallable.class);

  private MobilPointsDao mobilPointsDao;
  private PhoneNumberStructure phoneNumberStructure;

  @Override
  public MobilPoints call() {
    try {
      return mobilPointsDao.getMobilPoints(phoneNumberStructure);
    } catch (Exception e) {
      logger.error("Error during loading Mobil Points", e);
      return null;
    }
  }

  @Autowired
  public void setMobilPointsDao(MobilPointsDao mobilPointsDao) {
    this.mobilPointsDao = mobilPointsDao;
  }

  public void setPhoneNumberStructure(PhoneNumberStructure phoneNumberStructure) {
    this.phoneNumberStructure = phoneNumberStructure;
  }
}