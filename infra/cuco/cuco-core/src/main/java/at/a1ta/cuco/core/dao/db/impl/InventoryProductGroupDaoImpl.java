package at.a1ta.cuco.core.dao.db.impl;

import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.InventoryProductGroupDao;
import at.a1ta.cuco.core.shared.dto.InventoryProductGroup;
import at.a1ta.cuco.core.shared.dto.InventoryProductGroupAssignation;
import at.a1ta.cuco.core.shared.dto.InventoryProductGroupUsage;
import at.a1ta.cuco.core.shared.dto.Product;
import at.a1ta.cuco.core.shared.dto.ProductLevel;

public class InventoryProductGroupDaoImpl extends AbstractDao implements InventoryProductGroupDao {

  @Override
  public List<InventoryProductGroup> getAllInventoryProductGroups() {
    return performListQuery("InventoryProductGroup.Get");
  }

  @Override
  public InventoryProductGroup getInventoryProductGroup(Long id) {
    return performObjectQuery("InventoryProductGroup.Get", id);
  }

  @Override
  public void insertInventoryProductGroup(InventoryProductGroup inventoryProductGroup) {
    executeInsert("InventoryProductGroup.Insert", inventoryProductGroup);
  }

  @Override
  public void updateInventoryProductGroup(InventoryProductGroup inventoryProductGroup) {
    executeUpdate("InventoryProductGroup.Update", inventoryProductGroup);
  }

  @Override
  public int deleteInventoryProductGroup(InventoryProductGroup inventoryProductGroup) {
    int result = executeDelete("InventoryProductGroup.Delete", inventoryProductGroup.getId());
    executeUpdate("InventoryProductGroup.MoveUpFrom", inventoryProductGroup.getOrder());
    return result;
  }

  @Override
  public void addProductToInventoryProductGroup(String productId, Long inventoryProductGroupId) {
    Map<String, Object> map = new HashMap<String, Object>(2);
    map.put("productId", productId);
    map.put("inventoryProductGroupId", inventoryProductGroupId);
    executeInsert("InventoryProductGroup.AddProduct", map);
  }

  @Override
  public void addLevelToInventoryProductGroup(Long levelId, Long inventoryProductGroupId) {
    Map<String, Object> map = new HashMap<String, Object>(2);
    map.put("levelId", levelId);
    map.put("inventoryProductGroupId", inventoryProductGroupId);
    executeInsert("InventoryProductGroup.AddLevel", map);
  }

  @Override
  public void removeProductFromInventoryProductGroup(String productId, Long inventoryProductGroupId) {
    Map<String, Object> map = new HashMap<String, Object>(2);
    map.put("productId", productId);
    map.put("inventoryProductGroupId", inventoryProductGroupId);
    executeDelete("InventoryProductGroup.RemoveProduct", map);
  }

  @Override
  public void removeLevelFromInventoryProductGroup(Long levelId, Long inventoryProductGroupId) {
    Map<String, Object> map = new HashMap<String, Object>(2);
    map.put("levelId", levelId);
    map.put("inventoryProductGroupId", inventoryProductGroupId);
    executeDelete("InventoryProductGroup.RemoveLevel", map);
  }

  @Override
  public List<Product> getProductsForInventoryProductGroup(Long inventoryProductGroupId) {
    return performListQuery("InventoryProductGroup.GetProductsForInventoryProductGroup", inventoryProductGroupId);
  }

  @Override
  public List<ProductLevel> getProductLevelsForInventoryProductGroup(Long inventoryProductGroupId) {
    return performListQuery("InventoryProductGroup.GetProductLevelsForInventoryProductGroup", inventoryProductGroupId);
  }

  @Override
  public void moveInventoryProductGroupUp(InventoryProductGroup inventoryProductGroup) {
    executeUpdate("InventoryProductGroup.MoveUp", inventoryProductGroup.getOrder());
  }

  @Override
  public void moveInventoryProductGroupDown(InventoryProductGroup inventoryProductGroup) {
    executeUpdate("InventoryProductGroup.MoveDown", inventoryProductGroup.getOrder());
  }

  @Override
  public List<InventoryProductGroupAssignation> getInventoryProductGroupAssignations() {
    return performListQuery("InventoryProductGroup.getInventoryProductGroupAssignations");
  }

  @Override
  public List<InventoryProductGroupUsage> getInventoryProductGroupUsagesByPartyId(Long partyId) {
    return performListQuery("InventoryProductGroup.GetUsagesByPartyId", partyId);
  }

  @Override
  public Set<String> getAnbSsaProductIds() {
    Collection<String> list = performListQuery("InventoryProductGroup.GetAnbSsaProductIds", null);
    return new HashSet<String>(list);
  }
}