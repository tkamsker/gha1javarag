package at.a1ta.cuco.core.bean;


/**
 * This class is necessary for whitelisting any classes which the report uses and are not defined anywhere else as the return type of
 * the reporting is defined as <String,Object> and GWT doesn't know what to include for Object
 * so add every class here you need to whitelist for GWT RPC
 * 
 * @author Q909158
 */
public class ReportingWhitelist extends Reporting {
  private static final long serialVersionUID = 1L;

  private ReportingWhitelist() {}
}
