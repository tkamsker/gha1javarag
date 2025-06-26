package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.CustomerBlockDao;
import at.a1ta.cuco.core.shared.dto.CustomerBlock;

public class CustomerBlockDaoImpl extends AbstractDao implements CustomerBlockDao {

  @Override
  public List<CustomerBlock> getCustomerBlocksForFlashInfo(long flashInfoId) {
    return performListQuery("CustomerBlock.getForFlashInfo", flashInfoId);
  }

  @Override
  public CustomerBlock getCustomerBlockById(long customerBlockId) {
    return performObjectQuery("CustomerBlock.get", customerBlockId);
  }

  @Override
  public void insertCustomerBlock(CustomerBlock customerBlock) {
    executeInsert("CustomerBlock.insert", customerBlock);
  }

  @Override
  public void updateCustomerBlock(CustomerBlock customerBlock) {
    executeUpdate("CustomerBlock.update", customerBlock);
  }

  @Override
  public void deleteCustomerBlock(long customerBlockId) {
    executeDelete("CustomerBlock.delete", customerBlockId);
  }
}
