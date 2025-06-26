package at.a1ta.cuco.core.shared.validator;

public class OneTVUserValidator {

  public OneTVUserValidator() {
    // Default Constructor
  }

  public boolean isValid(String value, String pattern) {
    if (CommonValidator.isBlank(value)) {
      return true;
    }
    return value.matches(pattern);
  }
}
