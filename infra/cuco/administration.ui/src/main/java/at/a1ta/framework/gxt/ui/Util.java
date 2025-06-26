package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.widget.toolbar.PagingToolBar;

public class Util {

  public static String getExtImgPath() {
    return "extImg/";
  }

  // if no min width is set, the width of the button is set to 0
  // see: http://www.extjs.com/forum/showthread.php?t=89068
  private static class PagingToolBarFix extends PagingToolBar {
    private static final int minWidth = 22;

    public PagingToolBarFix(int pageSize) {
      super(pageSize);
      first.setMinWidth(minWidth);
      prev.setMinWidth(minWidth);
      next.setMinWidth(minWidth);
      last.setMinWidth(minWidth);
      refresh.setMinWidth(minWidth);
    }
  }

  public static PagingToolBar createPagingToolBar(int pagingSize) {
    return new PagingToolBarFix(pagingSize);
  }
}
