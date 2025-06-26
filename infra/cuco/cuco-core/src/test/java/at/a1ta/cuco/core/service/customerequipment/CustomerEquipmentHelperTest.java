package at.a1ta.cuco.core.service.customerequipment;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class CustomerEquipmentHelperTest {

  @Test
  public void testCleanEquipmentNumberNull() {
    assertEquals("null", null, CustomerEquipmentHelper.cleanEquipmentNumber(null));
  }

  @Test
  public void testCleanEquipmentNumberEmpty() {
    assertEquals("empty", "", CustomerEquipmentHelper.cleanEquipmentNumber(""));
  }

  @Test
  public void testCleanEquipmentNumberJustZeros() {
    assertEquals("Just zeros", "", CustomerEquipmentHelper.cleanEquipmentNumber("000"));
  }

  @Test
  public void testCleanEquipmentNumberNoZeros() {
    assertEquals("no zeros", "123", CustomerEquipmentHelper.cleanEquipmentNumber("123"));
  }

  @Test
  public void testCleanEquipmentNumberOneLeadingZeros() {
    assertEquals("one leading zeros", "123", CustomerEquipmentHelper.cleanEquipmentNumber("0123"));
  }

  @Test
  public void testCleanEquipmentNumberManyLeadingZeros() {
    assertEquals("many leading zeros", "123", CustomerEquipmentHelper.cleanEquipmentNumber("0000123"));
  }

  @Test
  public void testCleanEquipmentNumberZerosInTheMiddle() {
    assertEquals("zeroes in the middle", "10203", CustomerEquipmentHelper.cleanEquipmentNumber("000010203"));
  }

  @Test
  public void testCleanEquipmentNumberZerosAtTheEnd() {
    assertEquals("zeros at the end", "123000", CustomerEquipmentHelper.cleanEquipmentNumber("0000123000"));
  }

}
