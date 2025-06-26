package at.a1ta.cuco.core.service.customerequipment;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import org.apache.commons.lang.StringUtils;
import org.springframework.stereotype.Service;

import at.a1ta.cuco.core.shared.dto.customerequipment.Equipment;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentAttribute;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentConsignee;
import at.telekom.eai.businesscustomerequipment.xsd.EquipmentItem;
import at.telekom.eai.businesscustomerequipment.xsd.PartnerItem;

@Service
public class CustomerEquipmentTranslator {
  private static final String EMPTY_STR = "";
  private static final String BLANK_STR = " ";
  private static final String BLANK_COMMA_STR = ", ";
  private static final String PARTNER_PREFIX = ", ID: ";

  // Equipment status encoding
  private static final String STATUS_ACTIVE = "aktiv";
  private static final String STATUS_NOT_ACTIVE = "inaktiv";
  private static final String STATUS_INAK = "inak";

  public ArrayList<EquipmentConsignee> convertToEquipmentConsigneeBeans(final long partyId, final PartnerItem[] partnerItems) {
    final ArrayList<EquipmentConsignee> lst = new ArrayList<EquipmentConsignee>(partnerItems.length);
    for (final PartnerItem item : partnerItems) {
      lst.add(convertToEquipmentConsigneeBean(partyId, item));
    }
    return lst;
  }

  private EquipmentConsignee convertToEquipmentConsigneeBean(final long partyId, final PartnerItem item) {
    final String sAnrede = StringUtils.defaultIfEmpty(item.getAnredeschlussel(), EMPTY_STR);
    final String sName1 = StringUtils.defaultIfEmpty(item.getName1(), EMPTY_STR);
    final String sName2 = StringUtils.defaultIfEmpty(item.getName2(), EMPTY_STR);
    final String sPlz = StringUtils.defaultIfEmpty(item.getPostZahl(), EMPTY_STR);
    final String sOrt = StringUtils.defaultIfEmpty(item.getOrt(), EMPTY_STR);
    final String sStrasse = StringUtils.defaultIfEmpty(item.getStrasse(), EMPTY_STR);
    final String sHausNr = StringUtils.defaultIfEmpty(item.getHausnummer(), EMPTY_STR);

    final EquipmentConsignee equipmentConsignee = new EquipmentConsignee();
    equipmentConsignee.setId(item.getWarenempfanger());
    equipmentConsignee.setSummary(sAnrede + BLANK_STR + sName1 + BLANK_STR + sName2 + BLANK_COMMA_STR + sStrasse + BLANK_STR + sHausNr + BLANK_COMMA_STR + sPlz + BLANK_STR + sOrt + PARTNER_PREFIX + item.getWarenempfanger());
    equipmentConsignee.setSummaryShort(sName1 + BLANK_STR + sName2 + BLANK_COMMA_STR + sPlz + BLANK_STR + sOrt);
    equipmentConsignee.setPartyId(partyId);

    equipmentConsignee.setTitle(item.getAnredeschlussel());
    equipmentConsignee.setName1(item.getName1());
    equipmentConsignee.setName2(item.getName2());
    equipmentConsignee.setPlz(item.getPostZahl());
    equipmentConsignee.setCity(item.getOrt());
    equipmentConsignee.setStreet(item.getStrasse());
    equipmentConsignee.setHouseNumber(item.getHausnummer());
    equipmentConsignee.setConsignee(item.getWarenempfanger());

    return equipmentConsignee;
  }

  public ArrayList<Equipment> convertToEquipmentBeans(final EquipmentItem[] equipmentItems, final Map<String, ArrayList<EquipmentAttribute>> attributesMap) {
    final ArrayList<Equipment> lst = new ArrayList<Equipment>(equipmentItems.length);
    for (final EquipmentItem item : equipmentItems) {
      lst.add(convertToEquipmentBean(item, attributesMap));
    }
    return lst;
  }

  private Date toDate(Calendar calendar) {
    return calendar == null ? null : calendar.getTime();
  }

  public Equipment convertToEquipmentBean(final EquipmentItem equipmentItem, final Map<String, ArrayList<EquipmentAttribute>> attributesMap) {
    final Equipment equipment = new Equipment();
    equipment.setId(CustomerEquipmentHelper.cleanEquipmentNumber(equipmentItem.getEquipmentnummer()));
    equipment.setName(equipmentItem.getEquipmentbezeichnung());
    equipment.setParentId(CustomerEquipmentHelper.cleanEquipmentNumber(equipmentItem.getUbergeorgnetesEquipment()));
    equipment.setAttributes(attributesMap.get(CustomerEquipmentHelper.cleanEquipmentNumber(equipmentItem.getEquipmentnummer())));
    equipment.setStatus(translateEquipmentStatus(equipmentItem.getSystemstatus()));
    equipment.setWarrentyBegin(toDate(equipmentItem.getGewahrleistungsdatumBegin()));
    equipment.setWarrentyEnd(toDate(equipmentItem.getGewahrleistungsdatumEnde()));
    equipment.setSerialNumber(equipmentItem.getSerialnummer());
    equipment.setMaterialId(equipmentItem.getMaterialnummer());
    equipment.setMaterialName(equipmentItem.getMaterialbezeichnung());

    equipment.setEquipmentTyp(equipmentItem.getEquipmenttyp());
    equipment.setTypBezeichnung(equipmentItem.getTypbezeichnung());

    equipment.setEquipmentArt(equipmentItem.getEquipmentart());
    equipment.setArtBezeichnung(equipmentItem.getArtbezeichnung());

    return equipment;
  }

  private String translateEquipmentStatus(final String systemStatus) {
    return systemStatus != null && systemStatus.toLowerCase().contains(STATUS_INAK) ? STATUS_NOT_ACTIVE : STATUS_ACTIVE;
  }

  @SuppressWarnings("unused")
  private String getConvertedEquipmentStatusExtended(final EquipmentItem e) {
    String sysStat = e.getSystemstatus(); // System status ...should always be provided
    String anwStat = e.getAnwenderstatus(); // Anwender status ...may be provided

    // get the active / not active status
    final String activeNotActiveStatus = sysStat != null && sysStat.toLowerCase().contains(STATUS_INAK) ? STATUS_NOT_ACTIVE : STATUS_ACTIVE;

    // Mapping for the system status codes
    final Map<String, String> sysStatMap = new HashMap<String, String>();
    sysStatMap.put("efre", "Equipment ist frei zu Verfügung");
    sysStatMap.put("eheq", "Equipment ist in ein übergeordnetes Equipment eingebaut");
    sysStatMap.put("elag", "Equipment liegt auf Lager");
    sysStatMap.put("elie", "Equipment ist einem Lieferschein zugeordnet");

    // Mapping for the anwender status codes
    final Map<String, String> anwStatMap = new HashMap<String, String>();
    anwStatMap.put("abg", "abgebaut");
    anwStatMap.put("fehl", "Eingabefehler");
    anwStatMap.put("gek", "gekündigt");
    anwStatMap.put("ues", "übersiedelt");

    // get other system stati
    final List<String> sysLst = new ArrayList<String>();
    if (sysStat != null) {
      sysStat = sysStat.toLowerCase();

      final Set<String> sysStatKeys = sysStatMap.keySet();
      for (final String key : sysStatKeys) {
        if (sysStat.contains(key)) {
          sysLst.add(sysStatMap.get(key));
        }
      }
    }

    // get other anw stati
    final List<String> anwLst = new ArrayList<String>();
    if (anwStat != null) {
      anwStat = anwStat.toLowerCase();

      final Set<String> anwStatKeys = anwStatMap.keySet();
      for (final String key : anwStatKeys) {
        if (anwStat.contains(key)) {
          anwLst.add(anwStatMap.get(key));
        }
      }
    }

    return activeNotActiveStatus;
  }
}
