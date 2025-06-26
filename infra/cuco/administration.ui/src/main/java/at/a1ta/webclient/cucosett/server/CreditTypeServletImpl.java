package at.a1ta.webclient.cucosett.server;

import javax.servlet.annotation.WebServlet;
import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.ui.server.servlet.SpringRemoteServiceServlet;
import at.a1ta.cuco.core.service.CreditTypeService;
import at.a1ta.cuco.core.shared.dto.CreditType;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.webclient.cucosett.client.service.CreditTypeServlet;

@WebServlet(name = "creditType", urlPatterns = {"/admin/cuco/creditType.rpc"})
public class CreditTypeServletImpl extends SpringRemoteServiceServlet implements CreditTypeServlet {

  private static final long serialVersionUID = -1737440649543126895L;

  @Autowired
  private CreditTypeService creditTypeService;

  @Override
  public RpcStatus deleteCreditType(Long id) {

    creditTypeService.deleteCreditType(id);
    return RpcStatus.OK;

  }

  @Override
  public ArrayList<CreditType> getAllCreditTypes() {
    return (ArrayList<CreditType>) creditTypeService.getAllCreditTypes();
  }

  @Override
  public CreditType saveCreditType(CreditType ct) {
    creditTypeService.saveCreditType(ct);
    return ct;
  }

}
