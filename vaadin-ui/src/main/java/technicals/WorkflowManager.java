package technicals;

import com.vaadin.data.util.BeanItemContainer;
import technicals.mdl.Measure;
import technicals.mdl.Workflow;

public class WorkflowManager {

    private Workflow currentWorkflow = null;

    public Workflow getCurrentWorkflow() {
        return currentWorkflow;
    }

    public void loadCurrentWorkflow(String currentWorkflowId) {
        this.currentWorkflow = Config.client(null).get().getWorkflow(currentWorkflowId);
    }

    public void newWorkflow(Workflow workflow) {
        String id = Config.client(null).get().saveWorkflow(workflow);
        loadCurrentWorkflow(id);
    }

    public BeanItemContainer<Measure> getMeasuresContainer() {
        BeanItemContainer<Measure> ctn = new BeanItemContainer<>(Measure.class);
        return ctn;
    }
}
