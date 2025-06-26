package at.a1ta.cuco.admin.ui.common.client.ui;

import com.google.gwt.user.client.ui.Grid;

import at.a1ta.bite.core.shared.dto.systemmessage.SystemMessage;
import at.a1ta.framework.gxt.ui.Util;
import at.a1ta.framework.ui.client.ErrorHandler;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.service.ServiceLocator;
import at.a1ta.framework.ui.client.util.HtmlUtils;
import at.a1ta.framework.ui.client.util.Validator;

public class SystemMessagePreviewComponent extends Grid {
  public SystemMessagePreviewComponent(final long messageId) {
    super(2, 1);

    ServiceLocator.getSystemMessageService().getMessageById(messageId, new BaseAsyncCallback<SystemMessage>() {
      @Override
      public void onFailure(Throwable caught) {
        ErrorHandler.onError("Server ist nicht erreichbar. Bitte nochmals versuchen", caught);
      }

      @Override
      public void onSuccess(SystemMessage result) {
        boolean hasImage = !Validator.isNullOrEmpty(result.getMessageContent().getImageUri());
        setHTML(0, 0, HtmlUtils.getBold(result.getMessageContent().getTitle()));
        String content = "<img height=\"150\" style=\"float: left; margin-right: 10px; margin-bottom: 10px; + "
            + (hasImage ? "" : "display:none;") + ")\" src=\"" + Util.getExtImgPath() + result.getMessageContent().getImageUri() + "\">"
            + "" + result.getMessageContent().getText();
        setHTML(1, 0, content);
      }
    });
  }
}
