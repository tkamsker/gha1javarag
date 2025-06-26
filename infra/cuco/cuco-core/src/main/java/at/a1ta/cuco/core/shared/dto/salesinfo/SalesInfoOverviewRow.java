package at.a1ta.cuco.core.shared.dto.salesinfo;

import java.io.Serializable;
import java.util.Comparator;
import java.util.Date;

import at.a1ta.cuco.core.shared.dto.OverviewStatus;
import at.a1ta.cuco.core.shared.dto.ReadOnlyStatusBasedOnCategory;

/**
 * Marker Interface for the UI
 */
public abstract class SalesInfoOverviewRow implements Serializable {

  /**
   * Copy Constructor
   * 
   * @param salesInfoOverviewRow a <code>SalesInfoOverviewRow</code> object
   */
  public SalesInfoOverviewRow(SalesInfoOverviewRow salesInfoOverviewRow) {
    this.overviewStatus = salesInfoOverviewRow.overviewStatus;
    this.statusBasedOnCaregory = salesInfoOverviewRow.statusBasedOnCaregory;
  }

  public SalesInfoOverviewRow() {
    // TODO Auto-generated constructor stub
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((overviewStatus == null) ? 0 : overviewStatus.hashCode());
    result = prime * result + ((statusBasedOnCaregory == null) ? 0 : statusBasedOnCaregory.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj) return true;
    if (obj == null) return false;
    if (getClass() != obj.getClass()) return false;
    SalesInfoOverviewRow other = (SalesInfoOverviewRow) obj;
    if (overviewStatus != other.overviewStatus) return false;
    if (statusBasedOnCaregory != other.statusBasedOnCaregory) return false;
    return true;
  }

  private OverviewStatus overviewStatus;

  private ReadOnlyStatusBasedOnCategory statusBasedOnCaregory;

  public enum SalesInfoNoteGroups {
    ALL, QUOTE, NOTE, REPORT, SALES_CONV
  }

  public static Comparator<SalesInfoOverviewRow> lastModDateComparator = new Comparator<SalesInfoOverviewRow>() {

    @Override
    public int compare(SalesInfoOverviewRow row1, SalesInfoOverviewRow row2) {
      if (row1.getLastModDate().before(row2.getLastModDate())) {
        return -1;
      } else if (row1.getLastModDate().after(row2.getLastModDate())) {
        return 1;
      } else {
        return 0;
      }
    }
  };

  public abstract Date getLastModDate();

  public static Comparator<SalesInfoOverviewRow> getLastModDateComparator() {
    return lastModDateComparator;
  }

  public OverviewStatus getOverviewStatus() {
    return overviewStatus;
  }

  public void setOverviewStatus(OverviewStatus overviewStatus) {
    this.overviewStatus = overviewStatus;
  }

  public ReadOnlyStatusBasedOnCategory getStatusBasedOnCaregory() {
    return statusBasedOnCaregory;
  }

  public void setStatusBasedOnCaregory(ReadOnlyStatusBasedOnCategory havingReadOnlyProductCategories) {
    this.statusBasedOnCaregory = havingReadOnlyProductCategories;
  }

}
