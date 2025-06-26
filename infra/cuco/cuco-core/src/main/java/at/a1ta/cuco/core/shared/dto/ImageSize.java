package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;

public class ImageSize implements Serializable {
  private Long id;
  private String name;
  private Long width;
  private Long height;

  public Long getHeight() {
    return this.height;
  }

  public Long getId() {
    return this.id;
  }

  public String getName() {
    return this.name;
  }

  public Long getWidth() {
    return this.width;
  }

  public void setHeight(final Long height) {
    this.height = height;
  }

  public void setId(final Long id) {
    this.id = id;
  }

  public void setName(final String name) {
    this.name = name;
  }

  public void setWidth(final Long width) {
    this.width = width;
  }
}