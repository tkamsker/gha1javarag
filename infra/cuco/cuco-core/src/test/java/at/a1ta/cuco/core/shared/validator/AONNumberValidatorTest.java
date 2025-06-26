package at.a1ta.cuco.core.shared.validator;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class AONNumberValidatorTest {

  private AONNumberValidator validator;

  @Before
  public void setup() {
    validator = new AONNumberValidator();
  }

  @Test
  public void validAONNumberNull() {
    assertTrue(validator.isValid(null));
  }

  @Test
  public void validAONNumberEmpty() {
    assertTrue(validator.isValid(""));
  }

  @Test
  public void validateCorrectAONNumber() {
    assertTrue(validator.isValid("123456"));
  }

  @Test
  public void invalidAONNumberTooShort() {
    assertFalse(validator.isValid("12345"));
  }

  @Test
  public void invalidAONNumberContainsInvalidCharacter() {
    assertFalse(validator.isValid("12345678x"));
  }

}
