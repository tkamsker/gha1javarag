package at.a1ta.cuco.core.shared.validator;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class StreetValidatorTest {

  private StreetValidator validator;

  @Before
  public void setup() {
    validator = new StreetValidator();
  }

  @Test
  public void validStreetNull() {
    assertTrue(validator.isValid(null));
  }

  @Test
  public void validStreetEmpty() {
    assertTrue(validator.isValid(""));
  }

  @Test
  public void invalidStreetTooShort() {
    assertFalse(validator.isValid("Pa"));
  }

  @Test
  public void validStreet() {
    assertTrue(validator.isValid("Lin"));
  }

}
