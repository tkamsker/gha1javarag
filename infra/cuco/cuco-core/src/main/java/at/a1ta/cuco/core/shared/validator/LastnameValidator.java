package at.a1ta.cuco.core.shared.validator;

public class LastnameValidator {

  public LastnameValidator() {}

  public boolean isValid(String value) {
    return CommonValidator.isBlank(value) || CommonValidator.isStringLonger(value, 3);
  }
}
