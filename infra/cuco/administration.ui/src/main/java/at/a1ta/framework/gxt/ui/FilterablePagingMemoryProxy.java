package at.a1ta.framework.gxt.ui;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import com.extjs.gxt.ui.client.data.BasePagingLoadResult;
import com.extjs.gxt.ui.client.data.DataReader;
import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.data.PagingLoadConfig;
import com.extjs.gxt.ui.client.data.PagingLoadResult;
import com.extjs.gxt.ui.client.data.PagingModelMemoryProxy;
import com.extjs.gxt.ui.client.util.DefaultComparator;
import com.google.gwt.user.client.rpc.AsyncCallback;

/**
 * This is a PagingMemoryProxy capable of filtering the results. You can bind as many ProxyFilterFields as you want. But
 * increasing the amount of filters will decrease the performance as every row has to be validated by every filter.
 * 
 * @author q909158
 */
public class FilterablePagingMemoryProxy extends PagingModelMemoryProxy implements FilterableMemoryProxy {

  private List<ProxyFilter<?>> filters = new ArrayList<ProxyFilter<?>>();

  /** Contains all models after filtering */
  private List<? extends ModelData> filtered;

  @SuppressWarnings("rawtypes")
  public FilterablePagingMemoryProxy(List data) {
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
  @SuppressWarnings({"unchecked", "rawtypes"})
  @Override
  public void load(DataReader<PagingLoadResult<? extends ModelData>> reader, Object loadConfig,
      AsyncCallback<PagingLoadResult<? extends ModelData>> callback) {
    List<? extends ModelData> data = new ArrayList<ModelData>((Collection<ModelData>) getData());
    final Comparator<Object> comparator = getComparator();

    try {
      if (reader != null) {
        data = (List) reader.read(loadConfig, data);
      }

      // filters whom values are not null, increases performance
      List<ProxyFilter<?>> notNull = new ArrayList<ProxyFilter<?>>();
      for (ProxyFilter filter : filters) {
        if (filter.getValue() != null) {
          notNull.add(filter);
        }
      }

      if (notNull.size() > 0) {
        List<ModelData> removes = new ArrayList();
        for (ModelData m : data) {
          for (ProxyFilter filter : notNull) {
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
          data.remove(m);
        }
      }

      PagingLoadConfig config = (PagingLoadConfig) loadConfig;

      if (config.getSortInfo().getSortField() != null) {
        final String sortField = config.getSortInfo().getSortField();
        if (sortField != null) {
          Collections.sort(data, config.getSortInfo().getSortDir().comparator(new Comparator<ModelData>() {

            @Override
            public int compare(ModelData o1, ModelData o2) {
              Object v1 = o1.get(sortField);
              Object v2 = o2.get(sortField);

              if (comparator != null) {
                return comparator.compare(v1, v2);
              }
              return DefaultComparator.INSTANCE.compare(v1, v2);
            }
          }));
        }
      }
      ArrayList<ModelData> sublist = new ArrayList<ModelData>();
      int start = config.getOffset();
      int limit = data.size();
      if (config.getLimit() > 0) {
        limit = Math.min(start + config.getLimit(), limit);
      }
      for (int i = config.getOffset(); i < limit; i++) {
        sublist.add(data.get(i));
      }
      filtered = new ArrayList<ModelData>(data);
      callback.onSuccess(new BasePagingLoadResult<ModelData>(sublist, config.getOffset(), data.size()));
    } catch (Exception e) {
      callback.onFailure(e);
    }
  }

  public List<? extends ModelData> getFiltered() {
    return filtered;
  }

}
