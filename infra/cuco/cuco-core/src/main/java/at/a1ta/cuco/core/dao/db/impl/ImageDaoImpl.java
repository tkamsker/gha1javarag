package at.a1ta.cuco.core.dao.db.impl;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import at.a1ta.bite.core.server.dao.AbstractDao;
import at.a1ta.cuco.core.dao.db.ImageDao;
import at.a1ta.cuco.core.shared.dto.Image;

public class ImageDaoImpl extends AbstractDao implements ImageDao {
  @Override
  public List<Image> getImages(final Number id, final String uuser, final String filename, final String name, final Number imageSizeId) {
    final Map<String, Object> params = new HashMap<String, Object>();

    params.put("id", id);
    params.put("uuser", uuser);
    params.put("filename", filename);
    params.put("name", name);
    params.put("imageSizeId", imageSizeId);
    return performListQuery("Image.GetImages", params);
  }

  @Override
  public void saveImage(final String uuser, final String filename, final String name, final Number imageSizeId) {
    final Map<String, Object> params = new HashMap<String, Object>();

    params.put("uuser", uuser);
    params.put("filename", filename);
    params.put("name", name);
    params.put("imageSizeId", imageSizeId);
    executeInsert("Image.SaveImage", params);
  }

  @Override
  public int updateImage(final String uuser, final String filename, final String name, final Number imageSizeId) {
    final Map<String, Object> params = new HashMap<String, Object>();

    params.put("uuser", uuser);
    params.put("filename", filename);
    params.put("name", name);
    params.put("imageSizeId", imageSizeId);
    return executeUpdate("Image.UpdateImage", params);
  }
}