package at.a1ta.cuco.core.service.impl;

import java.util.List;

import at.a1ta.cuco.core.dao.db.ImageDao;
import at.a1ta.cuco.core.service.ImageService;
import at.a1ta.cuco.core.shared.dto.Image;

/**
 * @author richard.gebauer@telekom.at
 */
public class ImageServiceImpl implements ImageService {
  private ImageDao imageDao;

  public ImageServiceImpl(final ImageDao imageDao) {
    if (imageDao == null) {
      throw new org.apache.commons.lang.NullArgumentException("imageDao");
    }
    this.imageDao = imageDao;
  }

  /**
   * @param id
   * @param uuser
   * @param filename
   * @param name
   * @param imageSizeId
   * @return list of images
   */
  @Override
  public List<Image> getImages(final Number id, final String uuser, final String filename, final String name, final Number imageSizeId) {
    return this.imageDao.getImages(id, uuser, filename, name, imageSizeId);
  }

  /**
   * @param uuser
   * @param filename
   * @param name
   * @param imageSizeId
   */
  @Override
  public void saveImage(final String uuser, final String filename, final String name, final Number imageSizeId) {
    this.imageDao.saveImage(uuser, filename, name, imageSizeId);
  }

  /**
   * @param uuser
   * @param filename
   * @param name
   * @param imageSizeId
   * @return number of affected rows
   */
  @Override
  public int updateImage(final String uuser, final String filename, final String name, final Number imageSizeId) {
    return this.imageDao.updateImage(uuser, filename, name, imageSizeId);
  }
}