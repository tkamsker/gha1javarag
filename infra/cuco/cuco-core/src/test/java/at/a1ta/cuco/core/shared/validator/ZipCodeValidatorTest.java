package at.a1ta.cuco.core.shared.validator;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class ZipCodeValidatorTest {

  private ZipCodeValidator validator;

  @Before
  public void setup() {
    validator = new ZipCodeValidator();
  }

  @Test
  public void validZIPCodeNull() {
    assertTrue(validator.isValid(null));
  }

  @Test
  public void validZIPCodeEmpty() {
    assertTrue(validator.isValid(""));
  }

  @Test
  public void invalidZIPCodeTooShort3Digits() {
    assertFalse(validator.isValid("123"));
  }

  @Test
  public void invalidZIPCodeTooLong6Digits() {
    assertFalse(validator.isValid("123456"));
  }

  @Test
  public void validZIPCode4Digits() {
    assertTrue(validator.isValid("1234"));
  }

  @Test
  public void validZIPCode5Digits() {
    assertTrue(validator.isValid("12345"));
  }
}
