package at.a1ta.cuco.core.shared.validator;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CityValidatorTest {

  @Mock
  private CityValidator validator;

  @Before
  public void setup() {
    validator = new CityValidator();
  }

  @Test
  public void validCityNull() {
    assertTrue(validator.isValid(null));
  }

  @Test
  public void validCityEmpty() {
    assertTrue(validator.isValid(""));
  }

  @Test
  public void invalidCityTooShort() {
    assertFalse(validator.isValid("L"));
  }

  @Test
  public void validCity() {
    assertTrue(validator.isValid("Li"));
  }
}
