package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.UsageDataDao;
import at.a1ta.cuco.core.shared.dto.usagedata.InetUsage;
import at.a1ta.cuco.core.shared.dto.usagedata.MobileUsage;
import at.a1ta.cuco.core.shared.dto.usagedata.NetworkProvider;
import at.a1ta.cuco.core.shared.dto.usagedata.VoiceUsage;

public class UsageDataDaoImpl extends AbstractDao implements UsageDataDao {

  private static final String CUSTOMER_IDS = "customerIds";
  private static final String PHONE_NUMBER = "phoneNumber";
  private static final String CUSTOMER_ID = "customerId";
  private static final String BAN_ID = "banId";

  @Override
  public List<String> getFixedLineNumbers(long partyId) {
    return performListQuery("UsageData.GetFixedLineNumbers", partyId);
  }

  @Override
  public List<String> getMobileBanNumbers(long partyId) {
    return performListQuery("UsageData.GetMobileBans", partyId);
  }

  @Override
  public List<String> getMobileNumbers(long partyId, String ban) {
    Map<String, Object> params = new HashMap<String, Object>(2);
    appendCustomerId(partyId, params);
    params.put(BAN_ID, ban);
    return performListQuery("UsageData.GetMobileNumbers", params);
  }

  @Override
  public List<String> getAonNumbers(long partyId) {
    return performListQuery("UsageData.GetAonNumbers", partyId);
  }

  @Override
  public List<VoiceUsage> getFixedLineUsage(List<Long> partyIds) {
    final Map<String, Object> params = new HashMap<String, Object>();

    params.put(CUSTOMER_IDS, partyIds);
    return performListQuery("UsageData.GetFixedLineUsage", params);
  }

  @Override
  public List<VoiceUsage> getFixedLineUsage(long partyId) {
    final Map<String, Object> params = new HashMap<String, Object>();

    appendCustomerId(partyId, params);
    return performListQuery("UsageData.GetFixedLineUsage", params);
  }

  @Override
  public List<VoiceUsage> getFixedLineUsage(long partyId, String phoneNumber) {
    final Map<String, Object> params = new HashMap<String, Object>();

    appendCustomerId(partyId, params);
    appendPhoneNumber(phoneNumber, params);
    return performListQuery("UsageData.GetFixedLineUsage", params);
  }

  @Override
  public List<VoiceUsage> getFixedLineZoneUsage(long partyId, String phoneNumber) {
    final Map<String, Object> params = new HashMap<String, Object>();

    appendCustomerId(partyId, params);
    appendPhoneNumber(phoneNumber, params);
    return performListQuery("UsageData.GetFixedLineZoneUsage", params);
  }

  @Override
  public List<VoiceUsage> getFixedLineTimeZones(long partyId, String phoneNumber) {
    final Map<String, Object> params = new HashMap<String, Object>();

    appendCustomerId(partyId, params);
    appendPhoneNumber(phoneNumber, params);
    return performListQuery("UsageData.GetTimeZones", params);
  }

  @Override
  public List<InetUsage> getAonUsageData(List<Long> partyIds, NetworkProvider provider) {
    Map<String, Object> params = new HashMap<String, Object>();

    params.put(CUSTOMER_IDS, partyIds);
    return performListQuery("UsageData.GetAonUsageData", params);
  }

  @Override
  public List<InetUsage> getAonUsageData(long partyId, NetworkProvider provider) {
    Map<String, Object> params = new HashMap<String, Object>();

    appendCustomerId(partyId, params);
    return performListQuery("UsageData.GetAonUsageData", params);
  }

  @Override
  public List<InetUsage> getAonUsageData(long partyId, String aonAccountNumber, NetworkProvider provider) {
    Map<String, Object> params = new java.util.HashMap<String, Object>();

    appendCustomerId(partyId, params);
    params.put(PHONE_NUMBER, aonAccountNumber);
    return performListQuery("UsageData.GetAonUsageData", params);
  }

  @Override
  public List<MobileUsage> getMobileUsageDataPerBan(long partyId, String ban) {
    Map<String, Object> params = new java.util.HashMap<String, Object>();

    appendCustomerId(partyId, params);
    params.put(BAN_ID, ban);
    return performListQuery("UsageData.GetMobileUsageData", params);
  }

  @Override
  public List<MobileUsage> getMobileUsageData(List<Long> partyIds) {
    Map<String, Object> params = new java.util.HashMap<String, Object>();

    params.put(CUSTOMER_IDS, partyIds);
    return performListQuery("UsageData.GetMobileUsageData", params);
  }

  @Override
  public List<MobileUsage> getMobileUsageData(long partyId) {
    Map<String, Object> params = new java.util.HashMap<String, Object>();

    appendCustomerId(partyId, params);
    return performListQuery("UsageData.GetMobileUsageData", params);
  }

  @Override
  public List<MobileUsage> getMobileUsageData(long partyId, String phoneNumber) {
    Map<String, Object> params = new java.util.HashMap<String, Object>();

    appendCustomerId(partyId, params);
    appendPhoneNumber(phoneNumber, params);
    return performListQuery("UsageData.GetMobileUsageData", params);
  }

  private void appendPhoneNumber(String phoneNumber, final Map<String, Object> params) {
    params.put(PHONE_NUMBER, phoneNumber);
  }

  private void appendCustomerId(long partyId, final Map<String, Object> params) {
    params.put(CUSTOMER_ID, partyId);
  }

}