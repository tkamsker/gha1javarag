package at.a1ta.cuco.core.dao.util;

import java.util.Properties;

import org.apache.axis2.AxisFault;
import org.apache.axis2.context.ConfigurationContext;

import com.telekomaustriagroup.esb.briana1.BrianA1Stub;

public class BrianCeeQueryOrderStub extends BrianA1Stub {

  public BrianCeeQueryOrderStub() throws AxisFault {
    super();
  }

  public BrianCeeQueryOrderStub(ConfigurationContext configurationContext, String httpEndpoint, String username, String pwd, Properties prop) throws AxisFault {
    super(configurationContext, httpEndpoint, username, pwd, prop);
  }

  public BrianCeeQueryOrderStub(ConfigurationContext configurationContext, String jmsServer1, String jmsServer2, String username, String pwd, Long defaultTimeoutMillisec, Properties prop)
      throws AxisFault {
    super(configurationContext, jmsServer1, jmsServer2, username, pwd, defaultTimeoutMillisec, prop);
  }

  public BrianCeeQueryOrderStub(ConfigurationContext configurationContext, String jmsServer1, String jmsServer2, String username, String pwd, Long defaultTimeoutMillisec) throws AxisFault {
    super(configurationContext, jmsServer1, jmsServer2, username, pwd, defaultTimeoutMillisec);
  }

  public BrianCeeQueryOrderStub(ConfigurationContext configurationContext, String httpEndpoint, String username, String pwd) throws AxisFault {
    super(configurationContext, httpEndpoint, username, pwd);
  }

  public BrianCeeQueryOrderStub(String httpEndpoint, String username, String pwd, Properties prop) throws AxisFault {
    super(httpEndpoint, username, pwd, prop);
  }

  public BrianCeeQueryOrderStub(String jmsServer1, String jmsServer2, String username, String pwd, Long defaultTimeoutMillisec, Properties prop) throws AxisFault {
    super(jmsServer1, jmsServer2, username, pwd, defaultTimeoutMillisec, prop);
  }

  public BrianCeeQueryOrderStub(String jmsServer1, String jmsServer2, String username, String pwd, Long defaultTimeoutMillisec) throws AxisFault {
    super(jmsServer1, jmsServer2, username, pwd, defaultTimeoutMillisec);
  }

  public BrianCeeQueryOrderStub(String httpEndpoint, String username, String pwd) throws AxisFault {
    super(httpEndpoint, username, pwd);
  }

}
