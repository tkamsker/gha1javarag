package at.a1ta.cuco.core.shared.validator;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class LastnameValidatorTest {

  private LastnameValidator validator;

  @Before
  public void setup() {
    validator = new LastnameValidator();
  }

  @Test
  public void validLastnameNull() {
    assertTrue(validator.isValid(null));
  }

  @Test
  public void validLastnameEmpty() {
    assertTrue(validator.isValid(""));
  }

  @Test
  public void validateCorrectLastname() {
    assertTrue(validator.isValid("Preinfalk"));
  }

  @Test
  public void invalidLastname() {
    assertFalse(validator.isValid("Pr"));
  }

}
