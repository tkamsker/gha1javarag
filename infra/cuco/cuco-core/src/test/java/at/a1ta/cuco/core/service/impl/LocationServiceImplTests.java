/*
 * Copyright 2009 - 2013 by A1 Telekom Austria AG
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

import java.util.Collections;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;

import at.a1ta.bite.data.clarify.dao.ClarifyInteractionAndWorkflowDao;
import at.a1ta.bite.data.clarify.shared.dto.Location;

@RunWith(MockitoJUnitRunner.class)
public class LocationServiceImplTests {

  @Mock
  private ClarifyInteractionAndWorkflowDao clarifyInteractionAndWorkflowDaoMock;

  private LocationServiceImpl locationService;

  @Before
  public void setUp() {
    locationService = new LocationServiceImpl();
    locationService.setClarifyInteractionAndWorkflowDao(clarifyInteractionAndWorkflowDaoMock);
  }

  @Test
  public void testGetClarifyLocationsForCustomer() {
    Page<Location> page = new PageImpl<Location>(Collections.<Location> emptyList());
    Mockito.when(clarifyInteractionAndWorkflowDaoMock.findLocationsByCustomerId(Matchers.anyLong(), Matchers.any(Pageable.class))).thenReturn(page);

    ArgumentCaptor<Pageable> captor = ArgumentCaptor.forClass(Pageable.class);
    locationService.getClarifyLocationsForCustmomer(100100100L, new PageRequest(0, 100));

    Mockito.verify(clarifyInteractionAndWorkflowDaoMock, Mockito.times(1)).findLocationsByCustomerId(Matchers.eq(100100100L), captor.capture());
    Assert.assertEquals(0, captor.getValue().getPageNumber());
    Assert.assertEquals(100, captor.getValue().getPageSize());
  }

  @Test
  public void testGetClarifyLocationsForCustomerWithNullPageable() {
    Page<Location> page = new PageImpl<Location>(Collections.<Location> emptyList());
    Mockito.when(clarifyInteractionAndWorkflowDaoMock.findLocationsByCustomerId(Matchers.anyLong(), Matchers.any(Pageable.class))).thenReturn(page);

    ArgumentCaptor<Pageable> captor = ArgumentCaptor.forClass(Pageable.class);
    locationService.getClarifyLocationsForCustmomer(100100100L, null);

    Mockito.verify(clarifyInteractionAndWorkflowDaoMock, Mockito.times(1)).findLocationsByCustomerId(Matchers.eq(100100100L), captor.capture());
    Assert.assertEquals(0, captor.getValue().getPageNumber());
    Assert.assertEquals(10, captor.getValue().getPageSize());
  }

  @Test(expected = IllegalArgumentException.class)
  public void testGetClarifyLocationsForCustomerWithNullCustomerId() {
    locationService.getClarifyLocationsForCustmomer(null, new PageRequest(0, 100));
  }

}
