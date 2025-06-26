package at.a1ta.cuco.core.shared.validator;

public class ZipCodeValidator {

  public ZipCodeValidator() {}

  public boolean isValid(String value) {
    if (CommonValidator.isBlank(value)) {
      return true;
    }
    return CommonValidator.isStringLengthBetween(value, 4, 5) && CommonValidator.containsOnlyDigits(value);
  }
}
