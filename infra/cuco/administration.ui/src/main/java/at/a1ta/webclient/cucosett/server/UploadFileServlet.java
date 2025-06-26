package at.a1ta.webclient.cucosett.server;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Iterator;
import java.util.List;

import org.apache.commons.fileupload.FileItem;
import org.apache.commons.fileupload.FileItemFactory;
import org.apache.commons.fileupload.FileUploadException;
import org.apache.commons.fileupload.disk.DiskFileItemFactory;
import org.apache.commons.fileupload.servlet.ServletFileUpload;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.support.WebApplicationContextUtils;

import at.a1ta.cuco.core.service.ImageService;
import at.a1ta.cuco.core.service.ImageSizeService;
import at.a1ta.cuco.ui.common.server.servlet.SpringServlet;
import at.a1ta.webclient.cucosett.server.util.FileUtil;

/** * Servlet implementation class for Servlet: UploadFileServlet */
public class UploadFileServlet extends SpringServlet {

  private static final long serialVersionUID = 8305367618713715640L;

  private static final Logger logger = LoggerFactory.getLogger(UploadFileServlet.class);

  private String remotePath;

  private String uUser;

  private FileItem file;

  private ImageSizeService imageSizeService;

  private ImageService imageService;

  public UploadFileServlet() {}

  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    WebApplicationContext ctx = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());
    imageSizeService = (ImageSizeService) ctx.getBean("imageSizeService");
    imageService = (ImageService) ctx.getBean("imageService");

    response.setContentType("text/html");
    uUser = getUsername(request);
    readParameters(request);

    if (file.get().length == 0) {
      response.getWriter().write("Die Datei darf nicht leer sein!");
    } else if (!file.getName().substring(file.getName().lastIndexOf(".") + 1).equalsIgnoreCase("jpg")) {
      response.getWriter().write("Es sind nur jpg Bilder erlaubt!");
    } else {
      try {
        FileUtil.saveNewFile(imageSizeService, imageService, file, uUser, remotePath);
        response.getWriter().write("Bild wurde erfolgreich hochgeladen!");
      } catch (Exception ex) {
        response.getWriter().write("Bild konnte nicht gespeichert werden!");
      }

    }
  }

  private void readParameters(HttpServletRequest request) {
    FileItemFactory factory = new DiskFileItemFactory();
    ServletFileUpload upload = new ServletFileUpload(factory);

    try {
      List<?> items = upload.parseRequest(request);
      Iterator<?> it = items.iterator();
      while (it.hasNext()) {
        FileItem item = (FileItem) it.next();
        if (!item.isFormField() && item.getFieldName().equals("uploadFormElement")) {
          file = item;
        } else if (item.isFormField() && item.getFieldName().equals("remotePath")) {
          remotePath = item.getString();
          if (!remotePath.endsWith("/")) {
            remotePath += "/";
          }
        }
      }
    } catch (FileUploadException e) {
      logger.error(e.getMessage());
    }
  }
}
