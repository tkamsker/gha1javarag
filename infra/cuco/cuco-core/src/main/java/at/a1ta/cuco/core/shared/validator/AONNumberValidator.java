package at.a1ta.cuco.core.shared.validator;

public class AONNumberValidator {

  public AONNumberValidator() {}

  public boolean isValid(String value) {
    if (CommonValidator.isBlank(value)) {
      return true;
    }
    return CommonValidator.isStringLonger(value, 6) && CommonValidator.containsOnlyDigits(value);
  }
}
