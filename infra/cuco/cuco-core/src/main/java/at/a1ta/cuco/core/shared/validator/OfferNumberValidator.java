package at.a1ta.cuco.core.shared.validator;

public class OfferNumberValidator {

  public OfferNumberValidator() {
    // Default Constructor
  }

  public boolean isValid(String value) {
    if (CommonValidator.isBlank(value)) {
      return true;
    }
    return true;
  }
}
