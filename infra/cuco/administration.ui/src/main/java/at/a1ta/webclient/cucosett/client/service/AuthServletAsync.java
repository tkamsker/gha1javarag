package at.a1ta.webclient.cucosett.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.bite.core.shared.dto.security.Authority;

public interface AuthServletAsync {
  public void getAllAuthorities(AsyncCallback<ArrayList<Authority>> callback);

  public void getAllAuthorities(String filter, AsyncCallback<ArrayList<Authority>> callback);

}
