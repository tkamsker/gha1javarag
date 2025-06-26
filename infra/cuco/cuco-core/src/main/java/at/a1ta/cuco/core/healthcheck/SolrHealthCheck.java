/*
 * Copyright 2009 - 2013 by A1 Telekom Austria AG
 * All Rights Reserved.
 * 
 * The Software is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * All information contained herein is, and remains the property of
 * A1 Telekom Austria AG and its suppliers, if any.
 * The intellectual and technical concepts contained herein are proprietary
 * to A1 Telekom Austria AG and its suppliers and may be covered by
 * intertional or national patents, patents in process, and are protected
 * by trade secret or copyright law. Dissemination of this information or
 * reproduction of this material is strictly forbidden unless prior written
 * permission is obtained from A1 Telekom Austria AG.
 */
package at.a1ta.cuco.core.healthcheck;

import org.apache.solr.client.solrj.SolrServer;
import org.apache.solr.client.solrj.response.SolrPingResponse;

import com.codahale.metrics.health.HealthCheck;

public class SolrHealthCheck extends HealthCheck {

  private final SolrServer solrServer;

  public SolrHealthCheck(SolrServer solrServer) {
    this.solrServer = solrServer;
  }

  @Override
  protected Result check() throws Exception {
    SolrPingResponse response = solrServer.ping();
    return Result.healthy("status: " + response.getStatus());
  }

}
