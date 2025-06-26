package at.a1ta.cuco.core.service;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import at.a1ta.cuco.core.dao.esb.CustomerAssignmentDao;
import at.a1ta.cuco.core.service.impl.CustomerAssignmentService;
import at.a1ta.cuco.core.shared.dto.ContractOwnerAssignment;

public class CustomerAssignmentServiceTest {

  private CustomerAssignmentService customerAssignmentService;
  private CustomerAssignmentDao customerAssignmentDao;

  @Before
  public void setup() {
    customerAssignmentService = new CustomerAssignmentService();
    customerAssignmentDao = mock(CustomerAssignmentDao.class);
  }

  @Test
  public void testGetParty() {
    customerAssignmentService.setCustomerAssignmentDao(customerAssignmentDao);
    ContractOwnerAssignment contractOwnerAssignment1 = mock(ContractOwnerAssignment.class);
    when(contractOwnerAssignment1.getPartyId()).thenReturn("123456");
    when(customerAssignmentDao.getContractOwnerAssignmentByBan("278900796")).thenReturn(contractOwnerAssignment1);
    ContractOwnerAssignment contractOwnerAssignment2 = customerAssignmentService.getContractOwnerAssignmentByBan("278900796");
    Assert.assertNotNull(contractOwnerAssignment2);
    Assert.assertEquals("123456", contractOwnerAssignment2.getPartyId());
  }

}
