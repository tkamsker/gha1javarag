package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;

public class SimplePage<T> implements Serializable {

  private long count;
  private ArrayList<T> content;
  private boolean isInputValid = true;

  public SimplePage() {}

  public long getCount() {
    return count;
  }

  public void setCount(long count) {
    this.count = count;
  }

  public ArrayList<T> getContent() {
    if (content == null) {
      return new ArrayList<T>();
    }
    return content;
  }

  public void setContent(ArrayList<T> content) {
    this.content = content;
  }

  public void setInputValid(boolean isInputValid) {
    this.isInputValid = isInputValid;
  }

  public boolean isInputValid() {
    return isInputValid;
  }

}
