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
package at.a1ta.cuco.core.configuration;

import java.io.File;
import java.util.concurrent.TimeUnit;

import javax.annotation.PreDestroy;
import javax.annotation.Resource;
import javax.sql.DataSource;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.Configuration;

import at.a1ta.bite.core.health.DatabaseHealthCheck;
import at.a1ta.bite.data.solr.core.SolrTemplate;
import at.a1ta.cuco.core.healthcheck.SolrHealthCheck;

import com.codahale.metrics.CsvReporter;
import com.codahale.metrics.MetricRegistry;
import com.codahale.metrics.SharedMetricRegistries;
import com.codahale.metrics.health.HealthCheckRegistry;
import com.codahale.metrics.health.jvm.ThreadDeadlockHealthCheck;
import com.ryantenney.metrics.spring.config.annotation.MetricsConfigurerAdapter;

@Configuration
//@EnableMetrics
public class MetricsConfiguration extends MetricsConfigurerAdapter {

  public static final String REGISTRY = "CUCOMETRICS";

  @Resource
  private ConfigurableApplicationContext context;

  @Value(value = "${metrics.csv.report.file.path:D:/logs/cuco/}")
  private String csvReportFilePath;

  private CsvReporter reporter;

  @Override
  public MetricRegistry getMetricRegistry() {
    return SharedMetricRegistries.getOrCreate(REGISTRY);
  }

  @Override
  public HealthCheckRegistry getHealthCheckRegistry() {
    HealthCheckRegistry healthCheckRegistry = new HealthCheckRegistry();
    healthCheckRegistry.register("CuCo-Database", new DatabaseHealthCheck((DataSource) context.getBean("dataSourceCuCo")));
    healthCheckRegistry.register("PKB-Database", new DatabaseHealthCheck((DataSource) context.getBean("dataSourcePKB")));
    healthCheckRegistry.register("Solr-Server", new SolrHealthCheck(((SolrTemplate) context.getBean("solrPartyTemplate")).getSolrServer()));
    healthCheckRegistry.register("Deadlocks", new ThreadDeadlockHealthCheck());
    return healthCheckRegistry;
  }

  @Override
  public void configureReporters(MetricRegistry metricRegistry) {
    reporter = CsvReporter.forRegistry(metricRegistry).build(new File(csvReportFilePath));
    reporter.start(5, TimeUnit.MINUTES);
  }

  @PreDestroy
  private void cleanUp() {
    reporter.stop();
  }
}
