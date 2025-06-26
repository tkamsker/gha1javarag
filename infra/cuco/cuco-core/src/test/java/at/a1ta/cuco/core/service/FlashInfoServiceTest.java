package at.a1ta.cuco.core.service;

import static org.mockito.Matchers.any;
import static org.mockito.Matchers.anyLong;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.Collection;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Matchers;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.core.shared.dto.security.Role;
import at.a1ta.cuco.core.dao.db.impl.FlashInfoDaoImpl;
import at.a1ta.cuco.core.service.impl.FlashInfoServiceImpl;
import at.a1ta.cuco.core.shared.dto.CustomerBlock;
import at.a1ta.cuco.core.shared.dto.FlashInfo;
import at.a1ta.cuco.core.shared.dto.Tupel;

@RunWith(MockitoJUnitRunner.class)
public class FlashInfoServiceTest {

  private FlashInfoServiceImpl service = new FlashInfoServiceImpl();
  @Mock
  private FlashInfoDaoImpl flashInfoDao;
  @Mock
  private CustomerBlockService customerBlockService;

  @Before
  public void setUp() {
    service.setFlashInfoDao(flashInfoDao);
    service.setCustomerBlockService(customerBlockService);
  }

  @SuppressWarnings("unchecked")
  @Test
  public void createNew() {
    FlashInfo flash = new FlashInfo();
    flash.setRoles(generateRoleList("1", "2", "3", "4"));
    ArrayList<CustomerBlock> blocks = generateCustomerBlocks(1, 2);
    blocks.get(0).setData("1;2;3");
    blocks.get(1).setData("4;5;6");
    flash.setCustomerBlocks(blocks);

    service.saveFlashInfo(flash);
    verify(flashInfoDao, times(1)).insertFlashInfo(flash);
    verify(flashInfoDao, times(4)).insertFlashRole(anyLong(), Matchers.anyString());
    verify(flashInfoDao, times(1)).insertFlashCustomer((Collection<Tupel<Long, Long>>) any());
    verify(customerBlockService, times(2)).insertCustomerBlock((CustomerBlock) any());
  }

  @SuppressWarnings("unchecked")
  @Test
  public void createNewBlocksWithSameCustomers() {
    FlashInfo flash = new FlashInfo();
    flash.setRoles(generateRoleList("1"));
    ArrayList<CustomerBlock> blocks = generateCustomerBlocks(1, 2);
    blocks.get(0).setData("1;2;3");
    blocks.get(1).setData("2;3;6");
    flash.setCustomerBlocks(blocks);

    service.saveFlashInfo(flash);
    verify(flashInfoDao, times(1)).insertFlashInfo(flash);
    verify(flashInfoDao, times(1)).insertFlashCustomer((Collection<Tupel<Long, Long>>) any());
    verify(customerBlockService, times(2)).insertCustomerBlock((CustomerBlock) any());
  }

  @SuppressWarnings("unchecked")
  @Test
  public void updateNoNewBlocks() {
    FlashInfo flash = new FlashInfo();
    flash.setId(1);
    flash.setRoles(generateRoleList("1", "2", "3", "4"));
    ArrayList<CustomerBlock> blocks = generateCustomerBlocks(1, 2);
    blocks.get(0).setData("1;2;3");
    blocks.get(1).setData("4;5;6");
    flash.setCustomerBlocks(blocks);

    when(customerBlockService.getCustomerBlocksForFlashInfo(1)).thenReturn(blocks);

    service.saveFlashInfo(flash);
    verify(flashInfoDao, times(1)).updateFlashInfo(flash);
    verify(flashInfoDao, times(4)).insertFlashRole(anyLong(), Matchers.anyString());
    verify(flashInfoDao, times(1)).insertFlashCustomer((Collection<Tupel<Long, Long>>) any());
    verify(customerBlockService, times(2)).updateCustomerBlock((CustomerBlock) any());
  }

  @Test
  public void updateOneNewBlock() {
    FlashInfo flash = new FlashInfo();
    flash.setId(1);
    flash.setRoles(generateRoleList("1"));
    ArrayList<CustomerBlock> blocks = generateCustomerBlocks(1, 2);
    blocks.add(new CustomerBlock());
    flash.setCustomerBlocks(blocks);

    when(customerBlockService.getCustomerBlocksForFlashInfo(1)).thenReturn(generateCustomerBlocks(1, 2));

    service.saveFlashInfo(flash);
    verify(flashInfoDao, times(1)).updateFlashInfo(flash);
    verify(customerBlockService, times(2)).updateCustomerBlock((CustomerBlock) any());
    verify(customerBlockService, times(1)).insertCustomerBlock((CustomerBlock) any());
  }

  @Test
  public void updateOneBlockToDelete() {
    FlashInfo flash = new FlashInfo();
    flash.setId(1);
    flash.setRoles(generateRoleList("1"));
    ArrayList<CustomerBlock> blocks = generateCustomerBlocks(1, 2);
    flash.setCustomerBlocks(blocks);

    when(customerBlockService.getCustomerBlocksForFlashInfo(1)).thenReturn(generateCustomerBlocks(1, 2, 3));

    service.saveFlashInfo(flash);
    verify(flashInfoDao, times(1)).updateFlashInfo(flash);
    verify(customerBlockService, times(2)).updateCustomerBlock((CustomerBlock) any());
    verify(customerBlockService, times(1)).deleteCustomerBlock(3);
  }

  private ArrayList<Role> generateRoleList(String... roleNames) {
    ArrayList<Role> roles = new ArrayList<Role>();
    for (String name : roleNames) {
      Role role = new Role();
      role.setName(name);
      roles.add(role);
    }
    return roles;
  }

  private ArrayList<CustomerBlock> generateCustomerBlocks(long... ids) {
    ArrayList<CustomerBlock> blocks = new ArrayList<CustomerBlock>();
    for (long id : ids) {
      CustomerBlock block = new CustomerBlock();
      block.setId(id);
      blocks.add(block);
    }
    return blocks;
  }
}
