package at.a1ta.cuco.core.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.cuco.core.dao.db.CucoLogsDao;
import at.a1ta.cuco.core.service.CucoLogsService;
import at.a1ta.cuco.core.shared.dto.BillingAccountNumber;
import at.a1ta.cuco.core.shared.dto.Party;

@Service
public class CucoLogsServiceImpl implements CucoLogsService {

  @Autowired
  private CucoLogsDao cucoLogsDao;

  @Autowired
  private SettingService settingService;
  private static final String PARTYLOADED_LOGTYPE = "Party Loaded";

  @Autowired
  public CucoLogsServiceImpl(CucoLogsDao cucoLogsDao) {
    this.cucoLogsDao = cucoLogsDao;
  }

  @Override
  public void entryForPartyLoaded(Party party, UserInfo userInfo, BillingAccountNumber curBan) {
    this.cucoLogsDao.insertLogEntryForPartyLoaded(party.getId(), userInfo.getName(), userInfo.getUsername(), curBan.getBan() + "",
        settingService.getValueOrDefault("cucoLogsPartyLoadedLogType", PARTYLOADED_LOGTYPE));

  }

}
