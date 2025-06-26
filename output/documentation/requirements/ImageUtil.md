# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/service/util/ImageUtil.java

ImageUtil.java
1. Purpose: Utility class for image processing operations
2. User interactions: No direct user interactions - backend utility
3. Data handling:
   - Works with Image and BufferedImage objects
   - Handles image byte arrays
   - Performs image I/O operations
4. Business rules: None explicitly visible
5. Dependencies:
   - java.awt.Image
   - java.awt.image.BufferedImage
   - javax.imageio.ImageIO
   - javax.swing.ImageIcon
   - SLF4J logging framework

Requirements:
- Must provide image processing utility functions
- Must handle image format conversions
- Must implement proper error handling for image operations
- Must log operations using SLF4J