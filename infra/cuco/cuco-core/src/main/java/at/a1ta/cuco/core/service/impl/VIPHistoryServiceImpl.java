package at.a1ta.cuco.core.service.impl;

import java.util.Date;
import java.util.List;

import org.apache.commons.lang.NullArgumentException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import at.a1ta.cuco.core.dao.db.PartyDao;
import at.a1ta.cuco.core.dao.db.VIPHistoryDao;
import at.a1ta.cuco.core.service.KumsCustomerService;
import at.a1ta.cuco.core.service.VIPHistoryService;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.VIPHistoryEntry;

@Service
public class VIPHistoryServiceImpl implements VIPHistoryService {

  private static final Logger logger = LoggerFactory.getLogger(VIPHistoryServiceImpl.class);

  @Autowired
  private VIPHistoryDao vipHistoryDao;

  @Autowired
  @Qualifier("cucoCustomerDao")
  private PartyDao customerDao;

  @Autowired
  private KumsCustomerService kumsCustomerService;

  @Override
  public List<VIPHistoryEntry> getVIPHistory(Long customerId) {
    if (customerId == null) {
      throw new NullArgumentException("customerId");
    }
    return vipHistoryDao.getVIPHistory(customerId);
  }

  @Override
  public List<VIPHistoryEntry> getVIPHistory(Date from, Date to, String searchTerm, String vipStatus) {
    return vipHistoryDao.getVIPHistory(from, to, searchTerm, vipStatus);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void saveVIPStatusAndHistory(VIPHistoryEntry vipHistory, String lastChangeDate, Party cucoCustomer, String uUser) {
    if (vipHistory == null) {
      throw new NullArgumentException("vipHistory");
    }
    vipHistoryDao.saveVIPHistory(vipHistory);

    if (cucoCustomer != null) {
      customerDao.saveCucoCustomer(cucoCustomer);
    }

    kumsCustomerService.saveVipStatus(String.valueOf(vipHistory.getCustomerId()), lastChangeDate, String.valueOf(vipHistory.getNewStatus() != null ? vipHistory.getNewStatus() : " "), uUser);

  }

}
