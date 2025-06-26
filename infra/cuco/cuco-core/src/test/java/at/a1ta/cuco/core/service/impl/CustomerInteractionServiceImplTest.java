package at.a1ta.cuco.core.service.impl;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import org.apache.commons.lang.time.DateUtils;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.data.clarify.dao.ClarifyInteractionAndWorkflowDao;
import at.a1ta.bite.data.clarify.shared.dto.ClarifyCustomerInteractionResponse;
import at.a1ta.bite.data.clarify.shared.dto.CustomerInteraction;
import at.a1ta.cuco.core.dao.db.MKInteractionDao;

@RunWith(MockitoJUnitRunner.class)
public class CustomerInteractionServiceImplTest {

  CustomerInteractionServiceImpl serviceSpy;

  @Mock
  private ClarifyInteractionAndWorkflowDao clarifyDaoMock;
  @Mock
  private MKInteractionDao mkInteractionDaoMock;

  @Before
  public void setUp() {
    CustomerInteractionServiceImpl service = new CustomerInteractionServiceImpl();
    service.setClarifyInteractionAndWorkflowDao(clarifyDaoMock);
    service.setMkInteractionDao(mkInteractionDaoMock);

    Date middle = new Date();
    Date later = DateUtils.addHours(middle, 5);
    Date earlier = DateUtils.addHours(middle, -5);

    List<CustomerInteraction> interactions = new ArrayList<CustomerInteraction>();
    addInteraction(later, "order_3", interactions);
    addInteraction(earlier, "order_1", interactions);
    Mockito.when(mkInteractionDaoMock.listMKInteractions(Matchers.anyLong())).thenReturn(interactions);

    ClarifyCustomerInteractionResponse response = new ClarifyCustomerInteractionResponse();
    ArrayList<CustomerInteraction> respInteractions = new ArrayList<CustomerInteraction>();
    addInteraction(null, "order_null", respInteractions);
    addInteraction(middle, "order_2", respInteractions);
    response.setInteractions(respInteractions);
    Mockito.when(clarifyDaoMock.getClarifyInteractionsViaSite(Matchers.anyLong(), Matchers.anyString())).thenReturn(response);

    serviceSpy = Mockito.spy(service);
  }

  private void addInteraction(Date startDate, String orderIdString, List<CustomerInteraction> interactionList) {
    CustomerInteraction inter1 = new CustomerInteraction();
    inter1.setStartDate(startDate);
    inter1.setOrderId(orderIdString);
    interactionList.add(inter1);
  }

  @Test
  public void testListAllInteractionsNoInteractions() {
    // siteId starts with "MK", no call of listInteractions(...)
    // addMKInteractions = false, no call of listMKInteractions(...)
    serviceSpy.listAllInteractions(123, "MK_testSiteId", false);

    Mockito.verify(serviceSpy, Mockito.never()).listInteractions(Matchers.anyLong(), Matchers.anyString());
    Mockito.verify(clarifyDaoMock, Mockito.never()).getClarifyInteractions(Matchers.anyLong(), Matchers.anyString());

    Mockito.verify(serviceSpy, Mockito.never()).listMKInteractions(Matchers.anyLong());
    Mockito.verify(mkInteractionDaoMock, Mockito.never()).listMKInteractions(Matchers.anyLong());
  }

  @Test
  public void testListAllInteractionsIsCalled() {
    serviceSpy.listAllInteractions(123, "testSiteId", true);

    Mockito.verify(serviceSpy).listInteractions(Matchers.anyLong(), Matchers.anyString());
    Mockito.verify(clarifyDaoMock).getClarifyInteractionsViaSite(Matchers.anyLong(), Matchers.anyString());

    Mockito.verify(serviceSpy).listMKInteractions(Matchers.anyLong());
    Mockito.verify(mkInteractionDaoMock).listMKInteractions(Matchers.anyLong());
  }

  @Test
  public void testListAllInteractionsCheckSorting() {
    List<CustomerInteraction> actionList = serviceSpy.listAllInteractions(123, "testSiteId", true);

    assertNotNull(actionList);
    assertEquals(4, actionList.size());

    assertEquals("order_3", actionList.get(0).getOrderId());
    assertEquals("order_2", actionList.get(1).getOrderId());
    assertEquals("order_1", actionList.get(2).getOrderId());
    assertEquals("order_null", actionList.get(3).getOrderId());
  }

}
