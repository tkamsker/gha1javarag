package at.a1ta.cuco.core.shared.validator;

public class StreetValidator {

  public StreetValidator() {}

  public boolean isValid(String value) {
    return CommonValidator.isBlank(value) || CommonValidator.isStringLonger(value, 3);
  }
}
