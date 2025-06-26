package at.a1ta.webclient.cucosett.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.bite.core.shared.dto.security.Authority;

@RemoteServiceRelativePath("cuco/auth.rpc")
public interface AuthServlet extends RemoteService {
  public ArrayList<Authority> getAllAuthorities();

  public ArrayList<Authority> getAllAuthorities(String filter);

}
