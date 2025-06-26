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
import java.util.Date;

import org.hamcrest.Matchers;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.server.dao.PersonDao;
import at.a1ta.bite.core.shared.Strategy;
import at.a1ta.bite.core.shared.dto.BiteUser;
import at.a1ta.bite.core.shared.dto.cd.CdPerson;
import at.a1ta.bite.data.clarify.service.ClarifyInteractionService;
import at.a1ta.bite.data.clarify.shared.dto.ClarifyInteraction;
import at.a1ta.cuco.core.dao.db.PayableTicketDao;
import at.a1ta.cuco.core.dao.esb.BrianDao;
import at.a1ta.cuco.core.shared.dto.ChargingType;
import at.a1ta.cuco.core.shared.dto.PayableTicket;

@RunWith(MockitoJUnitRunner.class)
public class PayableTicketServiceImplTest {

  private static final String NT_USER = "q907291";
  private long CHARGE_TYPE_ADX = 3;
  private long CHARGE_TYPE_SIMBA = 2;

  @Mock
  private PayableTicketDao ticketDaoMock;

  @Mock
  private BrianDao brainDaoMock;

  @Mock
  private ClarifyInteractionService interactionServiceMock;

  @Mock
  private PersonDao personDaoMock;

  private PayableTicketServiceImpl ticketService;

  @Before
  public void setUp() {
    ticketService = new PayableTicketServiceImpl(Collections.<Strategy<PayableTicket>> emptyList());
    ticketService.setPayableTicketDao(ticketDaoMock);
    ticketService.setBrianDao(brainDaoMock);
    ticketService.setPersonDao(personDaoMock);
    ticketService.setInteractionService(interactionServiceMock);

    Mockito.when(personDaoMock.getPerson(org.mockito.Matchers.any(String.class))).thenReturn(new CdPerson(NT_USER));
  }

  @Test
  public void testInsertTicketSetsExportDateToNowWhenChargingTypeIsAdx() {
    Date timestamp = new Date();
    PayableTicket ticket = createDefaultTicket(CHARGE_TYPE_ADX);
    ticketService.insertTicket(ticket);

    Assert.assertThat(timestamp, Matchers.lessThanOrEqualTo(ticket.getExportedDate()));
  }

  @Test
  public void testInsertTicketDoesNotSetExportDateWhenChargingTypeIsNonAdx() {
    PayableTicket ticket = createDefaultTicket(CHARGE_TYPE_SIMBA);
    ticketService.insertTicket(ticket);

    Assert.assertNull(ticket.getExportedDate());
  }

  @Test
  public void testInsertTicketCreatesInteractionWhenTransactionSucessfullAndChargeTypeIsSimba() {
    ticketService.afterPropertiesSet();
    PayableTicket ticket = createDefaultTicket(CHARGE_TYPE_SIMBA);
    ticketService.insertTicket(ticket);

    Mockito.verify(interactionServiceMock, Mockito.times(1)).saveInteraction(org.mockito.Matchers.any(ClarifyInteraction.class));
  }

  @Test
  public void testInsertTicketDoesNotCreateInteractionWhenTransactionSucessfullAndChargeTypeIsAdx() {
    ticketService.afterPropertiesSet();
    PayableTicket ticket = createDefaultTicket(CHARGE_TYPE_ADX);
    ticketService.insertTicket(ticket);

    Mockito.verifyZeroInteractions(interactionServiceMock);
  }

  @Test
  public void testInsertTicketDoesNotCreateInteractionOnError() {
    ticketService.afterPropertiesSet();
    try {
      ticketService.insertTicket(createDefaultTicket(CHARGE_TYPE_ADX));
    } catch (Exception e) {
      // do nothing
    }
    Mockito.verifyZeroInteractions(interactionServiceMock);
  }

  private PayableTicket createDefaultTicket(long chargeType) {
    BiteUser user = new BiteUser();
    user.setUsername("username");
    user.setFirstName("asdf");
    user.setLastName("asdf");
    user.setId(120L);
    PayableTicket ticket = PayableTicket.builder().chargedAs(new ChargingType(chargeType)).createdBy(user).build();
    ticket.setClearingAccountNumber(1L);
    ticket.setCustomerId(1L);
    return ticket;
  }
}
