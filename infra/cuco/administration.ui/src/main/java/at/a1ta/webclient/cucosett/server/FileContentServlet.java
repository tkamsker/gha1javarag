package at.a1ta.webclient.cucosett.server;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
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

public class FileContentServlet extends HttpServlet {

  private static final String ERROR_PREFIX = "@@FileContentServletError@@";

  private static final Logger log = LoggerFactory.getLogger(FileContentServlet.class);

  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    try {
      response.setContentType("text/html");
      FileItemFactory factory = new DiskFileItemFactory();
      ServletFileUpload servletFileUpload = new ServletFileUpload(factory);

      List<?> fileItemsList = servletFileUpload.parseRequest(request);
      Iterator<?> it = fileItemsList.iterator();
      while (it.hasNext()) {
        FileItem fileItem = (FileItem) it.next();
        if (!fileItem.isFormField()) {
          if (checkFile(fileItem)) {
            request.getSession().setAttribute("filecontent", fileItem.getString());
            request.getSession().setAttribute("filename", fileItem.getName());
          } else {
            log.error("Invalid file uploaded");
            response.getWriter().write(ERROR_PREFIX + "Es handelt sich um keine CSV Datei.");
          }
          // response.getWriter().write(fileItem.getString());
        }
      }
    } catch (FileUploadException e) {
      log.error(e.getMessage(), e);
      response.getWriter().write(ERROR_PREFIX + e.getMessage());
    }
  }

  private boolean checkFile(FileItem fileItem) {
    return fileItem != null && fileItem.getName() != null && fileItem.getName().toLowerCase().endsWith(".csv");
  }

}
