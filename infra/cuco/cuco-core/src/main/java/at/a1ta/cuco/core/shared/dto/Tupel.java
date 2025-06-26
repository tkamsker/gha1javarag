package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class Tupel<N, M> implements Serializable {
  private N value1;
  private M value2;

  public Tupel() {}

  public Tupel(N value1, M value2) {
    super();
    this.value1 = value1;
    this.value2 = value2;
  }

  public N getValue1() {
    return value1;
  }

  public void setValue1(N value1) {
    this.value1 = value1;
  }

  public M getValue2() {
    return value2;
  }

  public void setValue2(M value2) {
    this.value2 = value2;
  }

}
