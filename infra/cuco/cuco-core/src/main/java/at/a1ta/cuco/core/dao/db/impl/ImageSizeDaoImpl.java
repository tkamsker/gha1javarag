package at.a1ta.cuco.core.dao.db.impl;

import java.util.List;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.ImageSizeDao;
import at.a1ta.cuco.core.shared.dto.ImageSize;

public class ImageSizeDaoImpl extends AbstractDao implements ImageSizeDao {

  @Override
  public List<ImageSize> getImageSizes() {
    return performListQuery("ImageSize.GetImageSizes", null);
  }
}