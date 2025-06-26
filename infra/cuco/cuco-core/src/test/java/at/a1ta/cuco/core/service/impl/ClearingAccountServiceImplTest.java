package at.a1ta.cuco.core.service.impl;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;

import org.apache.commons.lang.NullArgumentException;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.cuco.core.dao.db.ClearingAccountDao;
import at.a1ta.cuco.core.shared.dto.ClearingAccount;

@RunWith(MockitoJUnitRunner.class)
public class ClearingAccountServiceImplTest {

  private ClearingAccountServiceImpl service;
  private static final Long ACCOUNT_NUMBER = Long.valueOf(123);

  @Mock
  private ClearingAccountDao accountDaoMock;

  @Before
  public void setUp() {
    service = new ClearingAccountServiceImpl();
    service.setClearingAccountDao(accountDaoMock);

    ClearingAccount account = new ClearingAccount(ACCOUNT_NUMBER);
    Mockito.when(accountDaoMock.getClearingAccountForPhonenumber(Matchers.isNotNull(String.class))).thenReturn(account);
  }

  @Test
  public void getClearingNumberForPhonenumber() {
    Long number = service.getClearingNumberForPhonenumber("+43/1234567");

    verify(accountDaoMock).getClearingAccountForPhonenumber(Matchers.anyString());
    assertEquals(ACCOUNT_NUMBER, number);
  }

  @Test
  public void getClearingNumberForPhonenumberNull() {
    Mockito.when(accountDaoMock.getClearingAccountForPhonenumber(Matchers.isNotNull(String.class))).thenReturn(null);

    Long number = service.getClearingNumberForPhonenumber("+43/1234567");

    verify(accountDaoMock).getClearingAccountForPhonenumber(Matchers.anyString());
    assertNull(number);
  }

  @Test(expected = NullArgumentException.class)
  public void getClearingNumberForPhonenumberWithException() {
    service.getClearingNumberForPhonenumber(null);
  }

  @Test
  public void testGetByAccountNumber() {
    service.getByAccountNumber(ACCOUNT_NUMBER);

    verify(accountDaoMock).getByAccountNumber(Matchers.anyLong());
  }

  @Test
  public void testGetActiveTaByPartyId() {
    service.getActiveTaByPartyId(Long.valueOf(333));

    verify(accountDaoMock).getActiveTaByPartyId(Matchers.anyLong());
  }

  @SuppressWarnings("unchecked")
  @Test
  public void testGetByPartyId() {
    when(accountDaoMock.getByPartyIds(Matchers.any(ArrayList.class))).thenReturn(new ArrayList<ClearingAccount>());

    service.getByPartyId(Long.valueOf(123));
    verify(accountDaoMock).getByPartyIds(Matchers.any(ArrayList.class));
  }

}
