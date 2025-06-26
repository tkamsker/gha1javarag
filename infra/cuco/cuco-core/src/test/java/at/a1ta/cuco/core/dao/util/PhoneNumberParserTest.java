package at.a1ta.cuco.core.dao.util;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.util.Arrays;
import java.util.List;

import org.junit.Test;

public class PhoneNumberParserTest {

  private static final List<String> COUNTRY_CODES = Arrays.asList(new String[] {"43"});
  private static final List<String> SPECIAL_ONKZS = Arrays.asList(new String[] {"0800", "0810"});
  private static final List<String> ONKZS = Arrays.asList(new String[] {"664", "7227"});

  @Test
  public void testTrimAndClean_IllegalChararcters() {
    assertEquals("+436641234567", PhoneNumberParser.trimAndClean(" +43 (664) 1234567"));
    assertEquals("+4372721234567", PhoneNumberParser.trimAndClean(" +43 / 7272 / 12345 - 67"));
    assertEquals("004372721234567", PhoneNumberParser.trimAndClean("004372721234567"));
    assertEquals("004372721234567", PhoneNumberParser.trimAndClean("0043.7272.1234567"));
  }

  @Test
  public void testTrimAndClean_ZeroInBrackets() {
    assertEquals("004372721234567", PhoneNumberParser.trimAndClean("0043(0)7272/1234567"));
    assertEquals("004372721234567", PhoneNumberParser.trimAndClean(" 0043 ( 0 ) 7272 / 1234567 "));
  }

  @Test
  public void testSplitAfterOnkz_SpecialOnkz() {
    assertArrayEquals(new String[] {"0800", "100100"}, PhoneNumberParser.splitAfterOnkz("0800100100", ONKZS, SPECIAL_ONKZS));
    assertArrayEquals(new String[] {"0810", "100100"}, PhoneNumberParser.splitAfterOnkz("0810100100", ONKZS, SPECIAL_ONKZS));
  }

  @Test
  public void testSplitAfterOnkz_Onkz() {
    assertArrayEquals(new String[] {"7227", "12345"}, PhoneNumberParser.splitAfterOnkz("722712345", ONKZS, SPECIAL_ONKZS));
    assertArrayEquals(new String[] {"7227", "12345"}, PhoneNumberParser.splitAfterOnkz("0722712345", ONKZS, SPECIAL_ONKZS));
    assertArrayEquals(new String[] {"664", "12345"}, PhoneNumberParser.splitAfterOnkz("66412345", ONKZS, SPECIAL_ONKZS));
    assertArrayEquals(new String[] {"664", "12345"}, PhoneNumberParser.splitAfterOnkz("066412345", ONKZS, SPECIAL_ONKZS));
  }

  @Test
  public void testContainsNonDigits() {

    assertTrue(PhoneNumberParser.containsNonDigits("abc"));
    assertTrue(PhoneNumberParser.containsNonDigits(" a b c "));

    assertFalse(PhoneNumberParser.containsNonDigits(null));
    assertFalse(PhoneNumberParser.containsNonDigits(""));
    assertFalse(PhoneNumberParser.containsNonDigits("1"));
    assertFalse(PhoneNumberParser.containsNonDigits("123"));
    assertFalse(PhoneNumberParser.containsNonDigits("1111"));
    assertFalse(PhoneNumberParser.containsNonDigits(" 1111 "));
  }

  @Test
  public void testGeneratePossibleNumbers() {
    assertEquals(Arrays.asList(new String[] {}), PhoneNumberParser.generateListOfPossibleNumbers(""));
    assertEquals(Arrays.asList(new String[] {}), PhoneNumberParser.generateListOfPossibleNumbers("1"));
    assertEquals(Arrays.asList(new String[] {}), PhoneNumberParser.generateListOfPossibleNumbers("21"));
    assertEquals(Arrays.asList(new String[] {"321"}), PhoneNumberParser.generateListOfPossibleNumbers("321"));
    assertEquals(Arrays.asList(new String[] {"3210", "321"}), PhoneNumberParser.generateListOfPossibleNumbers("3210"));
    assertEquals(Arrays.asList(new String[] {"3 2 1", "3 2 ", "3 2"}), PhoneNumberParser.generateListOfPossibleNumbers("3 2 1"));
  }

  @Test
  public void testIsFullyParsed() {

    // null or empty
    assertFalse(PhoneNumberParser.isFullyParsed(null));
    assertFalse(PhoneNumberParser.isFullyParsed(new String[] {}));

    // null values
    assertFalse(PhoneNumberParser.isFullyParsed(new String[] {null, null, null, null}));
    assertFalse(PhoneNumberParser.isFullyParsed(new String[] {"43", null, null, null}));
    assertFalse(PhoneNumberParser.isFullyParsed(new String[] {"43", "7227", null, null}));
    assertFalse(PhoneNumberParser.isFullyParsed(new String[] {"43", "7227", "12345", null}));
    assertFalse(PhoneNumberParser.isFullyParsed(new String[] {null, "7227", "12345", "67"}));

    // illegal length
    assertFalse(PhoneNumberParser.isFullyParsed(new String[] {"43", "7227", "12345"}));
    assertFalse(PhoneNumberParser.isFullyParsed(new String[] {"43", "7227", "12345", "67", "89"}));

    // valid
    assertTrue(PhoneNumberParser.isFullyParsed(new String[] {"43", "7227", "12345", "67"}));
    assertTrue(PhoneNumberParser.isFullyParsed(new String[] {"43", "7227", "12345", ""}));
  }

  @Test
  public void testSplitAfterCountryCode() {
    assertArrayEquals(new String[] {"43", "722712345"}, PhoneNumberParser.splitAfterCountryCode("+43722712345", COUNTRY_CODES));
    assertArrayEquals(new String[] {"43", "722712345"}, PhoneNumberParser.splitAfterCountryCode("0043722712345", COUNTRY_CODES));
  }

}
