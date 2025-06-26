package at.a1ta.cuco.admin.ui.common.client.dto;

import com.extjs.gxt.ui.client.data.BaseModelData;

import at.a1ta.cuco.core.shared.dto.RTCode;

public class RTCodeModel extends BaseModelData {
  private static final long serialVersionUID = 1L;

  public RTCodeModel() {
    // default constructor to support GWT parsing
  }

  public RTCodeModel(RTCode code) {
    setProdNum(code.getProdNum());
    setDescription(code.getDescription());
    setSales(code.getSales());
    setMonths(code.getMonths());
    setCode(code);
  }

  public final void setCode(RTCode c) {
    set("code", c);
  }

  public RTCode getCode() {
    return get("code");
  }

  public final void setProdNum(String prodNum) {
    set("prodNum", prodNum);
  }

  public final void setDescription(String description) {
    set("description", description);
  }

  public String getProdNum() {
    return get("prodNum");
  }

  public String getDescription() {
    return get("description");
  }

  public Number getMonths() {
    return get("months");
  }

  public final void setMonths(Number months) {
    set("months", months);
  }

  public String getSales() {
    Boolean b = get("salesBoolean");
    if (b == null) {
      return null;
    }
    if (b.booleanValue()) {
      return "J";
    }

    return "N";
  }

  public final void setSales(String sales) {
    set("sales", sales);
    set("salesBoolean", sales.equals("J"));
  }
}
