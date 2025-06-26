package at.a1ta.webclient.cucosett.client.dialog;

import java.util.Date;
import java.util.logging.Logger;

import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.uibinder.client.UiBinder;
import com.google.gwt.uibinder.client.UiField;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.Widget;

import at.a1ta.bite.ui.client.PopupFrame;
import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.bite.ui.client.widget.Button;
import at.a1ta.bite.ui.client.widget.InputBox;
import at.a1ta.bite.ui.client.widget.TextArea;
import at.a1ta.cuco.admin.ui.common.client.bundle.AdminUI;
import at.a1ta.cuco.admin.ui.common.client.event.AddTeamEvent;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class EditTeamsDialog extends Composite {

  // @formatter:off
  private static EditTeamsDialogUiBinder uiBinder = GWT.create(EditTeamsDialogUiBinder.class);

  private static Logger logger = Logger.getLogger(EditTeamsDialog.class.getName());

  interface EditTeamsDialogUiBinder extends UiBinder<Widget, EditTeamsDialog> {}

  private static EditTeamsDialog _instance = null;

  private Team team;

  private PopupFrame popupFrame;

  @UiField
  InputBox teamName;
  @UiField
  TextArea txtDescription;
  @UiField
  Button bSave;
  @UiField
  Button bCancel;

  public static EditTeamsDialog getInstance() {
    if (_instance == null) {
      _instance = new EditTeamsDialog();
    }
    _instance.teamName.setValue("");
    _instance.txtDescription.setValue("");
    return _instance;
  }

  public static EditTeamsDialog getInstance(Team team) {
    EditTeamsDialog instance = getInstance();
    instance.setTeam(team);
    return instance;
  }

  private void setTeam(Team team) {
    this.team = team;
    teamName.setValue(team.getName());
    txtDescription.setValue(team.getDescription());
  }

  public EditTeamsDialog() {
    initWidget(uiBinder.createAndBindUi(this));
    popupFrame = new PopupFrame(this, 365, 200);
    bSave.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        save();
      }
    });

    bCancel.addClickHandler(new ClickHandler() {
      @Override
      public void onClick(ClickEvent event) {
        cancel();
      }

      private void cancel() {
        popupFrame.close();
      }
    });

  }

  protected void save() {
    if (!teamName.validate() || !txtDescription.validate()) {
      Window.alert("\"Name\" ist ein Pflichtfeld");
      return;
    }
    Window.alert("Team speichern");

    if (team == null) {
      team = new Team();
      team.setCreator(UserManager.getUserInfo().getBiteUser());
      team.setCreateDate(new Date());
    }
    team.setName(teamName.getValue());
    team.setDescription(txtDescription.getValue());
    SettingsServiceLocator.getTeamServlet().saveTeam(team, new BaseAsyncCallback<Team>() {

      @Override
      public void onSuccess(Team result) {
        PortletEventManager.fireEvent(new AddTeamEvent(team));
        popupFrame.close();
      }

      @Override
      public void onFailure(Throwable exception) {
        Window.alert(AdminUI.ADMINCOMMONTEXTPOOL.messageboxSaveError());
      }
    });
  }

  public void show(Team tm) {
    if (tm == null) {
      teamName.clear();
      txtDescription.clear();
    } else {
      team = tm;
      teamName.setText(team.getName());
      txtDescription.setText(team.getDescription());
    }
    popupFrame.hideMessageBar();
    popupFrame.showContent();
  }

  public void hide() {
    popupFrame.hide();
  }
}
