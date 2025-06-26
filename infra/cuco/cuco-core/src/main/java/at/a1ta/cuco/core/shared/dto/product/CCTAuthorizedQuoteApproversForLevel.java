package at.a1ta.cuco.core.shared.dto.product;

import java.io.Serializable;
import java.util.ArrayList;

public class CCTAuthorizedQuoteApproversForLevel implements Serializable {
  private static final long serialVersionUID = 1L;
  private int level;
  private ArrayList<CCTOrgStructureElement> approvers;

  public int getLevel() {
    return level;
  }

  public void setLevel(int level) {
    this.level = level;
  }

  public ArrayList<CCTOrgStructureElement> getApprovers() {
    return approvers;
  }

  public void setApprovers(ArrayList<CCTOrgStructureElement> approvers) {
    this.approvers = approvers;
  }

}
