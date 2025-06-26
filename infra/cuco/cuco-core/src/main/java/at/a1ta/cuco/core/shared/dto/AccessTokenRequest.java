package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.Set;

public class AccessTokenRequest implements Iterable<Entry<String, String>>, Serializable {

  private String targetSystem;
  private String sourceSystem;

  private HashMap<String, String> parameters = new HashMap<String, String>();

  public AccessTokenRequest() {}

  public AccessTokenRequest(String targetSystem, String sourceSystem) {
    super();
    this.targetSystem = targetSystem;
    this.sourceSystem = sourceSystem;
  }

  public String getTargetSystem() {
    return targetSystem;
  }

  public void setTargetSystem(String targetSystem) {
    this.targetSystem = targetSystem;
  }

  public String getSourceSystem() {
    return sourceSystem;
  }

  public void setSourceSystem(String sourceSystem) {
    this.sourceSystem = sourceSystem;
  }

  public boolean hasParameters() {
    return parameters.isEmpty();
  }

  public String getParameter(String key) {
    return parameters.get(key);
  }

  public boolean containsParameter(String key) {
    return parameters.containsKey(key);
  }

  public String addParameter(String key, String value) {
    return parameters.put(key, value);
  }

  public Collection<String> getParameters() {
    return parameters.values();
  }

  public Set<Entry<String, String>> getParameterSet() {
    return parameters.entrySet();
  }

  @Override
  public Iterator<Entry<String, String>> iterator() {
    return getParameterSet().iterator();
  }

}
