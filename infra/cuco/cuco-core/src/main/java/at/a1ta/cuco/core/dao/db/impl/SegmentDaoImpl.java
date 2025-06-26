package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.SegmentDao;
import at.a1ta.cuco.core.shared.dto.Segment;

public class SegmentDaoImpl extends AbstractDao implements SegmentDao {

  @Override
  public List<Segment> listSegments() {
    return performListQuery("SegSegment.list");
  }
}
