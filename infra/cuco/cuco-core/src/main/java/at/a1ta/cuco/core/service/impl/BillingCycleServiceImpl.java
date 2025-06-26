package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.Date;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.billingcycle.BillingCycleDao;
import at.a1ta.cuco.core.service.BillingCycleService;
import at.a1ta.cuco.core.shared.dto.BillingCycle;
import at.a1ta.cuco.core.shared.dto.BillingCycleEntry;

/**
 * @author q914835 manuels
 */
@Service
public class BillingCycleServiceImpl implements BillingCycleService {

  private static String USAGE_END_DATE_STR = "Usage End-Date";

  private BillingCycleDao billingCycleDao;

  private KumsAccountService kumsAccountService;

  @Override
  public ArrayList<BillingCycle> getBillingCycle(Long clearingAccount) {
    try {
      String vblock = kumsAccountService.getAccount(clearingAccount.toString()).getBILLCYCLID();
      return (ArrayList<BillingCycle>) billingCycleDao.getBillingCycle(vblock);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  public Date getUsageEndDate(Long clearingAccount) throws Exception {
    ArrayList<BillingCycle> bcs = getBillingCycle(clearingAccount);
    if (bcs != null && bcs.size() > 0) {
      BillingCycle first = bcs.get(0);
      for (BillingCycleEntry e : first.getEntries()) {
        if (e.getStep().contains(USAGE_END_DATE_STR)) {
          return e.getFrom();
        }
      }
    }
    return null;
  }

  @Autowired
  public void setBillingCycleDao(BillingCycleDao billingCycleDao) {
    this.billingCycleDao = billingCycleDao;
  }

  @Autowired
  public void setKumsAccountService(KumsAccountService kumsAccountService) {
    this.kumsAccountService = kumsAccountService;
  }
}
