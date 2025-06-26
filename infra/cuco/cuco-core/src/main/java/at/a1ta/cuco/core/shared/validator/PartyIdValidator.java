package at.a1ta.cuco.core.shared.validator;

public class PartyIdValidator {

  public PartyIdValidator() {}

  public boolean isValid(String value) {
    if (CommonValidator.isBlank(value)) {
      return true;
    }
    return isValidLeadSearch(value) || (value.length() == 9 && CommonValidator.containsOnlyDigits(value));
  }

  private boolean isValidLeadSearch(String value) {
    return value.trim().toUpperCase().startsWith("L") && CommonValidator.containsOnlyDigits(value.trim().toUpperCase().replaceFirst("L", ""));
  }

}
