package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Date;

import org.apache.solr.client.solrj.beans.Field;

public class Person implements Serializable {
  private static final long serialVersionUID = 1L;
  private String firstname;
  private String gender;
  private String lastname;
  private Date birthdate;
  private String title;
  private String salutation;

  public String getFirstname() {
    return firstname != null ? firstname : "";
  }

  @Field("firstname")
  public void setFirstname(String firstname) {
    this.firstname = firstname;
  }

  public String getGender() {
    return gender;
  }

  @Field("gender")
  public void setGender(String gender) {
    this.gender = gender;
  }

  public String getLastname() {
    return lastname;
  }

  @Field("lastname")
  public void setLastname(String lastname) {
    this.lastname = lastname;
  }

  public Date getBirthdate() {
    return birthdate;
  }

  @Field("birthdate")
  public void setBirthdate(Date birthdate) {
    this.birthdate = birthdate;
  }

  public String getTitle() {
    return title;
  }

  @Field("title")
  public void setTitle(String title) {
    this.title = title;
  }

  public String getSalutation() {
    return salutation;
  }

  @Field("salutation")
  public void setSalutation(String salutation) {
    this.salutation = salutation;
  }

  @SuppressWarnings("deprecation")
  public boolean hasBirthdayToday() {
    Date today = new Date();
    return (this.birthdate != null && birthdate.getDate() == today.getDate() && birthdate.getMonth() == today.getMonth());
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((birthdate == null) ? 0 : birthdate.hashCode());
    result = prime * result + ((firstname == null) ? 0 : firstname.hashCode());
    result = prime * result + ((gender == null) ? 0 : gender.hashCode());
    result = prime * result + ((lastname == null) ? 0 : lastname.hashCode());
    result = prime * result + ((salutation == null) ? 0 : salutation.hashCode());
    result = prime * result + ((title == null) ? 0 : title.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) {
      return true;
    }
    if (obj == null) {
      return false;
    }
    if (getClass() != obj.getClass()) {
      return false;
    }
    Person other = (Person) obj;
    if (birthdate == null) {
      if (other.birthdate != null) {
        return false;
      }
    } else if (!birthdate.equals(other.birthdate)) {
      return false;
    }
    if (firstname == null) {
      if (other.firstname != null) {
        return false;
      }
    } else if (!firstname.equals(other.firstname)) {
      return false;
    }
    if (gender == null) {
      if (other.gender != null) {
        return false;
      }
    } else if (!gender.equals(other.gender)) {
      return false;
    }
    if (lastname == null) {
      if (other.lastname != null) {
        return false;
      }
    } else if (!lastname.equals(other.lastname)) {
      return false;
    }
    if (salutation == null) {
      if (other.salutation != null) {
        return false;
      }
    } else if (!salutation.equals(other.salutation)) {
      return false;
    }
    if (title == null) {
      if (other.title != null) {
        return false;
      }
    } else if (!title.equals(other.title)) {
      return false;
    }
    return true;
  }

  @Override
  public String toString() {
    return "Person [firstname=" + firstname + ", gender=" + gender + ", lastname=" + lastname + ", birthdate=" + birthdate + ", title=" + title + ", salutation=" + salutation + "]";
  }

}
