package at.a1ta.cuco.core.service.impl;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

import org.apache.commons.lang.StringUtils;
import org.springframework.beans.factory.ObjectFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.esb.MobilPointsDao;
import at.a1ta.cuco.core.service.MobilPointsService;
import at.a1ta.cuco.core.service.PhoneNumberService;
import at.a1ta.cuco.core.shared.dto.PhoneNumberStructure;
import at.a1ta.cuco.core.shared.dto.mobilpoints.BusinessHardwareReplacement;
import at.a1ta.cuco.core.shared.dto.mobilpoints.MobilPoints;
import at.a1ta.cuco.core.shared.dto.mobilpoints.MobilPointsBundle;

@Service
public class MobilPointsServiceImpl implements MobilPointsService {
  @Autowired
  private PhoneNumberService phonenumberService;

  @Autowired
  private ObjectFactory<MobilPointsCallable> mobilePointsCallableFactory;
  @Autowired
  private ObjectFactory<BusinessHardwareReplacementCallable> businessHardwareReplacementCallableFactory;
  @Autowired
  private MobilPointsDao mobilPointsDao;

  private ExecutorService executor = Executors.newCachedThreadPool();

  @Override
  public MobilPointsBundle getMobilPoints(String phoneNumber) {
    try {
      PhoneNumberStructure phoneNumberStructure = getPhoneNumberStructureFromString(phoneNumber);
      long billingAccountNumber = getBillingAccountNumber(phoneNumberStructure);

      MobilPointsCallable mobilePointsCallable = mobilePointsCallableFactory.getObject();
      mobilePointsCallable.setPhoneNumberStructure(phoneNumberStructure);
      Future<MobilPoints> futureMobilPoints = executor.submit(mobilePointsCallable);

      BusinessHardwareReplacementCallable businessHardwareReplacementCallable = businessHardwareReplacementCallableFactory.getObject();
      businessHardwareReplacementCallable.setBillingAccountNumber(billingAccountNumber);
      Future<BusinessHardwareReplacement> futureBusinessHardwareReplacement = executor.submit(businessHardwareReplacementCallable);

      MobilPoints mobilPoints = futureMobilPoints.get();
      BusinessHardwareReplacement businessHardwareReplacement = futureBusinessHardwareReplacement.get();

      return createBundle(phoneNumber, mobilPoints, businessHardwareReplacement);
    } catch (Exception e) {
      throw new RuntimeException("Error during requesting Mobil Points and Business Hardware Replacement", e);
    }
  }

  @Override
  public MobilPoints getMobilPoints(PhoneNumberStructure phoneNumberStructure) {
    return mobilPointsDao.getMobilPoints(phoneNumberStructure);
  }

  @Override
  public MobilPointsBundle getBusinessHardwareReplacement(String ban) {
    if (StringUtils.isEmpty(ban)) {
      BusinessHardwareReplacement hr = new BusinessHardwareReplacement();
      hr.setBusinessRewardingAccountsAvailable(false);
      return createBundle(ban, null, hr);
    }
    BusinessHardwareReplacementCallable businessHardwareReplacementCallable = businessHardwareReplacementCallableFactory.getObject();
    businessHardwareReplacementCallable.setBillingAccountNumber(Long.valueOf(ban));
    BusinessHardwareReplacement result = businessHardwareReplacementCallable.call();

    return createBundle(ban, null, result);
  }

  private long getBillingAccountNumber(PhoneNumberStructure phoneNumberStr) {
    return phonenumberService.getBillingAccountNumberForPhoneNumber(phoneNumberStr.getCountryCode(), phoneNumberStr.getOnkz(), phoneNumberStr.getNumber());
  }

  private PhoneNumberStructure getPhoneNumberStructureFromString(String phoneNumber) {
    return phonenumberService.parse(phoneNumber);
  }

  private MobilPointsBundle createBundle(String phoneNumber, MobilPoints mobilPoints, BusinessHardwareReplacement hr) {
    MobilPointsBundle bundle = new MobilPointsBundle();
    bundle.setPhoneNumber(phoneNumber);
    bundle.setMobilPoints(mobilPoints);
    bundle.setBusinessHardwareReplacement(hr);
    return bundle;
  }
}
