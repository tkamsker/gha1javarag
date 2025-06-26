package at.a1ta.cuco.core.dao.db;

import java.util.ArrayList;
import java.util.List;

import at.a1ta.cuco.core.shared.dto.ClearingAccount;

public interface ClearingAccountDao {
  List<ClearingAccount> getByPartyIds(ArrayList<Long> partyIds);

  ClearingAccount getClearingAccountForPhonenumber(String phonenubmer);

  ClearingAccount getByAccountNumber(Long accountNumber);

  List<ClearingAccount> getActiveTaByPartyId(Long partyId);
}
