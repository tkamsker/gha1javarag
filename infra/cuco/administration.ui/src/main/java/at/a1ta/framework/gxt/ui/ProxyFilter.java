package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.data.BaseListLoader;
import com.extjs.gxt.ui.client.data.ModelData;


/**
 * @author q909158 Basic Interface for ProxyFilters
 * @param <M>
 */
public interface ProxyFilter<M> {

    /**
     * bins this instance to a loader. The loader.load method is called when this filter is validated.<br>
     * The filter can only be bound to loader which have a FilterablePagingMemoryProxy otherwise this function will throw an Exception<br>
     * 
     * @see at.telekom.webclient.cuco.client.util.ProxyFilter#bind(com.extjs.gxt.ui.client.data.BaseListLoader)
     * @param loader
     * @throws Exception if proxy is not an instance of FilterablePagingMemoryProxy
     */
    public void bind(BaseListLoader<?> loader) throws Exception;

    /**
     * @param m
     * @return false if row should be filtered out
     */
    public boolean doFilter(ModelData m);

    public M getValue();
}
