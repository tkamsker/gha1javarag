package at.a1ta.cuco.core.dao.billingcycle;

import java.util.List;

import at.a1ta.cuco.core.shared.dto.BillingCycle;

public interface BillingCycleDao {

  public List<BillingCycle> getBillingCycle(String vBlock);
}
