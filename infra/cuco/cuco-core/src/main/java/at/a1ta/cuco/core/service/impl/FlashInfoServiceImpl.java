package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.cuco.core.dao.db.FlashInfoDao;
import at.a1ta.cuco.core.service.CustomerBlockService;
import at.a1ta.cuco.core.service.FlashInfoService;
import at.a1ta.cuco.core.shared.dto.CustomerBlock;
import at.a1ta.cuco.core.shared.dto.FlashInfo;
import at.a1ta.cuco.core.shared.dto.Tupel;

@Service
public class FlashInfoServiceImpl implements FlashInfoService {

  private FlashInfoDao flashInfoDao;
  private CustomerBlockService customerBlockService;

  @Override
  public FlashInfo getFlashInfoById(long flashId) {
    return flashInfoDao.getFlashInfoById(flashId);
  }

  @Override
  public List<FlashInfo> getAllFlashInfos() {
    return flashInfoDao.getAllFlashInfos();
  }

  @Override
  public List<FlashInfo> getFlashInfoForUserAndCustomer(long userId, long customerId) {
    return flashInfoDao.getFlashInfoForUserAndCustomer(userId, customerId);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void saveFlashInfo(FlashInfo flashInfo) {
    setCorrectFlashInfoToBlock(flashInfo);
    if (flashInfo.getId() == -1) {
      createFlashInfo(flashInfo);
    } else {
      updateFlashInfo(flashInfo);
    }
  }

  @Override
  public void deleteFlashInfo(long flashId) {
    flashInfoDao.deleteFlashInfo(flashId);
  }

  @Override
  public void insertFlashViewed(long flashInfoId, long partyId, long userId) {
    flashInfoDao.insertFlashViewed(flashInfoId, partyId, userId);
  }

  private void createFlashInfo(FlashInfo flashInfo) {
    flashInfoDao.insertFlashInfo(flashInfo);
    insertRoles(flashInfo);
    insertFlashCustomers(flashInfo);
    insertCustomerBlocks(flashInfo);
  }

  private void setCorrectFlashInfoToBlock(FlashInfo flashInfo) {
    for (CustomerBlock block : flashInfo.getCustomerBlocks()) {
      block.setFlashInfo(flashInfo);
    }
  }

  private void insertRoles(FlashInfo flashInfo) {
    for (Role role : flashInfo.getRoles()) {
      flashInfoDao.insertFlashRole(flashInfo.getId(), role.getName());
    }
  }

  private void insertFlashCustomers(FlashInfo flashInfo) {
    long flashId = flashInfo.getId();
    HashMap<Long, Tupel<Long, Long>> toAdd = new HashMap<Long, Tupel<Long, Long>>(1000);
    for (CustomerBlock block : flashInfo.getCustomerBlocks()) {
      long count = 0;
      for (long customer : getFilteredCustomers(block)) {
        if (!toAdd.containsKey(flashId)) {
          count++;
        }
        toAdd.put(customer, new Tupel<Long, Long>(flashId, customer));
      }
      block.setCount(count);
    }

    flashInfoDao.insertFlashCustomer(toAdd.values());
  }

  private ArrayList<Long> getFilteredCustomers(CustomerBlock block) {
    if (block.getData() == null || block.getData().equals("")) {
      return new ArrayList<Long>();
    }

    String[] stringIds = block.getData().replaceAll("\r\n", "").split(";");
    ArrayList<Long> longIds = new ArrayList<Long>(stringIds.length);
    for (int i = 0; i < stringIds.length; i++) {
      try {
        longIds.add(Long.parseLong(stringIds[i]));
      } catch (NumberFormatException e) {
        // if it's not parseable, forget it
      }
    }
    return longIds;
  }

  private void insertCustomerBlocks(FlashInfo flashInfo) {
    for (CustomerBlock block : flashInfo.getCustomerBlocks()) {
      customerBlockService.insertCustomerBlock(block);
    }
  }

  private void updateFlashInfo(FlashInfo flashInfo) {
    flashInfoDao.updateFlashInfo(flashInfo);

    flashInfoDao.deleteFlashRoleForFlash(flashInfo.getId());
    insertRoles(flashInfo);

    flashInfoDao.deleteFlashCustomerForFlash(flashInfo.getId());
    insertFlashCustomers(flashInfo);
    processBlocks(flashInfo);
  }

  private void processBlocks(FlashInfo flashInfo) {
    List<CustomerBlock> toDelete = getBlocksToDelete(flashInfo);
    for (CustomerBlock block : toDelete) {
      customerBlockService.deleteCustomerBlock(block.getId());
    }

    for (CustomerBlock block : flashInfo.getCustomerBlocks()) {
      if (block.getId() == -1) {
        customerBlockService.insertCustomerBlock(block);
      } else {
        customerBlockService.updateCustomerBlock(block);
      }
    }
  }

  private List<CustomerBlock> getBlocksToDelete(FlashInfo flashInfo) {
    ArrayList<CustomerBlock> toDelete = new ArrayList<CustomerBlock>();
    for (CustomerBlock oldBlock : customerBlockService.getCustomerBlocksForFlashInfo(flashInfo.getId())) {
      if (!flashInfoContainsBlock(flashInfo, oldBlock)) {
        toDelete.add(oldBlock);
      }
    }

    return toDelete;
  }

  private boolean flashInfoContainsBlock(FlashInfo flashInfo, CustomerBlock oldBlock) {
    for (CustomerBlock block : flashInfo.getCustomerBlocks()) {
      if (block.getId() == oldBlock.getId()) {
        return true;
      }
    }
    return false;
  }

  @Autowired
  public void setFlashInfoDao(FlashInfoDao flashInfoDao) {
    this.flashInfoDao = flashInfoDao;
  }

  @Autowired
  public void setCustomerBlockService(CustomerBlockService customerBlockService) {
    this.customerBlockService = customerBlockService;
  }
}
