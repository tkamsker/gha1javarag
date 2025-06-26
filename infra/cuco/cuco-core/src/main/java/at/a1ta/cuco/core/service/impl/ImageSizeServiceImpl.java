package at.a1ta.cuco.core.service.impl;

import java.util.List;

import at.a1ta.cuco.core.dao.db.ImageSizeDao;
import at.a1ta.cuco.core.service.ImageSizeService;
import at.a1ta.cuco.core.shared.dto.ImageSize;

/**
 * @author richard.gebauer@telekom.at
 */
public class ImageSizeServiceImpl implements ImageSizeService {
  private ImageSizeDao imageSizeDao;

  public ImageSizeServiceImpl(final ImageSizeDao imageSizeDao) {
    if (imageSizeDao == null) {
      throw new org.apache.commons.lang.NullArgumentException("imageSizeDao");
    }
    this.imageSizeDao = imageSizeDao;
  }

  /**
   * @return list of all image sizes
   */
  @Override
  public List<ImageSize> getImageSizes() {
    return this.imageSizeDao.getImageSizes();
  }
}