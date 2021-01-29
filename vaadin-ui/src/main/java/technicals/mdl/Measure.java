package technicals.mdl;

import java.util.Collection;
import java.util.Map;

/**
 * Created by dean.high on 20/11/2016.
 */
public class Measure extends Input {
    private Collection<Input> inputs;
    private String name;
    private Map<String,String> params;

    public Collection<Input> getInputs() {
        return inputs;
    }

    public void setInputs(Collection<Input> inputs) {
        this.inputs = inputs;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Map<String, String> getParams() {
        return params;
    }

    public void setParams(Map<String, String> params) {
        this.params = params;
    }
}
