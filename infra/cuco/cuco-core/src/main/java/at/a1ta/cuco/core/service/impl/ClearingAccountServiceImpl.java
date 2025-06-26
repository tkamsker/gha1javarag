package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.ClearingAccountDao;
import at.a1ta.cuco.core.service.ClearingAccountService;
import at.a1ta.cuco.core.shared.dto.ClearingAccount;

@Service
public class ClearingAccountServiceImpl implements ClearingAccountService {

  private ClearingAccountDao clearingAccountDao;

  @Override
  public List<ClearingAccount> getByPartyId(Long partyId) {
    final ArrayList<Long> ids = new ArrayList<Long>(1);
    ids.add(partyId);
    return getByPartyIds(ids);
  }

  @Override
  public List<ClearingAccount> getByPartyIds(ArrayList<Long> partyIds) {
    return clearingAccountDao.getByPartyIds(partyIds);
  }

  @Override
  public ClearingAccount getClearingAccountForPhonenumber(String phonenumber) {
    if (phonenumber == null) {
      throw new org.apache.commons.lang.NullArgumentException("phonenumber");
    }
    return clearingAccountDao.getClearingAccountForPhonenumber(phonenumber);
  }

  @Override
  public Long getClearingNumberForPhonenumber(String phonenubmer) {
    final ClearingAccount c = getClearingAccountForPhonenumber(phonenubmer);
    return c != null ? c.getAccountNumber() : null;
  }

  @Override
  public ClearingAccount getByAccountNumber(Long accountNumber) {
    return clearingAccountDao.getByAccountNumber(accountNumber);
  }

  @Override
  public List<ClearingAccount> getActiveTaByPartyId(Long partyId) {
    return clearingAccountDao.getActiveTaByPartyId(partyId);
  }

  @Autowired
  public void setClearingAccountDao(ClearingAccountDao clearingAccountDao) {
    this.clearingAccountDao = clearingAccountDao;
  }

}
