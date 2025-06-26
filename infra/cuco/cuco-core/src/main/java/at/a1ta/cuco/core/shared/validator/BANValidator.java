package at.a1ta.cuco.core.shared.validator;

public class BANValidator {

  public BANValidator() {}

  public boolean isValid(String value) {
    if (CommonValidator.isBlank(value)) {
      return true;
    }
    return value.length() == 9 && CommonValidator.containsOnlyDigits(value);
  }
}
