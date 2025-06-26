package at.a1ta.cuco.core.shared.validator;

public class CityValidator {

  public CityValidator() {}

  public boolean isValid(String value) {
    return CommonValidator.isBlank(value) || CommonValidator.isStringLonger(value, 2);
  }
}
