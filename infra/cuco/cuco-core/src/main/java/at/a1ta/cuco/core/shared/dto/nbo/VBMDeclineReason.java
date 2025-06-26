package at.a1ta.cuco.core.shared.dto.nbo;

import java.io.Serializable;

public class VBMDeclineReason implements Serializable {
  private String declineReasonId;
  private String declineReasonText;
  private String productId;

  public String getDeclineReasonId() {
    return declineReasonId;
  }

  public void setDeclineReasonId(String declineReasonId) {
    this.declineReasonId = declineReasonId;
  }

  public String getDeclineReasonText() {
    return declineReasonText;
  }

  public void setDeclineReasonText(String declineReasonText) {
    this.declineReasonText = declineReasonText;
  }

  public String getProductId() {
    return productId;
  }

  public void setProductId(String productId) {
    this.productId = productId;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) return true;
    if (obj == null) return false;
    if (getClass() != obj.getClass()) return false;
    VBMDeclineReason other = (VBMDeclineReason) obj;
    if (declineReasonText == null) {
      if (other.declineReasonText != null) return false;
    } else if (!declineReasonText.equals(other.declineReasonText)) return false;
    return true;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((declineReasonText == null) ? 0 : declineReasonText.hashCode());
    return result;
  }

}
