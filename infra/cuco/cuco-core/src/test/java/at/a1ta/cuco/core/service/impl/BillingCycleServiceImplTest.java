package at.a1ta.cuco.core.service.impl;

import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertTrue;
import static org.mockito.Matchers.anyLong;
import static org.mockito.Matchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;

import org.junit.Test;

import at.a1ta.cuco.core.dao.billingcycle.BillingCycleDao;
import at.a1ta.cuco.core.shared.dto.BillingCycle;
import at.a1ta.cuco.core.shared.dto.BillingCycleEntry;
import at.telekom.www.eai.wstokumsretrieveaccount.WSKUMSRetrieveAccountResponseACC1ACCOUNTType;

public class BillingCycleServiceImplTest {

  private final Date endDate = new Date();

  @Test
  public void testGetBillingCycle1() throws Exception {
    BillingCycleDao daoMock = mock(BillingCycleDao.class);
    KumsAccountService accountServiceMock = mock(KumsAccountService.class);
    BillingCycleServiceImpl service = createService(daoMock, accountServiceMock);

    when(accountServiceMock.getAccount(anyString())).thenReturn(createAccountObject());
    when(daoMock.getBillingCycle(anyString())).thenReturn(new ArrayList<BillingCycle>());

    service.getBillingCycle(Long.valueOf(1234567));

    verify(accountServiceMock).getAccount(anyString());
    verify(daoMock).getBillingCycle(anyString());
  }

  private WSKUMSRetrieveAccountResponseACC1ACCOUNTType createAccountObject() {
    WSKUMSRetrieveAccountResponseACC1ACCOUNTType account = WSKUMSRetrieveAccountResponseACC1ACCOUNTType.Factory.newInstance();
    account.setBILLCYCLID("testId");
    return account;
  }

  @Test
  public void testGetUsageEndDateNoCycles() throws Exception {
    BillingCycleServiceImpl serviceMock = createServicePartialMock();
    when(serviceMock.getBillingCycle(anyLong())).thenReturn(new ArrayList<BillingCycle>());
    when(serviceMock.getUsageEndDate(anyLong())).thenCallRealMethod();

    Date usageEndDate = serviceMock.getUsageEndDate(Long.valueOf(1234567));

    verify(serviceMock).getBillingCycle(anyLong());
    assertNull(usageEndDate);
  }

  @Test
  public void testGetUsageEndDateWithCyclesNotingFound() throws Exception {
    BillingCycleServiceImpl serviceMock = createServicePartialMock();

    BillingCycleEntry entity = createInvalidEntity();
    ArrayList<BillingCycle> bcs = createCycleList(entity);

    when(serviceMock.getBillingCycle(anyLong())).thenReturn(bcs);

    Date usageEndDate = serviceMock.getUsageEndDate(Long.valueOf(1234567));

    verify(serviceMock).getBillingCycle(anyLong());
    assertNull(usageEndDate);
  }

  @Test
  public void testGetUsageEndDateWithCyclesSomethingFound() throws Exception {
    BillingCycleServiceImpl serviceMock = createServicePartialMock();

    BillingCycleEntry entity = createValidEntity();
    ArrayList<BillingCycle> bcs = createCycleList(entity);

    when(serviceMock.getBillingCycle(anyLong())).thenReturn(bcs);

    Date usageEndDate = serviceMock.getUsageEndDate(Long.valueOf(1234567));

    verify(serviceMock).getBillingCycle(anyLong());
    assertTrue(endDate.equals(usageEndDate));
  }

  private ArrayList<BillingCycle> createCycleList(BillingCycleEntry entity) {
    ArrayList<BillingCycle> bcs = new ArrayList<BillingCycle>();
    BillingCycle cycle = new BillingCycle();
    cycle.setEntries(Arrays.asList(entity));
    bcs.add(cycle);
    return bcs;
  }

  private BillingCycleEntry createInvalidEntity() {
    BillingCycleEntry entity = new BillingCycleEntry();
    entity.setStep("non-existent-step");
    entity.setFrom(endDate);
    return entity;
  }

  private BillingCycleEntry createValidEntity() {
    BillingCycleEntry entity = new BillingCycleEntry();
    entity.setStep("Usage End-Date");
    entity.setFrom(endDate);
    return entity;
  }

  private BillingCycleServiceImpl createServicePartialMock() throws Exception {
    BillingCycleServiceImpl mock = mock(BillingCycleServiceImpl.class);
    when(mock.getUsageEndDate(anyLong())).thenCallRealMethod();

    return mock;
  }

  private BillingCycleServiceImpl createService(BillingCycleDao daoMock, KumsAccountService accountServiceMock) {
    BillingCycleServiceImpl service = new BillingCycleServiceImpl();
    service.setBillingCycleDao(daoMock);
    service.setKumsAccountService(accountServiceMock);
    return service;
  }

}
