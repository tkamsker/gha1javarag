package at.a1ta.cuco.core.shared.model.contactperson;

import java.io.Serializable;
import java.util.Comparator;

import at.a1ta.cuco.core.shared.dto.ContactPerson;

public class ContactPersonComparator implements Comparator<ContactPerson>, Serializable {
  @Override
  public int compare(ContactPerson o1, ContactPerson o2) {
    String s1 = buildComparisonString(o1);
    String s2 = buildComparisonString(o2);
    return s1.compareTo(s2);
  }

  private String buildComparisonString(ContactPerson detail) {
    return detail.getAddressLine2() + " " + detail.getAddressLine1() + " " + detail.getLastname() + " " + detail.getFirstname();
  }
}
