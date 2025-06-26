package at.a1ta.cuco.core.service;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.usagedata.InetUsage;
import at.a1ta.cuco.core.shared.dto.usagedata.MobileUsage;
import at.a1ta.cuco.core.shared.dto.usagedata.NetworkProvider;
import at.a1ta.cuco.core.shared.dto.usagedata.VoiceUsage;

public interface UsageDataService {

  List<String> getFixedLineNumbers(long partyId);

  List<String> getMobileBanNumbers(long partyId);

  List<String> getMobileNumbers(long partyId, String ban);

  List<String> getAonNumbers(long partyId);

  List<VoiceUsage> getFixedLineUsage(List<Long> partyIds);

  List<VoiceUsage> getFixedLineUsage(long partyId);

  List<VoiceUsage> getFixedLineUsage(long partyId, String phoneNumber);

  List<VoiceUsage> getFixedLineZoneUsage(long partyId, String phoneNumber);

  List<VoiceUsage> getFixedLineTimeZones(long partyId, String phoneNumber);

  List<InetUsage> getAonUsageData(List<Long> partyIds, NetworkProvider provider);

  List<InetUsage> getAonUsageData(long partyId, NetworkProvider provider);

  List<InetUsage> getAonUsageData(long partyId, String aonNumber, NetworkProvider networkProvider);

  List<MobileUsage> getMobileUsageDataPerBan(long partyId, String ban);

  List<MobileUsage> getMobileUsageData(List<Long> partyIds);

  List<MobileUsage> getMobileUsageData(long partyId);

  List<MobileUsage> getMobileUsageData(long partyId, String phoneNumber);

}