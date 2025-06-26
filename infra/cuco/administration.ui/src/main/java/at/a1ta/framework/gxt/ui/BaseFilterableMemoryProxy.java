package at.a1ta.framework.gxt.ui;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import com.extjs.gxt.ui.client.data.BaseListLoadConfig;
import com.extjs.gxt.ui.client.data.BaseListLoadResult;
import com.extjs.gxt.ui.client.data.DataReader;
import com.extjs.gxt.ui.client.data.ListLoadResult;
import com.extjs.gxt.ui.client.data.MemoryProxy;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.util.DefaultComparator;
import com.google.gwt.user.client.rpc.AsyncCallback;

/**
 * This is a PagingMemoryProxy capable of filtering the results. You can bind as many ProxyFilterFields as you want. But
 * increasing the amount of filters will decrease the performance as every row has to be validated by every filter.
 * 
 * @author q909158
 */
public class BaseFilterableMemoryProxy extends MemoryProxy<ListLoadResult<? extends ModelData>> implements FilterableMemoryProxy {

  private List<ProxyFilter<?>> filters = new ArrayList<ProxyFilter<?>>();

  /** Contains all models after filtering */
  public BaseFilterableMemoryProxy(List<?> data) {
    super(data);
  }

  /**
   * adds a filter to the proxy<br>
   * this function should not be called by hand, but by the bind function of filters
   * 
   * @param filter
   */
  @Override
  public void addFilter(ProxyFilter<?> filter) {
    filters.add(filter);
  }

  /**
   * this is a direct copy of the load function of the basic class with the extension that it filters the rows with the
   * ProxyFilters
   * 
   * @see com.extjs.gxt.ui.client.data.PagingModelMemoryProxy#load(com.extjs.gxt.ui.client.data.DataReader, java.lang.Object,
   *      com.google.gwt.user.client.rpc.AsyncCallback)
   */
  @SuppressWarnings("unchecked")
  @Override
  public void load(DataReader<ListLoadResult<? extends ModelData>> reader, Object loadConfig,
      AsyncCallback<ListLoadResult<? extends ModelData>> callback) {
    List<ModelData> loadedData = new ArrayList<ModelData>((Collection<ModelData>) getData());

    try {
      if (reader != null) {
        loadedData = (List<ModelData>) reader.read(loadConfig, loadedData);
      }

      // filters whom values are not null, increases performance
      List<ProxyFilter<?>> notNull = new ArrayList<ProxyFilter<?>>();
      for (ProxyFilter<?> filter : filters) {
        if (filter.getValue() != null) {
          notNull.add(filter);
        }
      }

      if (notNull.size() > 0) {
        List<ModelData> removes = new ArrayList<ModelData>();
        for (ModelData m : loadedData) {
          for (ProxyFilter<?> filter : notNull) {
            try {
              if (!filter.doFilter(m)) {
                removes.add(m);
                break;
              }
            } catch (Exception e) {
              removes.add(m);
              break;
            }
          }
        }
        for (ModelData m : removes) {
          loadedData.remove(m);
        }
      }

      BaseListLoadConfig config = (BaseListLoadConfig) loadConfig;

      if (config.getSortInfo().getSortField() != null) {
        final String sortField = config.getSortInfo().getSortField();
        if (sortField != null) {
          Collections.sort(loadedData, config.getSortInfo().getSortDir().comparator(new Comparator<ModelData>() {

            @Override
            public int compare(ModelData o1, ModelData o2) {
              Object v1 = o1.get(sortField);
              Object v2 = o2.get(sortField);

              return DefaultComparator.INSTANCE.compare(v1, v2);
            }
          }));
        }
      }
      callback.onSuccess(new BaseListLoadResult<ModelData>(loadedData));
    } catch (Exception e) {
      callback.onFailure(e);
    }
  }
}
