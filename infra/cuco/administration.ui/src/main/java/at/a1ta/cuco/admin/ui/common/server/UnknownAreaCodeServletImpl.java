package at.a1ta.cuco.admin.ui.common.server;

import javax.servlet.annotation.WebServlet;
import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.ui.server.servlet.SpringRemoteServiceServlet;
import at.a1ta.cuco.admin.ui.common.client.service.UnknownAreaCodeServlet;
import at.a1ta.cuco.core.service.UnknownAreaCodeService;
import at.a1ta.cuco.core.shared.dto.UnknownAreaCode;
import at.a1ta.framework.ui.client.dto.RpcStatus;

@WebServlet(name = "unknownAreaCode", urlPatterns = {"/admin/cuco/unknownAreaCode.rpc", "/app/unknownAreaCode.rpc"})
public class UnknownAreaCodeServletImpl extends SpringRemoteServiceServlet implements UnknownAreaCodeServlet {
  @Autowired
  private UnknownAreaCodeService unknownAreaCodeService;

  @Override
  public RpcStatus deleteUnknownAreaCode(Long id) {
    unknownAreaCodeService.deleteUnknownAreaCode(id);
    return RpcStatus.OK;
  }

  @Override
  public ArrayList<UnknownAreaCode> getAllUnknownAreaCodes() {
    return (ArrayList<UnknownAreaCode>) unknownAreaCodeService.getAllUnknownAreaCodes();
  }

  @Override
  public UnknownAreaCode saveUnknownAreaCode(UnknownAreaCode code) {
    unknownAreaCodeService.saveUnknownAreaCode(code);
    return code;
  }
}
