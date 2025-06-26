package at.a1ta.cuco.core.dao.solr;

import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import at.a1ta.bite.data.solr.core.SolrTemplate;
import at.a1ta.bite.data.solr.repository.support.SimpleSolrRepository;

@RunWith(MockitoJUnitRunner.class)
public abstract class AbstractSolrRepositoryTest {
  
  @Mock
  SolrTemplate solrTemplateMock;
  
  void initMockedRepository(SimpleSolrRepository<?, ?> repository) {
    repository.setSolrTemplate(solrTemplateMock);
  }
  
}
