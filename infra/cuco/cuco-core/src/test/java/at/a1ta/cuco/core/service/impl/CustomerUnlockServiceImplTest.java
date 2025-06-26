/*
 * Copyright 2009 - 2012 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.UserInfo;
import at.a1ta.cuco.core.dao.db.CustomerUnlockRequestDao;
import at.a1ta.cuco.core.service.CuscoUnlockService;
import at.a1ta.cuco.core.shared.dto.Customer;
import at.a1ta.cuco.core.shared.dto.access.ContextAwareCustomerUnlockRequest;
import at.a1ta.cuco.core.shared.dto.access.UnlockStateEnum;

@RunWith(MockitoJUnitRunner.class)
public class CustomerUnlockServiceImplTest {

  @Mock
  private CustomerUnlockRequestDao unlockDaoMock;

  @Mock
  private CuscoUnlockService cuscoUnlockService;

  private CustomerUnlockServiceImpl unlockService;

  @Before
  public void setUp() {
    unlockService = new CustomerUnlockServiceImpl();
    unlockService.setCuscoUnlockService(cuscoUnlockService);
    unlockService.setUnlockDao(unlockDaoMock);
  }

  @Test(expected = IllegalArgumentException.class)
  public void testCheckIfUnlockedNullCusomer() {
    unlockService.checkIfUnlockded(null, new UserInfo(), "session-id", "job-id");
  }

  @Test(expected = IllegalArgumentException.class)
  public void testCheckIfUnlockedNullUser() {
    unlockService.checkIfUnlockded(new Customer(), null, "session-id", "job-id");
  }

  @Test(expected = IllegalArgumentException.class)
  public void testCheckIfUnlockedNullJob() {
    unlockService.checkIfUnlockded(new Customer(), new UserInfo(), "session-id", null);
  }

  @Test
  public void testCheckIfUnlockedDaoRetunsNull() {
    Assert.assertFalse(unlockService.checkIfUnlockded(new Customer(), new UserInfo(), "session-id", "job-id"));
  }

  @Test
  public void testCheckIfUnlockedRequestPending() {
    ContextAwareCustomerUnlockRequest result = createFor(0, 12, "session");
    result.setState(UnlockStateEnum.PENDING);
    Mockito.when(unlockDaoMock.findByCustomerIdAndUsernameAndJobIdAndSessionKey(Matchers.anyLong(), (BiteUser) Matchers.anyObject(), Matchers.anyString(), Matchers.anyString())).thenReturn(result);

    Assert.assertFalse(unlockService.checkIfUnlockded(new Customer(), new UserInfo(), "session-id", "job-id"));
    Mockito.verify(unlockDaoMock, Mockito.times(1)).findByCustomerIdAndUsernameAndJobIdAndSessionKey(Matchers.eq(0L), (BiteUser) Matchers.anyObject(), Matchers.eq("job-id"),
        Matchers.eq("session-id"));
  }

  @Test
  public void testCheckIfUnlockedRequestFinishedWithError() {
    ContextAwareCustomerUnlockRequest result = createFor(0, 12, "session");
    result.setState(UnlockStateEnum.FINISHED_ERROR);
    Mockito.when(unlockDaoMock.findByCustomerIdAndUsernameAndJobIdAndSessionKey(Matchers.anyLong(), (BiteUser) Matchers.anyObject(), Matchers.anyString(), Matchers.anyString())).thenReturn(result);

    Assert.assertFalse(unlockService.checkIfUnlockded(new Customer(), new UserInfo(), "session-id", "job-id"));
    Mockito.verify(unlockDaoMock, Mockito.times(1)).findByCustomerIdAndUsernameAndJobIdAndSessionKey(Matchers.eq(0L), (BiteUser) Matchers.anyObject(), Matchers.eq("job-id"),
        Matchers.eq("session-id"));
  }

  @Test
  public void testCheckIfUnlockedRequestFinishedLocked() {
    ContextAwareCustomerUnlockRequest result = createFor(0, 12, "session");
    result.setState(UnlockStateEnum.FINISHED_LOCKED);
    Mockito.when(unlockDaoMock.findByCustomerIdAndUsernameAndJobIdAndSessionKey(Matchers.anyLong(), (BiteUser) Matchers.anyObject(), Matchers.anyString(), Matchers.anyString())).thenReturn(result);

    Assert.assertFalse(unlockService.checkIfUnlockded(new Customer(), new UserInfo(), "session-id", "job-id"));
    Mockito.verify(unlockDaoMock, Mockito.times(1)).findByCustomerIdAndUsernameAndJobIdAndSessionKey(Matchers.eq(0L), (BiteUser) Matchers.anyObject(), Matchers.eq("job-id"),
        Matchers.eq("session-id"));
  }

  @Test
  public void testCheckIfUnlockedRequestFinishedUnlocked() {
    ContextAwareCustomerUnlockRequest result = createFor(0, 12, "session");
    result.setState(UnlockStateEnum.FINISHED_UNLOCKED);
    Mockito.when(unlockDaoMock.findByCustomerIdAndUsernameAndJobIdAndSessionKey(Matchers.anyLong(), (BiteUser) Matchers.anyObject(), Matchers.anyString(), Matchers.anyString())).thenReturn(result);

    Assert.assertTrue(unlockService.checkIfUnlockded(new Customer(), new UserInfo(), "session-id", "job-id"));
    Mockito.verify(unlockDaoMock, Mockito.times(1)).findByCustomerIdAndUsernameAndJobIdAndSessionKey(Matchers.eq(0L), (BiteUser) Matchers.anyObject(), Matchers.eq("job-id"),
        Matchers.eq("session-id"));
  }

  @Test
  public void testCheckIfUnlockedForSessionTrue() {
    ContextAwareCustomerUnlockRequest bean = createFor(0, 12, "session");
    bean.setState(UnlockStateEnum.FINISHED_UNLOCKED);
    ArrayList<ContextAwareCustomerUnlockRequest> result = new ArrayList<ContextAwareCustomerUnlockRequest>();
    result.add(bean);

    Mockito.when(unlockDaoMock.findByCustomerIdAndUsernameAndContextKey(Matchers.anyLong(), (BiteUser) Matchers.anyObject(), Matchers.anyString())).thenReturn(result);

    Assert.assertTrue(unlockService.checkIfUnlockedForSession(new Customer(), new UserInfo(), "session-id"));
  }

  @Test
  public void testCheckIfUnlockedForSessionFalse() {
    ContextAwareCustomerUnlockRequest bean = createFor(0, 12, "session");
    bean.setState(UnlockStateEnum.FINISHED_LOCKED);
    ArrayList<ContextAwareCustomerUnlockRequest> result = new ArrayList<ContextAwareCustomerUnlockRequest>();
    result.add(bean);

    Mockito.when(unlockDaoMock.findByCustomerIdAndUsernameAndContextKey(Matchers.anyLong(), (BiteUser) Matchers.anyObject(), Matchers.anyString())).thenReturn(result);

    Assert.assertFalse(unlockService.checkIfUnlockedForSession(new Customer(), new UserInfo(), "session-id"));
  }

  @Test
  public void testCheckIfUnlockedForSessionMultiResult() {
    ContextAwareCustomerUnlockRequest locked = createFor(0, 12, "session");
    locked.setState(UnlockStateEnum.FINISHED_LOCKED);
    ContextAwareCustomerUnlockRequest unlocked = createFor(0, 12, "session");
    unlocked.setState(UnlockStateEnum.FINISHED_UNLOCKED);

    ArrayList<ContextAwareCustomerUnlockRequest> result = new ArrayList<ContextAwareCustomerUnlockRequest>();
    result.add(locked);
    result.add(unlocked);

    Mockito.when(unlockDaoMock.findByCustomerIdAndUsernameAndContextKey(Matchers.anyLong(), (BiteUser) Matchers.anyObject(), Matchers.anyString())).thenReturn(result);

    Assert.assertTrue(unlockService.checkIfUnlockedForSession(new Customer(), new UserInfo(), "session-id"));
  }

  @Test
  public void testLockOverride() {
    ContextAwareCustomerUnlockRequest locked = createFor(0, 12, "session");
    locked.setState(UnlockStateEnum.FINISHED_LOCKED);
    ArrayList<ContextAwareCustomerUnlockRequest> result = new ArrayList<ContextAwareCustomerUnlockRequest>();
    result.add(locked);

    Mockito.when(unlockDaoMock.findByCustomerIdAndUsernameAndContextKey(Matchers.anyLong(), (BiteUser) Matchers.anyObject(), Matchers.anyString())).thenReturn(result);

    unlockService.lockOverride(new Customer(), new UserInfo(), "session-id", UnlockStateEnum.FINISHED_UNLOCKED);

    ArgumentCaptor<ContextAwareCustomerUnlockRequest> captor = ArgumentCaptor.forClass(ContextAwareCustomerUnlockRequest.class);
    Mockito.verify(unlockDaoMock, Mockito.times(1)).update(captor.capture());

    Assert.assertEquals(UnlockStateEnum.FINISHED_UNLOCKED, captor.getValue().getState());
    Assert.assertTrue(captor.getValue().getFinished().getTime() >= captor.getValue().getCreated().getTime());
    Assert.assertEquals(locked.getSessionKey(), captor.getValue().getSessionKey());
  }

  private ContextAwareCustomerUnlockRequest createFor(long customerId, long userId, String session) {
    ContextAwareCustomerUnlockRequest request = new ContextAwareCustomerUnlockRequest();
    request.setUser(new BiteUser());
    request.setCustomerId(customerId);
    request.getUser().setId(userId);
    request.setSessionKey(session);
    return request;
  }
}
