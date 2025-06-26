package at.a1ta.webclient.cucosett.client.service;

import java.util.ArrayList;

import com.google.gwt.user.client.rpc.AsyncCallback;

import at.a1ta.framework.ui.client.dto.RpcStatus;

public interface IbatisServletAsync {
    public void getDaos(AsyncCallback<ArrayList<String>> callback);

    public void flushDao(String name, AsyncCallback<RpcStatus> callback);

    public void flushAll(AsyncCallback<RpcStatus> callback);
}
