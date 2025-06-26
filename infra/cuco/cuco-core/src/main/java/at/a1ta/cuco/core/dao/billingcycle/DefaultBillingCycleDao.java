package at.a1ta.cuco.core.dao.billingcycle;

import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.shared.dto.BillingCycle;

public class DefaultBillingCycleDao extends AbstractDao implements BillingCycleDao {

  @Override
  public List<BillingCycle> getBillingCycle(String vBlock) {
    List<BillingCycle> cycles = performListQuery("BillingCycle.getVBlock", vBlock);

    int cyclecnt = cycles.size();

    if (cyclecnt > 1) {
      BillingCycle cycle1 = cycles.get(0);

      Calendar cal = new GregorianCalendar();
      cal.add(Calendar.DAY_OF_MONTH, 5);

      Date now = cal.getTime();

      if (cycle1.getBillingDate().after(now)) {
        for (int i = cyclecnt - 1; i > 0; i--) {
          cycles.remove(i);
        }
      } else {
        for (int i = cyclecnt - 1; i > 1; i--) {
          cycles.remove(i);
        }
      }
    }
    return cycles;
  }
}
