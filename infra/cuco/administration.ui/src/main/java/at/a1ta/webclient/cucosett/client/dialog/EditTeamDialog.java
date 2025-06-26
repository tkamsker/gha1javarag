package at.a1ta.webclient.cucosett.client.dialog;

import java.util.Date;

import com.extjs.gxt.ui.client.widget.Dialog;
import com.extjs.gxt.ui.client.widget.MessageBox;
import com.extjs.gxt.ui.client.widget.button.Button;
import com.extjs.gxt.ui.client.widget.form.TextArea;
import com.extjs.gxt.ui.client.widget.form.TextField;
import com.extjs.gxt.ui.client.widget.layout.FitLayout;
import com.google.gwt.user.client.ui.FlexTable;
import com.google.gwt.user.client.ui.HTML;

import at.a1ta.bite.ui.client.handler.UserManager;
import at.a1ta.cuco.admin.ui.common.client.event.CuCoEventType;
import at.a1ta.cuco.core.shared.dto.Team;
import at.a1ta.framework.ui.client.command.BaseAsyncCallback;
import at.a1ta.framework.ui.client.event.GenericEvent;
import at.a1ta.framework.ui.client.event.PortletEventManager;
import at.a1ta.webclient.cucosett.client.service.SettingsServiceLocator;

public class EditTeamDialog extends Dialog {

  private static EditTeamDialog _instance = null;

  private Team team = null;

  private TextField<String> name = new TextField<String>();

  private TextArea description = new TextArea();

  public static EditTeamDialog getInstance() {
    if (_instance == null) {
      _instance = new EditTeamDialog();
    }
    _instance.name.setValue("");
    _instance.description.setValue("");
    return _instance;
  }

  public static EditTeamDialog getInstance(Team team) {
    EditTeamDialog instance = getInstance();
    instance.setTeam(team);
    return instance;
  }

  private void setTeam(Team team) {
    this.team = team;
    name.setValue(team.getName());
    description.setValue(team.getDescription());
  }

  public EditTeamDialog() {
    setSize(400, 200);
    setResizable(false);
    okText = "Speichern";
    cancelText = "Abbrechen";
    setButtons(Dialog.OKCANCEL);
    setHeading("Team");
    setModal(true);

    name.addStyleName("field-necessary");
    name.setAllowBlank(false);
    name.setWidth(300);
    name.setMaxLength(32);
    description.setWidth(300);
    description.setHeight(80);
    description.setMaxLength(1000);

    FlexTable table = new FlexTable();
    table.setWidget(0, 0, new HTML("Name"));
    table.setWidget(0, 1, name);
    table.setWidget(1, 0, new HTML("Beschreibung"));
    table.setWidget(1, 1, description);

    setLayout(new FitLayout());
    add(table);
  }

  @Override
  protected void onButtonPressed(Button button) {
    super.onButtonPressed(button);
    if (button == getButtonById(OK)) {

      if (!name.validate() || !description.validate()) {
        MessageBox.info("Team", "\"Name\" ist ein Pflichtfeld", null);
        return;
      }

      final MessageBox wait = MessageBox.wait("Team", "Team speichern", "speichern...");
      wait.show();

      if (team == null) {
        team = new Team();
        team.setCreator(UserManager.getUserInfo().getBiteUser());
        team.setCreateDate(new Date());
      }

      team.setName(name.getValue());
      team.setDescription(description.getValue());

      SettingsServiceLocator.getTeamServlet().saveTeam(team, new BaseAsyncCallback<Team>() {

        @Override
        public void onSuccess(Team result) {
          wait.close();
          PortletEventManager.fireEvent(new GenericEvent<Void>(CuCoEventType.UPDATE_TEAMS));
          hide();
        }

        @Override
        public void onFailure(Throwable exception) {
          wait.close();
          MessageBox.info("Team", "Speichern Fehlgeschlagen", null);
        }

      });
    }
    if (button == getButtonById(CANCEL)) {
      hide();
    }
  }

  @Override
  protected void onHide() {
    super.onHide();
    team = null;
  }
}
