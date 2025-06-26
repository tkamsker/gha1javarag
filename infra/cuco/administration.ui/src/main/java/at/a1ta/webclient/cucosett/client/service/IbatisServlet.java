package at.a1ta.webclient.cucosett.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

import at.a1ta.framework.ui.client.dto.RpcStatus;

@RemoteServiceRelativePath("cuco/ibatis.rpc")
public interface IbatisServlet extends RemoteService {
    public ArrayList<String> getDaos();

    public RpcStatus flushDao(String name);

    public RpcStatus flushAll();
}