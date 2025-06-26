package at.a1ta.webclient.cucosett.server;

import javax.servlet.annotation.WebServlet;
import java.util.ArrayList;

import org.springframework.orm.ibatis.support.SqlMapClientDaoSupport;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.support.WebApplicationContextUtils;

import at.a1ta.bite.ui.server.servlet.SpringRemoteServiceServlet;
import at.a1ta.framework.ui.client.dto.RpcStatus;
import at.a1ta.webclient.cucosett.client.service.IbatisServlet;

@WebServlet(name = "ibatis", urlPatterns = {"/admin/cuco/ibatis.rpc"})
public class IbatisServletImpl extends SpringRemoteServiceServlet implements IbatisServlet {

  @Override
  public RpcStatus flushAll() {
    WebApplicationContext ctx = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());
    ArrayList<String> names = getDaos();

    for (String name : names) {
      SqlMapClientDaoSupport dao = (SqlMapClientDaoSupport) ctx.getBean(name);
      dao.getSqlMapClient().flushDataCache();
    }

    return RpcStatus.OK;
  }

  @Override
  public RpcStatus flushDao(String name) {
    WebApplicationContext ctx = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());
    SqlMapClientDaoSupport dao = (SqlMapClientDaoSupport) ctx.getBean(name);
    dao.getSqlMapClient().flushDataCache();
    return RpcStatus.OK;
  }

  @Override
  public ArrayList<String> getDaos() {
    WebApplicationContext ctx = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());
    String[] names = ctx.getBeanNamesForType(SqlMapClientDaoSupport.class);
    ArrayList<String> result = new ArrayList<String>();
    for (String s : names) {
      result.add(s);
    }

    return result;
  }
}
