package at.a1ta.cuco.core.dao.db.impl;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.ClearingAccountDao;
import at.a1ta.cuco.core.shared.dto.ClearingAccount;

public class ClearingAccountDaoImpl extends AbstractDao implements ClearingAccountDao {
  @Override
  public List<ClearingAccount> getByPartyIds(ArrayList<Long> partyIds) {
    if (partyIds != null && partyIds.size() > 0) {
      Map<String, Object> params = new HashMap<String, Object>(2);
      params.put("partyIds", partyIds);
      return performListQuery("ClearingAccount.getByPartyIds", params);
    }
    return new ArrayList<ClearingAccount>();
  }

  @Override
  public ClearingAccount getClearingAccountForPhonenumber(String phonenubmer) {
    return performObjectQuery("ClearingAccount.GetForPhonenumber", phonenubmer);
  }

  @Override
  public ClearingAccount getByAccountNumber(Long accountNumber) {
    return performObjectQuery("ClearingAccount.getByAccountNumber", accountNumber);
  }

  @Override
  public List<ClearingAccount> getActiveTaByPartyId(Long partyId) {
    return performListQuery("ClearingAccount.getActiveTaByPartyId", partyId);
  }
}
