package at.a1ta.cuco.core.shared.dto;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;

public class MatrixData implements Serializable {
  private ArrayList<Segment> segments;
  private ArrayList<Category> categories;
  private HashMap<Long, HashMap<Long, ArrayList<ProductGroup>>> matrixData = new HashMap<Long, HashMap<Long, ArrayList<ProductGroup>>>();
  private long partyId;

  public MatrixData() {}

  public MatrixData(ArrayList<Segment> segments, ArrayList<Category> categories) {
    this.segments = segments;
    this.categories = categories;
  }

  public void setMatrixData(ArrayList<MatrixPosition<ProductGroup>> groups) {
    for (MatrixPosition<ProductGroup> posGroup : groups) {
      ProductGroup group = posGroup.getObject();
      addMatrixData(posGroup.getSegment(), posGroup.getCategory(), group);
    }
  }

  private void addMatrixData(long segment, long category, ProductGroup prodGroup) {
    HashMap<Long, ArrayList<ProductGroup>> mapOfCategories = matrixData.get(segment); // contains the categories of a
    // segment

    if (mapOfCategories == null) {
      mapOfCategories = new HashMap<Long, ArrayList<ProductGroup>>();
      matrixData.put(segment, mapOfCategories);
    }

    ArrayList<ProductGroup> entries = mapOfCategories.get(category); // contains all productgroups of a matrixentry
    if (entries == null) {
      entries = new ArrayList<ProductGroup>();
      mapOfCategories.put(category, entries);
    }

    entries.add(prodGroup);
  }

  public ArrayList<ProductGroup> getProductgroups(long segment, long category) {
    try {
      ArrayList<ProductGroup> ret = matrixData.get(segment).get(category);
      // check if ret is null to get no nullpointer exception if the calling class whant's so access the list
      if (ret == null) {
        return new ArrayList<ProductGroup>();
      }
      return ret;
    } catch (NullPointerException e) {
      return new ArrayList<ProductGroup>();
    }
  }

  public ArrayList<Segment> getSegments() {
    return segments;
  }

  public ArrayList<Category> getCategories() {
    return categories;
  }

  public void setPartyId(long partyId) {
    this.partyId = partyId;
  }

  public long getPartyId() {
    return partyId;
  }

}
