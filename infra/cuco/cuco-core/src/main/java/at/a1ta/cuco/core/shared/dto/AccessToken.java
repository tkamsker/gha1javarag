package at.a1ta.cuco.core.shared.dto;

public class AccessToken {

  private String targetSystem;
  private String token;

  public static final AccessToken NONE = new AccessToken() {

    @Override
    public final boolean isValid() {
      return false;
    }

  };

  public AccessToken() {}

  public AccessToken(String targetSystem) {
    super();
    this.targetSystem = targetSystem;
  }

  public AccessToken(String targetSystem, String token) {
    super();
    this.targetSystem = targetSystem;
    this.token = token;
  }

  public String getTargetSystem() {
    return targetSystem;
  }

  public void setTargetSystem(String targetSystem) {
    this.targetSystem = targetSystem;
  }

  public String getToken() {
    return token;
  }

  public void setToken(String token) {
    this.token = token;
  }

  public boolean isValid() {
    return token != null;
  }

  @Override
  public String toString() {
    return "AccessToken [targetSystem=" + targetSystem + ", token=" + token + "]";
  }

}
