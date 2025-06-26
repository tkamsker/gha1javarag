package at.a1ta.webclient.cucosett.client.ui;

import com.google.gwt.user.client.ui.FlowPanel;

public class SettingsCell extends FlowPanel {
    Long segment;
    Long category;

    public SettingsCell(Long segment, Long category) {
        this.segment = segment;
        this.category = category;
    }
}
