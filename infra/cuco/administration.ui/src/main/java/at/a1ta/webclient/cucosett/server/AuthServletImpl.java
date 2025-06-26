package at.a1ta.webclient.cucosett.server;

import javax.servlet.annotation.WebServlet;
import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;

import at.a1ta.bite.core.server.service.AuthorityService;
import at.a1ta.bite.core.shared.dto.security.Authority;
import at.a1ta.bite.ui.server.servlet.SpringRemoteServiceServlet;
import at.a1ta.webclient.cucosett.client.service.AuthServlet;

@WebServlet(name = "auth", urlPatterns = {"/admin/cuco/auth.rpc"})
public class AuthServletImpl extends SpringRemoteServiceServlet implements AuthServlet {

  private static final long serialVersionUID = 1L;

  @Autowired
  private AuthorityService authorityService;

  @Override
  public ArrayList<Authority> getAllAuthorities() {
    return (ArrayList<Authority>) authorityService.getAllAuthorities();
  }

  @Override
  public ArrayList<Authority> getAllAuthorities(String filter) {
    return (ArrayList<Authority>) authorityService.getAllAuthorities(filter);
  }
}
