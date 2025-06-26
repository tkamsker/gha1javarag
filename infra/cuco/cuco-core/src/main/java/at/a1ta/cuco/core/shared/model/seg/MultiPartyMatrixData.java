package at.a1ta.cuco.core.shared.model.seg;

import java.util.ArrayList;
import java.util.HashMap;

import at.a1ta.cuco.core.shared.dto.MatrixPosition;

public class MultiPartyMatrixData {
  private HashMap<Long, HashMap<Long, ArrayList<MultiPartyProductGroup>>> matrixData = new HashMap<Long, HashMap<Long, ArrayList<MultiPartyProductGroup>>>();

  public void setMatrixData(ArrayList<MatrixPosition<MultiPartyProductGroup>> groups) {
    for (MatrixPosition<MultiPartyProductGroup> posGroup : groups) {
      MultiPartyProductGroup group = posGroup.getObject();
      addMatrixData(posGroup.getSegment(), posGroup.getCategory(), group);
    }
  }

  private void addMatrixData(long segment, long category, MultiPartyProductGroup prodGroup) {
    HashMap<Long, ArrayList<MultiPartyProductGroup>> mapOfCategories = matrixData.get(segment); // contains the categories of a
    // segment

    if (mapOfCategories == null) {
      mapOfCategories = new HashMap<Long, ArrayList<MultiPartyProductGroup>>();
      matrixData.put(segment, mapOfCategories);
    }

    ArrayList<MultiPartyProductGroup> entries = mapOfCategories.get(category); // contains all productgroups of a matrixentry
    if (entries == null) {
      entries = new ArrayList<MultiPartyProductGroup>();
      mapOfCategories.put(category, entries);
    }

    entries.add(prodGroup);
  }

  public ArrayList<MultiPartyProductGroup> getProductgroups(long segment, long category) {
    try {
      ArrayList<MultiPartyProductGroup> ret = matrixData.get(segment).get(category);
      // check if ret is null to get no nullpointer exception if the calling class whant's so access the list
      if (ret == null) {
        return new ArrayList<MultiPartyProductGroup>();
      }
      return ret;
    } catch (NullPointerException e) {
      return new ArrayList<MultiPartyProductGroup>();
    }
  }
}
