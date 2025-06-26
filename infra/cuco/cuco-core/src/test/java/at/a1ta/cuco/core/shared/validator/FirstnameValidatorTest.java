package at.a1ta.cuco.core.shared.validator;

import static org.junit.Assert.assertTrue;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class FirstnameValidatorTest {

  private FirstnameValidator validator;

  @Before
  public void setup() {
    validator = new FirstnameValidator();
  }

  @Test
  public void validateCorrectFirstname() {
    assertTrue(validator.isValid());
  }

}
