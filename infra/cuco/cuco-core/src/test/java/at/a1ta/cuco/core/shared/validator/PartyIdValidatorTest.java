package at.a1ta.cuco.core.shared.validator;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class PartyIdValidatorTest {

  private PartyIdValidator validator;

  @Before
  public void setup() {
    validator = new PartyIdValidator();
  }

  @Test
  public void validPartyIdNull() {
    assertTrue(validator.isValid(null));
  }

  @Test
  public void validPartyIdEmpty() {
    assertTrue(validator.isValid(""));
  }

  @Test
  public void validateCorrectPartyId() {
    assertTrue(validator.isValid("123456789"));
  }

  @Test
  public void invalidPartyIdTooShort() {
    assertFalse(validator.isValid("123"));
  }

  @Test
  public void invalidPartyIdContainsInvalidCharacter() {
    assertFalse(validator.isValid("12345678x"));
  }

}
