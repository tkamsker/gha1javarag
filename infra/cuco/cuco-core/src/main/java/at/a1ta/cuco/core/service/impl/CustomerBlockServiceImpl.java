package at.a1ta.cuco.core.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.dao.db.CustomerBlockDao;
import at.a1ta.cuco.core.service.CustomerBlockService;
import at.a1ta.cuco.core.shared.dto.CustomerBlock;

@Service
public class CustomerBlockServiceImpl implements CustomerBlockService {

  @Autowired
  private CustomerBlockDao customerBlockDao;

  @Override
  public List<CustomerBlock> getCustomerBlocksForFlashInfo(long flashInfoId) {
    return customerBlockDao.getCustomerBlocksForFlashInfo(flashInfoId);
  }

  @Override
  public CustomerBlock getCustomerBlockById(long customerBlockId) {
    return customerBlockDao.getCustomerBlockById(customerBlockId);
  }

  @Override
  public void insertCustomerBlock(CustomerBlock customerBlock) {
    customerBlockDao.insertCustomerBlock(customerBlock);
  }

  @Override
  public void updateCustomerBlock(CustomerBlock customerBlock) {
    customerBlockDao.updateCustomerBlock(customerBlock);
  }

  @Override
  public void deleteCustomerBlock(long customerBlockId) {
    customerBlockDao.deleteCustomerBlock(customerBlockId);
  }
}
