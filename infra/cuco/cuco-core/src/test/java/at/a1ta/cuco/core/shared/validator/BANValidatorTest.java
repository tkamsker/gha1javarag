package at.a1ta.cuco.core.shared.validator;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BANValidatorTest {

  private BANValidator validator;

  @Before
  public void setup() {
    validator = new BANValidator();
  }

  @Test
  public void validBANNull() {
    assertTrue(validator.isValid(null));
  }

  @Test
  public void validBANEmpty() {
    assertTrue(validator.isValid(""));
  }

  @Test
  public void validateCorrectBAN() {
    assertTrue(validator.isValid("123456789"));
  }

  @Test
  public void invalidBANTooShort() {
    assertFalse(validator.isValid("123"));
  }

  @Test
  public void invalidBANContainsInvalidCharacter() {
    assertFalse(validator.isValid("12345678x"));
  }

}
