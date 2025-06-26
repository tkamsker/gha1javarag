/*
 * Copyright 2009 - 2012 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.webclient.cucosett.server.util;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.List;

import org.apache.commons.fileupload.FileItem;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import at.a1ta.cuco.core.service.ImageService;
import at.a1ta.cuco.core.service.ImageSizeService;
import at.a1ta.cuco.core.shared.dto.ImageSize;
import at.a1ta.pkb.ui.server.ImageUtil;

/**
 * Contains commonly used methods for filehandling. By now that's file extension utilities and ftp utilities
 */
public final class FileUtil {

  private final static Logger logger = LoggerFactory.getLogger(FileUtil.class);

  private FileUtil() {}

  private static void writeFile(String fullPath, byte[] data) {
    FileOutputStream fos = null;
    try {
      fos = new FileOutputStream(fullPath);
      fos.write(data);
      fos.flush();
    } catch (Exception e) {
      if (logger.isErrorEnabled()) {
        logger.error(e.getMessage(), e);
      }

    } finally {
      // clean up
      if (fos != null) {
        try {
          fos.close();
        } catch (IOException e1) {
          logger.error("Error during writing file " + fullPath, e1);
        }
      }
    }
  }

  private static String transformUmlaut(String s) {
    if (s == null) {
      return s;
    }

    String tmp = s;
    try {
      tmp = tmp.replaceAll("ä", "ae");
      tmp = tmp.replaceAll("ü", "ue");
      tmp = tmp.replaceAll("ö", "oe");
      tmp = tmp.replaceAll("Ä", "Ae");
      tmp = tmp.replaceAll("Ü", "Ue");
      tmp = tmp.replaceAll("Ö", "Oe");
      tmp = tmp.replaceAll("ß", "ss");
      tmp = tmp.replaceAll("\\(", "");
      tmp = tmp.replaceAll("\\)", "");
      tmp = tmp.replaceAll(" ", "_");
    } catch (Exception e) {
      if (logger.isWarnEnabled()) {
        logger.warn("Unable to encode " + s + "", e);
      }
    }
    if (logger.isDebugEnabled()) {
      logger.debug("Transformed " + s + " to " + tmp);
    }
    return tmp;
  }

  public static String saveNewFile(ImageSizeService imgSizeService, ImageService imgService, FileItem ff, String uuser, String path)
      throws FileNotFoundException, IOException, Exception {

    String filename = null;

    List<ImageSize> imageSizes = imgSizeService.getImageSizes();
    filename = FileUtil.transformUmlaut(ff.getName());
    int index = filename.lastIndexOf("\\");
    filename = filename.substring(index + 1);
    byte fileData[] = ff.get();

    for (ImageSize size : imageSizes) {
      try {
        byte imageData[];
        if (size.getWidth() != null && size.getHeight() != null) {
          imageData = ImageUtil.resizeImage(fileData, size.getWidth().intValue(), size.getHeight().intValue(), true);
        } else {
          imageData = fileData;
        }
        // Create necessary directories.
        File f = new File(path + size.getName());
        if (!f.exists()) {
          f.mkdirs();
        }
        String newImageFilename = createImageFilename(filename, size.getName());
        FileUtil.writeFile(path + newImageFilename, imageData);
        if (imgService.updateImage(uuser, newImageFilename, filename, size.getId()) == 0) {
          imgService.saveImage(uuser, newImageFilename, filename, size.getId());
        }
      } catch (Exception e) {
        logger.error("error saving file", e);
        throw new Exception("Bild konnte nicht gespeichert werden", e);
      }
    }
    return filename;
  }

  private static String createImageFilename(String filename, String sizeName) {
    return sizeName + "/" + filename;
  }
}
