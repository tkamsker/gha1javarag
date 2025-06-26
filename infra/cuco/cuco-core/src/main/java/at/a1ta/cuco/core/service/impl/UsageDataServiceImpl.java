package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.UsageDataDao;
import at.a1ta.cuco.core.service.PhoneNumberService;
import at.a1ta.cuco.core.service.UsageDataService;
import at.a1ta.cuco.core.shared.dto.usagedata.InetUsage;
import at.a1ta.cuco.core.shared.dto.usagedata.MobileUsage;
import at.a1ta.cuco.core.shared.dto.usagedata.NetworkProvider;
import at.a1ta.cuco.core.shared.dto.usagedata.VoiceUsage;

@Service
public class UsageDataServiceImpl implements UsageDataService {

  @Autowired
  private UsageDataDao usageDataDao;

  @Autowired
  private PhoneNumberService phoneNumberService;

  @Override
  public List<String> getFixedLineNumbers(long partyId) {
    return usageDataDao.getFixedLineNumbers(partyId);
  }

  @Override
  public List<String> getMobileBanNumbers(long partyId) {
    return usageDataDao.getMobileBanNumbers(partyId);
  }

  @Override
  public List<String> getMobileNumbers(long partyId, String ban) {
    return usageDataDao.getMobileNumbers(partyId, ban);
  }

  @Override
  public List<String> getAonNumbers(long partyId) {
    return usageDataDao.getAonNumbers(partyId);
  }

  @Override
  public List<VoiceUsage> getFixedLineUsage(List<Long> partyIds) {
    return usageDataDao.getFixedLineUsage(partyIds);
  }

  @Override
  public List<VoiceUsage> getFixedLineUsage(long partyId) {
    return usageDataDao.getFixedLineUsage(partyId);
  }

  @Override
  public List<VoiceUsage> getFixedLineUsage(long partyId, String phoneNumber) {
    return usageDataDao.getFixedLineUsage(partyId, phoneNumber);
  }

  @Override
  public List<VoiceUsage> getFixedLineZoneUsage(long partyId, String phoneNumber) {
    return usageDataDao.getFixedLineZoneUsage(partyId, phoneNumber);
  }

  @Override
  public List<VoiceUsage> getFixedLineTimeZones(long partyId, String phoneNumber) {
    return usageDataDao.getFixedLineTimeZones(partyId, phoneNumber);
  }

  @Override
  public List<InetUsage> getAonUsageData(List<Long> partyIds, NetworkProvider provider) {
    return usageDataDao.getAonUsageData(partyIds, provider);
  }

  @Override
  public java.util.List<InetUsage> getAonUsageData(long partyId, NetworkProvider provider) {
    return usageDataDao.getAonUsageData(partyId, provider);
  }

  @Override
  public List<InetUsage> getAonUsageData(long partyId, String aonNumber, NetworkProvider networkProvider) {
    return usageDataDao.getAonUsageData(partyId, aonNumber, networkProvider);
  }

  @Override
  public List<MobileUsage> getMobileUsageData(List<Long> partyIds) {
    return usageDataDao.getMobileUsageData(partyIds);
  }

  @Override
  public List<MobileUsage> getMobileUsageDataPerBan(long partyId, String ban) {
    return usageDataDao.getMobileUsageDataPerBan(partyId, ban);
  }

  @Override
  public List<MobileUsage> getMobileUsageData(long partyId) {
    return usageDataDao.getMobileUsageData(partyId);
  }

  @Override
  public List<MobileUsage> getMobileUsageData(long partyId, String phoneNumber) {
    return usageDataDao.getMobileUsageData(partyId, phoneNumber);
  }

}
