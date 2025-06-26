package at.a1ta.cuco.core.shared.validator;

public class CommonValidator {

  public static boolean containsOnlyDigits(String value) {
    String onlyDigits = value.replaceAll("[^0-9]", "");
    return !value.isEmpty() && value.equals(onlyDigits);
  }

  public static boolean isStringLengthBetween(String value, int minLen, int maxLen) {
    return value != null && value.length() >= minLen && value.length() <= maxLen;
  }

  public static boolean isStringLonger(String value, int minLen) {
    return value != null && value.length() >= minLen;
  }

  public static boolean isBlank(String value) {
    return value == null || value.trim().isEmpty();
  }
}
