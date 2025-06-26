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
package at.a1ta.cuco.core.service.customerequipment;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Date;
import java.util.HashMap;
import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import at.a1ta.bite.core.server.util.ParseUtils;
import at.a1ta.cuco.core.shared.dto.customerequipment.Equipment;
import at.a1ta.cuco.core.shared.dto.customerequipment.EquipmentAttribute;
import at.a1ta.cuco.core.shared.dto.product.DefaultProductNode;
import at.a1ta.cuco.core.shared.dto.product.DefaultProductNode.ProductType;
import at.a1ta.cuco.core.shared.dto.product.MetaData;
import at.a1ta.cuco.core.shared.dto.product.MetaDataEntry;
import at.a1ta.cuco.core.shared.dto.product.MetaDataEntryType;
import at.a1telekom.cdm.common.CallNumber;
import at.a1telekom.cdm.common.TimePeriod;
import at.a1telekom.cdm.common.ValueType;
import at.a1telekom.cdm.common.ValueType.Enum;
import at.a1telekom.eai.customerinventory.PhysicalResource;
import at.a1telekom.eai.customerinventory.Product;
import at.a1telekom.eai.customerinventory.Product.ProductCharacteristicValues;
import at.a1telekom.eai.customerinventory.ProductBundle;
import at.a1telekom.eai.customerinventory.ProductCharacteristicValue;
import at.a1telekom.eai.customerinventory.ProductComponent;

public class MetaDataHelper {
  private static final Logger logger = LoggerFactory.getLogger(MetaDataHelper.class);

  private static SimpleDateFormat dateFormat = new SimpleDateFormat("dd.MM.yyyy");

  private static final HashMap<String, String> DATE_FORMAT_REGEXPS = new HashMap<String, String>() {
    {
      put("^\\d{4}-\\d{1,2}-\\d{1,2}$", "yyyy-MM-dd");
    }
  };

  private MetaDataHelper() {}

  public static String determineDateFormat(String dateString) {
    for (String regexp : DATE_FORMAT_REGEXPS.keySet()) {
      if (dateString.toLowerCase().matches(regexp)) {
        return DATE_FORMAT_REGEXPS.get(regexp);
      }
    }
    return null;
  }

  public static ArrayList<MetaDataEntry> createMetaData(Product product, List<String> blacklist) {
    ArrayList<MetaDataEntry> entries = new ArrayList<MetaDataEntry>();

    entries.add(new MetaDataEntry("getDescription", "getDescription", product.getDescription(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getProductId", "getProductId", product.getProductId(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getProductStatus", "getProductStatus", product.getProductStatus(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getStartDateTime", "Gültikeit Beginn", getDateValue(getValidForStart(product.getValidFor())), MetaDataEntryType.STRING));
    Date tempPromotionEndDate = null;
    try {

      tempPromotionEndDate = ParseUtils.parseDate(getTempProdEndDate(product.getProductCharacteristicValues()), "yyyy-MM-dd", null);
      if (getDateValue(tempPromotionEndDate) != null && getDateValue(tempPromotionEndDate).contains(("31.12.9999"))) {
        tempPromotionEndDate = null;
      }
      Date validForEnd = getValidForEnd(product.getValidFor());
      if (validForEnd != null && (getDateValue(validForEnd).contains("31.12.9999"))) {
        validForEnd = null;
      }
      if (validForEnd != null && getDateValue(tempPromotionEndDate) != null) {
        if (getDateValue(validForEnd).contains("31.12.9999") && getDateValue(tempPromotionEndDate).contains(("31.12.9999"))) {
          tempPromotionEndDate = null;
          validForEnd = null;
        }
      }
      entries.add(new MetaDataEntry("getEndDateTime", "Gültikeit Ende", ((validForEnd == null && tempPromotionEndDate == null) ? ""
          : ((validForEnd != null && tempPromotionEndDate == null) ? getDateValue(validForEnd) : (validForEnd != null ? (tempPromotionEndDate.before(validForEnd) ? getDateValue(tempPromotionEndDate)
              : getDateValue(validForEnd)) : getDateValue(tempPromotionEndDate)))), MetaDataEntryType.STRING));

    } catch (Exception ex) {
      // do nothing
      entries.add(new MetaDataEntry("getEndDateTime", "Gültikeit Ende", getDateValue(getValidForEnd(product.getValidFor())), MetaDataEntryType.STRING));
    }

    entries.add(new MetaDataEntry("getBrand", "getDescription", product.getBrand(), MetaDataEntryType.STRING));
    entries.addAll(getProductCharacteristicValuesMetaDataEntries(product.getProductCharacteristicValues(), "Blacklist", blacklist, null));
    return entries;
  }

  public static ArrayList<MetaDataEntry> createMetaData(ProductBundle product) {
    ArrayList<MetaDataEntry> entries = new ArrayList<MetaDataEntry>();

    if (product.getBundledProductOffering() != null) {
      entries.add(new MetaDataEntry("getBundledProductOfferingId", "getBundledProductOfferingId", product.getBundledProductOffering().getProductOfferingId(), MetaDataEntryType.STRING));
    }

    return entries;
  }

  public static ArrayList<MetaDataEntry> createVoiceMetaData(ProductComponent product) {
    ArrayList<MetaDataEntry> entries = new ArrayList<MetaDataEntry>();

    entries.add(new MetaDataEntry("getSimpleProductOfferingId", "getSimpleProductOfferingId", product.getSimpleProductOffering().getProductOfferingId(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getType", "getType", translateProductType(product).toString(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getCallNumber", "getCallNumber", getCallNumberValue(product.getCallNumber()), MetaDataEntryType.STRING));

    boolean geheim = false;
    if (product.getProductCharacteristicValues() != null && product.getProductCharacteristicValues().getProductCharacteristicValueArray() != null) {
      Calendar now = Calendar.getInstance();
      for (ProductCharacteristicValue productCharacteristicValues : product.getProductCharacteristicValues().getProductCharacteristicValueArray()) {
        if (productCharacteristicValues != null && "Geheimnummer".equals(productCharacteristicValues.getValue())) {
          TimePeriod validFor = productCharacteristicValues.getValidFor();
          if ((validFor.getStartDateTime() == null || validFor.getStartDateTime().before(now)) && (validFor.getEndDateTime() == null || validFor.getEndDateTime().after(now))) {
            geheim = true;
          }
        }
      }
      entries.add(new MetaDataEntry("getUnlistedNumber", "getUnlistedNumber", getBooleanValue(geheim), MetaDataEntryType.BOOLEAN));
    }

    return entries;
  }

  @SuppressWarnings("unchecked")
  private final static List<String> mobileTypes = Arrays.asList(new String[] {"663", "664", "650", "660", "681", "699", "676"});

  private static ProductType translateProductType(Product voiceProduct) {
    String ndc = voiceProduct.getCallNumber().getNDC();
    if (mobileTypes.contains(ndc)) {
      return ProductType.MOBILE;
    }
    return ProductType.FIXED;
  }

  public static ArrayList<MetaDataEntry> createMetaData(ProductComponent product) {
    ArrayList<MetaDataEntry> entries = new ArrayList<MetaDataEntry>();

    if (product.getSimpleProductOffering() != null) {
      entries.add(new MetaDataEntry("getSimpleProductOfferingId", "getSimpleProductOfferingId", product.getSimpleProductOffering().getProductOfferingId(), MetaDataEntryType.STRING));
    }

    return entries;
  }

  public static ArrayList<MetaDataEntry> createMetaData(PhysicalResource res) {
    ArrayList<MetaDataEntry> entries = new ArrayList<MetaDataEntry>();

    entries.add(new MetaDataEntry("getFirmwareVersion", "getFirmwareVersion", res.getFirmwareVersion(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getInstallationDate", "getInstallationDate", getDateValue(res.getInstallationDate()), MetaDataEntryType.DATE_TIME));
    entries.add(new MetaDataEntry("getSerialNumber", "getSerialNumber", res.getSerialNumber(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getVersionNumber", "getVersionNumber", res.getVersionNumber(), MetaDataEntryType.STRING));

    return entries;
  }

  public static ArrayList<MetaDataEntry> getAllProductCharecteristicsAsMetaData(Product product, DefaultProductNode productNode) {
    ArrayList<MetaDataEntry> entries = new ArrayList<MetaDataEntry>();
    if (product == null || !product.isSetProductCharacteristicValues()) {
      return entries;
    }
    for (ProductCharacteristicValue element : product.getProductCharacteristicValues().getProductCharacteristicValueArray()) {
      try {
          entries.add(new MetaDataEntry(element.getProductSpecCharacteristic().getName(), element.getProductSpecCharacteristic().getDescription(),
            (element.getProductSpecCharacteristicValue() != null ? element.getProductSpecCharacteristicValue().getValue() : "-"), MetaDataEntryType.STRING, element.getProductSpecCharacteristic()
                .getProductSpecCharacteristicId()));
        productNode.setProductCharacteristicValuesAsString(productNode.getProductCharacteristicValuesAsString() + element.getProductSpecCharacteristic().getName() + ":"
            + (element.getProductSpecCharacteristicValue() != null ? element.getProductSpecCharacteristicValue().getValue() : "-") + "\n");
      } catch (Exception e) {
        StringWriter stack = new StringWriter();
        e.printStackTrace(new PrintWriter(stack));
        logger.debug("Exception: " + stack.toString());
      }
    }
    return entries;
  }

  private static String getDateValue(Calendar cal) {
    if (cal == null) {
      return null;
    }
    return getDateValue(cal.getTime());
  }

  private static String getDateValue(Date date) {
    if (date == null) {
      return null;
    }
    return dateFormat.format(date);
  }

  private static String getBooleanValue(boolean bool) {
    return bool ? "Ja" : "Nein";
  }

  public static String getCallNumberValue(CallNumber callNumber) {
    if (callNumber == null) {
      return null;
    }
    return callNumber.getCC() + " " + callNumber.getNDC() + " " + callNumber.getSN();
  }

  public static Date getValidForStart(TimePeriod validFor) {
    if (validFor != null) {
      if (validFor.getStartDateTime() != null) {
        return validFor.getStartDateTime().getTime();
      }
    }
    return null;
  }

  public static Date getValidForEnd(TimePeriod validFor) {
    if (validFor != null) {
      if (validFor.getEndDateTime() != null) {
        return validFor.getEndDateTime().getTime();
      }
    }
    return null;
  }

  public static MetaDataEntryType translateValueType(Enum valueType) {
    int value = valueType.intValue();

    for (MetaDataEntryType type : MetaDataEntryType.values()) {
      if (type.getValue() == value) {
        return type;
      }
    }

    return MetaDataEntryType.STRING;
  }

  public static String getTempProdEndDate(ProductCharacteristicValues productCharacteristicValues) {
    if (productCharacteristicValues != null && productCharacteristicValues.getProductCharacteristicValueArray() != null) {
      for (ProductCharacteristicValue value : productCharacteristicValues.getProductCharacteristicValueArray()) {
        if (value != null && value.getProductSpecCharacteristic().getProductSpecCharacteristicId() != null
            && value.getProductSpecCharacteristic().getProductSpecCharacteristicId().equalsIgnoreCase("PSC_TEMPPROD_ENDS")) {
          return value.getValue();
        }
      }
    }
    return null;
  }

  public static ArrayList<MetaDataEntry> getProductCharacteristicValuesMetaDataEntries(ProductCharacteristicValues productCharacteristicValues, String filterMode,
      List<String> blacklistValuesForNewProductView, List<String> whitelistValuesForNewProductView) {
    if (productCharacteristicValues != null && productCharacteristicValues.getProductCharacteristicValueArray() != null) {
      ArrayList<MetaDataEntry> entries = new ArrayList<MetaDataEntry>();

      for (ProductCharacteristicValue value : productCharacteristicValues.getProductCharacteristicValueArray()) {
        if (value.getProductSpecCharacteristic().getProductSpecCharacteristicId() != null
            && value.getProductSpecCharacteristic().getProductSpecCharacteristicId().equalsIgnoreCase("PSC_TEMPPROD_ENDS")) {
          continue;
        }
        if (filterMode.equalsIgnoreCase("Blacklist") && value.getProductSpecCharacteristic() != null
            && !isBlacklisted(value.getProductSpecCharacteristic().getProductSpecCharacteristicId(), blacklistValuesForNewProductView)) {
          entries.add(createEntry(value));
        }
        if (filterMode.equalsIgnoreCase("Whitelist") && value.getProductSpecCharacteristic() != null
            && isWhitelisted(value.getProductSpecCharacteristic().getProductSpecCharacteristicId(), whitelistValuesForNewProductView)) {
          entries.add(createEntry(value));
        }
      }
      return entries;
    }

    return new ArrayList<MetaDataEntry>();
  }

  private static MetaDataEntry createEntry(ProductCharacteristicValue value) {
    MetaDataEntry entry = new MetaDataEntry();

    if (ValueType.DATE_TIME == value.getProductSpecCharacteristic().getValueType()) {
      try {
        SimpleDateFormat orig = new SimpleDateFormat(determineDateFormat(value.getValue()));
        Date date = orig.parse(value.getValue());
        entry.setValue(dateFormat.format(date));
      } catch (Exception e) {
        entry.setValue(value.getValue());
      }
    } else {
      entry.setValue(value.getValue());
    }
    entry.setValidForStart(getValidForStart(value.getValidFor()));
    entry.setValidForEnd(getValidForEnd(value.getValidFor()));

    entry.setDescription(value.getProductSpecCharacteristic().getDescription());
    entry.setName(value.getProductSpecCharacteristic().getName());
    entry.setType(translateValueType(value.getProductSpecCharacteristic().getValueType()));
    entry.setId(value.getProductSpecCharacteristic().getProductSpecCharacteristicId());
    return entry;
  }

  private static boolean isBlacklisted(String productSpecCharacteristicId, List<String> blacklist) {
    return blacklist.contains(productSpecCharacteristicId);
  }

  private static boolean isWhitelisted(String productSpecCharacteristicId, List<String> whitelist) {
    return whitelist.contains(productSpecCharacteristicId);
  }

  public static MetaData createMetaData(Equipment equipment) {
    ArrayList<MetaDataEntry> entries = new ArrayList<MetaDataEntry>();

    entries.add(new MetaDataEntry("getId", "getId", equipment.getId(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getName", "getName", equipment.getName(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getSerialNumber", "getSerialNumber", equipment.getSerialNumber(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getStatus", "getStatus", equipment.getStatus(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getWarrentyBegin", "getWarrentyBegin", getDateValue(equipment.getWarrentyBegin()), MetaDataEntryType.DATE_TIME));
    entries.add(new MetaDataEntry("getWarrentyEnd", "getWarrentyEnd", getDateValue(equipment.getWarrentyEnd()), MetaDataEntryType.DATE_TIME));
    entries.add(new MetaDataEntry("getMaterialId", "getMaterialId", equipment.getMaterialId(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getMaterialName", "getMaterialName", equipment.getMaterialName(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getEquipmentTyp", "getEquipmentTyp", equipment.getEquipmentTyp(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getTypBezeichnung", "getTypBezeichnung", equipment.getTypBezeichnung(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getEquipmentArt", "getEquipmentArt", equipment.getEquipmentArt(), MetaDataEntryType.STRING));
    entries.add(new MetaDataEntry("getArtBezeichnung", "getArtBezeichnung", equipment.getArtBezeichnung(), MetaDataEntryType.STRING));

    MetaData metaData = new MetaData();
    metaData.put(entries);
    return metaData;
  }

  public static MetaData createMetaDataEquipmentAttributes(Equipment equipment) {
    ArrayList<MetaDataEntry> entries = new ArrayList<MetaDataEntry>();

    if (equipment.hasAttributes()) {
      for (EquipmentAttribute attr : equipment.getAttributes()) {
        entries.add(new MetaDataEntry(attr.getKey(), attr.getKey(), attr.getValue(), MetaDataEntryType.STRING));
      }
    }

    MetaData metaData = new MetaData();
    metaData.put(entries);
    return metaData;
  }

}
