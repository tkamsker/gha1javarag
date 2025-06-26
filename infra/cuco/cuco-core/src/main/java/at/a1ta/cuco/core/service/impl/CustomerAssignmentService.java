package at.a1ta.cuco.core.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.esb.CustomerAssignmentDao;
import at.a1ta.cuco.core.shared.dto.ContractOwnerAssignment;

@Service
public class CustomerAssignmentService {

  private CustomerAssignmentDao customerAssignmentDao;

  public ContractOwnerAssignment getContractOwnerAssignmentByBan(String ban) {
    return customerAssignmentDao.getContractOwnerAssignmentByBan(ban);
  }

  public ContractOwnerAssignment getContractOwnerAssignmentByPartyId(String partyId) {
    return customerAssignmentDao.getContractOwnerAssignmentByPartyId(partyId);
  }

  @Autowired
  public void setCustomerAssignmentDao(CustomerAssignmentDao customerAssignmentDao) {
    this.customerAssignmentDao = customerAssignmentDao;
  }

}
