package at.a1ta.cuco.core.service.impl;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.apache.commons.lang3.ObjectUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import at.a1ta.cuco.core.dao.db.InventoryProductGroupDao;
import at.a1ta.cuco.core.dao.db.ProductHierarchyDao;
import at.a1ta.cuco.core.service.ProductAdminService;
import at.a1ta.cuco.core.shared.dto.InventoryProductGroup;
import at.a1ta.cuco.core.shared.dto.InventoryProductGroupAssignation;
import at.a1ta.cuco.core.shared.dto.Product;
import at.a1ta.cuco.core.shared.dto.ProductHierarchy;
import at.a1ta.cuco.core.shared.dto.ProductLevel;

@Service
public class ProductAdminServiceImpl implements ProductAdminService {

  @Autowired
  private InventoryProductGroupDao inventoryProductGroupDao;

  @Autowired
  private ProductHierarchyDao productHierarchyDao;

  @Override
  public List<InventoryProductGroup> getAllInventoryProductGroups() {
    return inventoryProductGroupDao.getAllInventoryProductGroups();
  }

  @Override
  @Transactional(value = "transactionManager")
  public void saveInventoryProductGroup(InventoryProductGroup inventoryProductGroup) {
    if (inventoryProductGroup.getId() != null) {
      inventoryProductGroupDao.updateInventoryProductGroup(inventoryProductGroup);
    } else {
      inventoryProductGroupDao.insertInventoryProductGroup(inventoryProductGroup);
    }
  }

  @Override
  @Transactional(value = "transactionManager")
  public void moveInventoryProductGroupUp(InventoryProductGroup inventoryProductGroup) {
    inventoryProductGroupDao.moveInventoryProductGroupUp(inventoryProductGroup);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void moveInventoryProductGroupDown(InventoryProductGroup inventoryProductGroup) {
    inventoryProductGroupDao.moveInventoryProductGroupDown(inventoryProductGroup);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void deleteInventoryProductGroup(InventoryProductGroup inventoryProductGroup) {
    inventoryProductGroupDao.deleteInventoryProductGroup(inventoryProductGroup);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void addProductToInventoryProductGroup(String productId, Long inventoryProductGroupId) {
    inventoryProductGroupDao.addProductToInventoryProductGroup(productId, inventoryProductGroupId);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void addLevelToInventoryProductGroup(Long levelId, Long inventoryProductGroupId) {
    inventoryProductGroupDao.addLevelToInventoryProductGroup(levelId, inventoryProductGroupId);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void removeProductFromInventoryProductGroup(String productId, Long inventoryProductGroupId) {
    inventoryProductGroupDao.removeProductFromInventoryProductGroup(productId, inventoryProductGroupId);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void removeLevelFromInventoryProductGroup(Long levelId, Long inventoryProductGroupId) {
    inventoryProductGroupDao.removeLevelFromInventoryProductGroup(levelId, inventoryProductGroupId);
  }

  @Override
  public List<Product> getProductsForInventoryProductGroup(Long inventoryProductGroupId) {
    return inventoryProductGroupDao.getProductsForInventoryProductGroup(inventoryProductGroupId);
  }

  @Override
  public List<ProductLevel> getProductLevelsForInventoryProductGroup(Long inventoryProductGroupId) {
    return inventoryProductGroupDao.getProductLevelsForInventoryProductGroup(inventoryProductGroupId);
  }

  @Override
  public List<ProductLevel> getProductTree() {
    List<ProductHierarchy> productHierarchy = productHierarchyDao.getProductHierarchy();
    List<InventoryProductGroupAssignation> inventoryProductGroupAssignations = inventoryProductGroupDao.getInventoryProductGroupAssignations();

    HashMap<String, InventoryProductGroupAssignation> assignedProducts = getAssignedProducts(inventoryProductGroupAssignations);
    HashMap<Long, InventoryProductGroupAssignation> assignedLevels = getAssignedLevels(inventoryProductGroupAssignations);
    List<ProductLevel> productTree = createProductTree(productHierarchy, assignedProducts, assignedLevels);

    return productTree;
  }

  private List<ProductLevel> createProductTree(List<ProductHierarchy> productHierarchy, HashMap<String, InventoryProductGroupAssignation> assignedProducts, HashMap<Long, InventoryProductGroupAssignation> assignedLevels) {
    Set<Long> level1Ids = new HashSet<Long>();
    List<ProductLevel> productTree = new ArrayList<ProductLevel>();
    for (ProductHierarchy item : productHierarchy) {
      if (!level1Ids.contains(item.getProductLevel1Id())) {
        ProductLevel level1 = new ProductLevel(item.getProductLevel1Id(), item.getProductLevel1Description());
        checkLevelAssignation(level1, assignedLevels);
        addLevel2(productHierarchy, level1, assignedProducts, assignedLevels);
        productTree.add(level1);
        level1Ids.add(item.getProductLevel1Id());
      }
    }
    return productTree;
  }

  private void addLevel2(List<ProductHierarchy> productHierarchy, ProductLevel level1, HashMap<String, InventoryProductGroupAssignation> assignedProducts, HashMap<Long, InventoryProductGroupAssignation> assignedLevels) {
    Set<Long> level2Ids = new HashSet<Long>();
    for (ProductHierarchy item : productHierarchy) {
      if (level1.getProductLevelId().equals(item.getProductLevel1Id())) {
        if (!level2Ids.contains(item.getProductLevel2Id())) {
          ProductLevel level2 = new ProductLevel(item.getProductLevel2Id(), item.getProductLevel2Description());
          checkLevelAssignation(level2, assignedLevels);
          addLevel3(productHierarchy, level2, assignedProducts, assignedLevels);
          level2.setParent(level1);
          level1.addSubProductLevel(level2);
          level2Ids.add(item.getProductLevel2Id());
        }
      }
    }
  }

  private void addLevel3(List<ProductHierarchy> productHierarchy, ProductLevel level2, HashMap<String, InventoryProductGroupAssignation> assignedProducts, HashMap<Long, InventoryProductGroupAssignation> assignedLevels) {
    Set<Long> level3Ids = new HashSet<Long>();
    for (ProductHierarchy item : productHierarchy) {
      if (level2.getProductLevelId().equals(item.getProductLevel2Id())) {
        if (!level3Ids.contains(item.getProductLevel3Id())) {
          ProductLevel level3 = new ProductLevel(item.getProductLevel3Id(), item.getProductLevel3Description());
          checkLevelAssignation(level3, assignedLevels);
          addLevel4(productHierarchy, level3, assignedProducts, assignedLevels);
          level3.setParent(level2);
          level2.addSubProductLevel(level3);
          level3Ids.add(item.getProductLevel3Id());
        }
      }
    }
  }

  private void addLevel4(List<ProductHierarchy> productHierarchy, ProductLevel level3, HashMap<String, InventoryProductGroupAssignation> assignedProducts, HashMap<Long, InventoryProductGroupAssignation> assignedLevels) {
    Set<Long> level4Ids = new HashSet<Long>();
    for (ProductHierarchy item : productHierarchy) {
      if (level3.getProductLevelId().equals(item.getProductLevel3Id())) {
        if (!level4Ids.contains(item.getProductLevel4Id())) {
          ProductLevel level4 = new ProductLevel(item.getProductLevel4Id(), item.getProductLevel4Description());
          checkLevelAssignation(level4, assignedLevels);
          addProducts(productHierarchy, level4, assignedProducts);
          level4.setParent(level3);
          level3.addSubProductLevel(level4);
          level4Ids.add(item.getProductLevel4Id());
        }
      }
    }
  }

  private void addProducts(List<ProductHierarchy> productHierarchy, ProductLevel level4, HashMap<String, InventoryProductGroupAssignation> assignedProducts) {
    for (ProductHierarchy item : productHierarchy) {
      if (level4.getProductLevelId().equals(item.getProductLevel4Id())) {
        String productDescription = item.getProductDescription() == null ? item.getProductId() : item.getProductDescription();

        Product product = new Product(item.getProductId(), productDescription);
        checkProductAssignation(product, assignedProducts);
        product.setParent(level4);
        level4.addProduct(product);
      }
    }
    
    Collections.sort(level4.getProducts(), new Comparator<Product>() {
      @Override
      public int compare(Product p1, Product p2) {
        return ObjectUtils.compare(p1.getDescription(), p2.getDescription());
      }
    });
  }

  private HashMap<String, InventoryProductGroupAssignation> getAssignedProducts(List<InventoryProductGroupAssignation> inventoryProductGroupAssignations) {
    HashMap<String, InventoryProductGroupAssignation> assignedProducts = new HashMap<String, InventoryProductGroupAssignation>(500);
    for (InventoryProductGroupAssignation assignment : inventoryProductGroupAssignations) {
      if (assignment.getProductId() != null) {
        assignedProducts.put(assignment.getProductId(), assignment);
      }
    }
    return assignedProducts;
  }

  private HashMap<Long, InventoryProductGroupAssignation> getAssignedLevels(List<InventoryProductGroupAssignation> inventoryProductGroupAssignations) {
    HashMap<Long, InventoryProductGroupAssignation> assignedLevels = new HashMap<Long, InventoryProductGroupAssignation>(500);
    for (InventoryProductGroupAssignation assignment : inventoryProductGroupAssignations) {
      if (assignment.getLevelId() != 0) {
        assignedLevels.put(assignment.getLevelId(), assignment);
      }
    }
    return assignedLevels;
  }

  private void checkLevelAssignation(ProductLevel level, HashMap<Long, InventoryProductGroupAssignation> assignedLevels) {
    if (assignedLevels.containsKey(level.getProductLevelId())) {
      level.setInventoryProductGroup(inventoryProductGroupDao.getInventoryProductGroup(assignedLevels.get(level.getProductLevelId()).getInventoryProductGroupId()));
    }
  }

  private void checkProductAssignation(Product product, HashMap<String, InventoryProductGroupAssignation> assignedProducts) {
    if (assignedProducts.containsKey(product.getProductId())) {
      product.setInventoryProductGroup(inventoryProductGroupDao.getInventoryProductGroup(assignedProducts.get(product.getProductId()).getInventoryProductGroupId()));
    }
  }
}
