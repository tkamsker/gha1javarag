/*
 * Copyright 2009 - 2012 by A1 Telekom Austria AG
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
package at.a1ta.cuco.core.dao.db;

import java.util.List;
import java.util.Set;

import at.a1ta.cuco.core.shared.dto.InventoryProductGroup;
import at.a1ta.cuco.core.shared.dto.InventoryProductGroupAssignation;
import at.a1ta.cuco.core.shared.dto.InventoryProductGroupUsage;
import at.a1ta.cuco.core.shared.dto.Product;
import at.a1ta.cuco.core.shared.dto.ProductLevel;

public interface InventoryProductGroupDao {

  InventoryProductGroup getInventoryProductGroup(Long id);

  List<InventoryProductGroup> getAllInventoryProductGroups();

  void insertInventoryProductGroup(InventoryProductGroup inventoryProductGroup);

  void updateInventoryProductGroup(InventoryProductGroup inventoryProductGroup);

  int deleteInventoryProductGroup(InventoryProductGroup inventoryProductGroup);

  void addProductToInventoryProductGroup(String productId, Long inventoryProductGroupId);

  void addLevelToInventoryProductGroup(Long levelId, Long inventoryProductGroupId);

  void removeProductFromInventoryProductGroup(String productId, Long inventoryProductGroupId);

  void removeLevelFromInventoryProductGroup(Long levelId, Long inventoryProductGroupId);

  List<Product> getProductsForInventoryProductGroup(Long inventoryProductGroupId);

  List<ProductLevel> getProductLevelsForInventoryProductGroup(Long inventoryProductGroupId);

  void moveInventoryProductGroupUp(InventoryProductGroup inventoryProductGroup);

  void moveInventoryProductGroupDown(InventoryProductGroup inventoryProductGroup);

  List<InventoryProductGroupAssignation> getInventoryProductGroupAssignations();

  List<InventoryProductGroupUsage> getInventoryProductGroupUsagesByPartyId(Long partyId);

  Set<String> getAnbSsaProductIds();

}
