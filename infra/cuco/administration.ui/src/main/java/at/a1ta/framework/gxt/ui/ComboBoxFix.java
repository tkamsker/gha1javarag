package at.a1ta.framework.gxt.ui;

import com.extjs.gxt.ui.client.data.ModelData;
import com.extjs.gxt.ui.client.widget.form.ComboBox;

public class ComboBoxFix<D extends ModelData> extends ComboBox<D> {

    @Override
    public void expand() {
        try {
            super.expand();
        } catch (Exception e) {
            super.expand();
        }
    }

}
