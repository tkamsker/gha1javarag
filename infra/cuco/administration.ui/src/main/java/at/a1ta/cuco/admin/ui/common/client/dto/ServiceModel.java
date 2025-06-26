package at.a1ta.cuco.admin.ui.common.client.dto;

import com.extjs.gxt.ui.client.data.BaseModelData;

import at.a1ta.cuco.core.shared.dto.Service;

public class ServiceModel extends BaseModelData {
  private static final long serialVersionUID = 1L;
  private static final String ID = "id";
  private static final String NAME = "name";
  private static final String COSTS = "costs";
  private static final String BEAN = "bean";

  public ServiceModel() {
    // default constructor to support GWT parsing
  }

  public ServiceModel(Service service) {
    setName(service.getName());
    setCosts(service.getCosts());
    setId(service.getId());
    setBean(service);
  }

  public final void setName(String name) {
    set(NAME, name);
  }

  public final void setCosts(Double costs) {
    set(COSTS, costs);
  }

  public final void setId(Long id) {
    set(ID, id);
  }

  public String getName() {
    return get(NAME);
  }

  public Float getCosts() {
    return get(COSTS);
  }

  public Long getId() {
    return get(ID);
  }

  public final void setBean(Service service) {
    set(BEAN, service);
  }

  public Service getBean() {
    return get(BEAN);
  }

  @Override
  public boolean equals(Object obj) {
    ServiceModel m = (ServiceModel) obj;
    return m != null && m.getId().equals(getId());
  }

  @Override
  public int hashCode() {
    return getId().hashCode();
  }
}
