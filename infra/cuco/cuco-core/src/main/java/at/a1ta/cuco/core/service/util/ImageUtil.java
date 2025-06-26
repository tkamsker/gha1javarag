package at.a1ta.cuco.core.service.util;

import java.awt.Image;
import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.ImageIcon;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * contains image processing utility functions
 * 
 * @author martin.gutenbrunner@telekom.at
 */
public final class ImageUtil {

  private static final Logger logger = LoggerFactory.getLogger(ImageUtil.class);

  private ImageUtil() {}

  /**
   * handles resizing of images. this is very useful for uploading video thumbnails and user's images which can be of
   * specific sizes for display purposes
   * 
   * @param imageData original image data
   * @param width desired width
   * @param height desired height
   * @param preserveAspectRatio whether image must not be stretched
   * @return resized image data
   */
  public static byte[] resizeImage(final byte imageData[], final int width, final int height, final boolean preserveAspectRatio) {
    if (logger.isDebugEnabled()) {
      logger.debug("ImageUtil::resizeImage width:" + width + ", height:" + height);
    }

    final ImageIcon imageIcon = new ImageIcon(imageData);
    final ImageIcon thumb;
    final BufferedImage img;
    int h = imageIcon.getIconHeight();
    int w = imageIcon.getIconWidth();

    if (h > height || w > width) {
      if (preserveAspectRatio) {
        // w / h = width / height.
        if (w * height < width * h) {
          w = -1;
          h = height;
        } else {
          w = width;
          h = -1;
        }
      } else {
        w = width;
        h = height;
      }
    }
    thumb = new ImageIcon(imageIcon.getImage().getScaledInstance(w, h, Image.SCALE_SMOOTH));
    img = new BufferedImage(thumb.getIconWidth(), thumb.getIconHeight(), BufferedImage.TYPE_INT_RGB);
    img.getGraphics().drawImage(thumb.getImage(), 0, 0, null);
    try {
      final ByteArrayOutputStream baos = new ByteArrayOutputStream();
      ImageIO.write(img, "jpg", baos);
      return baos.toByteArray();
    } catch (final IOException ioe) {
      if (logger.isErrorEnabled()) {
        logger.error(ioe.getMessage(), ioe);
      }
    }
    return null;
  }
}
