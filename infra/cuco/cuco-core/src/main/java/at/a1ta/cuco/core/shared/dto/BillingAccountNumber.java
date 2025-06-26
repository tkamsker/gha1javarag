package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.HashSet;
import java.util.List;

public class BillingAccountNumber implements Serializable {
  private long ban;
  private HashSet<String> brands = new HashSet<String>(6);
  private String brand;
  private List<PhoneNumber> numbers;

  public long getBan() {
    return ban;
  }

  public void setBan(long ban) {
    this.ban = ban;
  }

  public void setBrands(HashSet<String> brands) {
    this.brands = brands;
  }

  public HashSet<String> getBrands() {
    return brands;
  }

  /**
   * this attribute is for ibatis only
   * 
   * @param brand
   */
  @Deprecated
  public void setBrand(String brand) {
    this.brand = brand;
  }

  /**
   * this attribute is for ibatis only
   * 
   * @param brand
   */
  @Deprecated
  public String getBrand() {
    return brand;
  }

  public List<PhoneNumber> getNumbers() {
    return numbers;
  }

  public void setNumbers(List<PhoneNumber> numbers) {
    this.numbers = numbers;
  }
}
