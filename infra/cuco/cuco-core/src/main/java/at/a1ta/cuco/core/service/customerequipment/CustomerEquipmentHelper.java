package at.a1ta.cuco.core.service.customerequipment;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

import org.apache.commons.lang.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.customerequipment.Equipment;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentAttribute;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentConsignee;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentSum;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentTree;
import at.telekom.eai.businesscustomerequipment.xsd.EquipmentItem;
import at.telekom.eai.businesscustomerequipment.xsd.EquipmentResponse;
import at.telekom.eai.businesscustomerequipment.xsd.Merkmaltem;

@Service
public class CustomerEquipmentHelper {

  private static final Logger logger = LoggerFactory.getLogger(CustomerEquipmentHelper.class);

  @Autowired
  private CustomerEquipmentTranslator translator;

  public EquipmentTree buildEquipmentTree(final EquipmentResponse response, final Party party, final EquipmentConsignee equipmentConsignee) {
    final Map<String, ArrayList<EquipmentAttribute>> equipmentIdAttributesMap = buildEquipmentIdAttributesMap(response.getMerkmaltemArray());

    final ArrayList<Equipment> equipments = translator.convertToEquipmentBeans(response.getEquipmentItemArray(), equipmentIdAttributesMap);
    Collections.sort(equipments);

    final Map<String, Equipment> equipmentIdEquipmentMap = buildEquipmentIdMap(equipments);

    final EquipmentTree data = new EquipmentTree();
    buildEquipmentTree(data, equipments, equipmentIdEquipmentMap);

    data.setEquipmentConsignee(equipmentConsignee);
    data.setEquipmentSums(getEquipmentSums(response));
    data.setMaterialSum(calculateMaterialSum(data));
    data.setParty(party);
    return data;
  }

  private long calculateMaterialSum(EquipmentTree data) {
    long allCount = 0;
    for (EquipmentSum sum : data.getEquipmentSums()) {
      allCount += sum.getCount();
    }
    return allCount;
  }

  public static String cleanEquipmentNumber(String equipmentNumber) {
    return StringUtils.stripStart(equipmentNumber, "0");
  }

  private Map<String, ArrayList<EquipmentAttribute>> buildEquipmentIdAttributesMap(final Merkmaltem[] merkmalItems) {
    final Map<String, ArrayList<EquipmentAttribute>> equipmentIdAttributesMap = new HashMap<String, ArrayList<EquipmentAttribute>>(
        merkmalItems.length * 2);

    for (final Merkmaltem merkmalItem : merkmalItems) {
      final String equipmentId = cleanEquipmentNumber(merkmalItem.getEquipmentnummer());

      ArrayList<EquipmentAttribute> attributes = equipmentIdAttributesMap.get(equipmentId);
      if (attributes == null) {
        attributes = new ArrayList<EquipmentAttribute>();
        equipmentIdAttributesMap.put(equipmentId, attributes);
      }

      attributes.add(new EquipmentAttribute(equipmentId, merkmalItem.getMerkmalsname(), merkmalItem.getMerkmalswert()));
      Collections.sort(attributes);
    }

    return equipmentIdAttributesMap;
  }

  private void buildEquipmentTree(final EquipmentTree rootEquipment, final ArrayList<Equipment> equipments,
      final Map<String, Equipment> equipmentIdEquipmentMap) {
    for (final Equipment equipment : equipments) {
      if (equipment.isTopLevel()) {
        linkChildToParentEquipment(equipment, rootEquipment);
      } else {
        final String parentId = equipment.getParentId();
        final Equipment parent = equipmentIdEquipmentMap.get(parentId);

        if (parent != null) {
          linkChildToParentEquipment(equipment, parent);
        } else {
          logger.warn("Customer Business Equipment with ID '" + equipment.getId() + "' referes a none existing parent equipment with ID '"
              + parentId + "'");
        }
      }
    }
  }

  private void linkChildToParentEquipment(final Equipment child, final Equipment parent) {
    parent.addChild(child);
    child.setParent(parent);
  }

  private ArrayList<EquipmentSum> getEquipmentSums(final EquipmentResponse response) {
    final Map<String, EquipmentSum> equipmentSums = new HashMap<String, EquipmentSum>();

    for (final EquipmentItem item : response.getEquipmentItemArray()) {
      final String materialId = item.getMaterialnummer();
      final String materialTitle = item.getMaterialbezeichnung();

      EquipmentSum material = equipmentSums.get(materialId);
      if (material == null) {
        // not existing yet
        material = new EquipmentSum(materialId, materialTitle, 0);
        equipmentSums.put(materialId, material);
      }
      material.incrementCount();
    }

    final ArrayList<EquipmentSum> lst = new ArrayList<EquipmentSum>(equipmentSums.values());
    Collections.sort(lst);
    return lst;
  }

  private Map<String, Equipment> buildEquipmentIdMap(final ArrayList<Equipment> equipments) {
    final Map<String, Equipment> equipmentsMap = new LinkedHashMap<String, Equipment>();
    for (final Equipment equipment : equipments) {
      if (equipment.hasEquipmentId()) {
        equipmentsMap.put(equipment.getId(), equipment);
      }
    }
    return equipmentsMap;
  }
}
