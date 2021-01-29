package technicals;

import javax.servlet.annotation.WebServlet;

import com.google.common.collect.Lists;
import com.mongodb.MongoClient;
import com.vaadin.annotations.Theme;
import com.vaadin.annotations.VaadinServletConfiguration;
import com.vaadin.data.Property;
import com.vaadin.server.VaadinRequest;
import com.vaadin.server.VaadinServlet;
import com.vaadin.ui.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.tylproject.vaadin.addon.MongoContainer;
import technicals.mdl.Measure;
import technicals.mdl.Symbols;
import technicals.mdl.Workflow;

import java.net.UnknownHostException;

/**
 * This UI is the application entry point. A UI may either represent a browser window
 * (or tab) or some part of a html page where a Vaadin application is embedded.
 * <p>
 * The UI is initialized using {@link #init(VaadinRequest)}. This method is intended to be
 * overridden to add component to the user interface and initialize non-component functionality.
 */
@Theme("valo")
public class TaUI extends UI {
    private final Logger logger = LoggerFactory.getLogger(TaUI.class);
    private WorkflowManager workflowManager = new WorkflowManager();

    @Override
    protected void init(VaadinRequest vaadinRequest) {
        final VerticalLayout layout = new VerticalLayout();
        final TabSheet tabsheet = new TabSheet();


        try {
            tabsheet.addTab(initAdminTab(), "Admin");
            tabsheet.addTab(initWorkflowTab(), "WorkflowBuilder");
            tabsheet.addTab(new VerticalLayout(), "BackTesting");
            layout.addComponents(tabsheet);
            setContent(layout);
        } catch (Throwable e) {
            logger.error("Could not load vaadin UI", e);
            throw new RuntimeException("Failed to load UI, make this a better response");
        }
    }

    private Layout initAdminTab() throws UnknownHostException {
        final VerticalLayout admin = new VerticalLayout();
        final MongoContainer<Symbols> sourcesMongoContainer = sourcesContainer();
        final Table sources = new Table("Sources", sourcesMongoContainer);
        // Allow selecting items from the table.
        sources.setSelectable(true);
        // Send changes in selection immediately to server.
        sources.setImmediate(true);
        sources.addValueChangeListener((Property.ValueChangeListener) event -> System.out.println("Selected: " + sources.getValue()));
        admin.addComponent(sources);
        return admin;
    }

    private PopupView newWorkflowPopup() {
        FormLayout popupContent = new FormLayout();
        popupContent.setWidthUndefined();

        TextField name = new TextField("Name");
        name.setWidth("30%");
        Button save = new Button("Save");
        save.addClickListener((Button.ClickListener) event ->
                workflowManager.newWorkflow(new Workflow(name.getValue())));
        popupContent.addComponent(name);
        popupContent.addComponent(save);

        PopupView popup = new PopupView(null, popupContent);
        popup.setHideOnMouseOut(false);
        return popup;
    }

    private VerticalLayout initWorkflowTab() throws UnknownHostException {
        final VerticalLayout v = new VerticalLayout();
        final MongoContainer<Workflow> workflowMongoContainer = workflowsContainer();
        final HorizontalLayout hl = new HorizontalLayout();
        final VerticalLayout vl = new VerticalLayout();
        final HorizontalSplitPanel singleWorkflowBuilder = new HorizontalSplitPanel();
        final Table measures = new Table("Measures");
        final Table triggers = new Table("Triggers");
        final ComboBox wfSelector = new ComboBox(null, workflowMongoContainer);
        final Label wfLbl = new Label("");

        wfSelector.setItemCaptionPropertyId("name");
        wfSelector.setNullSelectionAllowed(false);

        PopupView newWorkflowPopup = newWorkflowPopup();

        final Button loadButton = new Button("Load Workflow");
        loadButton.addClickListener(click -> {
            workflowManager.loadCurrentWorkflow(wfSelector.getValue().toString());
            measures.setContainerDataSource(workflowManager.getMeasuresContainer());
            wfLbl.setValue(workflowManager.getCurrentWorkflow().getName());

        });

        final Button newWorkflowButton = new Button("New Workflow");
        newWorkflowButton.addClickListener(click -> newWorkflowPopup.setPopupVisible(true));

        PopupView measurePopup = createAddMeasurePopup();
        final Button addMeasureButton = new Button("Add Measure");
        addMeasureButton.addClickListener(click -> measurePopup.setPopupVisible(true));

        hl.addComponent(wfSelector);
        hl.addComponent(loadButton);
        hl.addComponent(newWorkflowButton);
        hl.addComponent(addMeasureButton);
        hl.addComponent(wfLbl);

        wfSelector.select(wfSelector.getItemIds().iterator().next());

        vl.addComponent(singleWorkflowBuilder);
        hl.addComponent(measurePopup);
        hl.addComponent(newWorkflowPopup);


        singleWorkflowBuilder.addComponents(measures, triggers);

        v.addComponent(hl);
        v.addComponent(vl);

        //v.addComponent(new AddMeasure());
        return v;
    }

    private PopupView createAddMeasurePopup() {
        FormLayout popupContent = new FormLayout();
        popupContent.setWidthUndefined();

        final TextField name = new TextField("Name");
        name.setWidth("30%");
        ComboBox type = new ComboBox("Measure Type", Lists.newArrayList("MA"));
        Button save = new Button("Save");
        save.addClickListener((Button.ClickListener) event -> {
                Measure m  = new Measure();
                m.setName(name.getValue());
                workflowManager.getCurrentWorkflow().getMeasures().add(m);
                workflowManager.saveCurrentWorkflow();
        });
        popupContent.addComponent(name);
        popupContent.addComponent(type);
        popupContent.addComponent(save);

        PopupView popup = new PopupView(null, popupContent);
        popup.setHideOnMouseOut(false);
        return popup;
    }

    private MongoContainer<Workflow> workflowsContainer() throws UnknownHostException {
        MongoOperations mo = new MongoTemplate(new MongoClient(), "admin");
        return
                MongoContainer.Builder
                        .forEntity(Workflow.class, mo).build();
    }

    private MongoContainer<Symbols> sourcesContainer() throws UnknownHostException {
        MongoOperations mo = new MongoTemplate(new MongoClient(), "admin");
        return
                MongoContainer.Builder
                        .forEntity(Symbols.class, mo).build();
    }

    @WebServlet(urlPatterns = "/*", name = "MyUIServlet", asyncSupported = true)
    @VaadinServletConfiguration(ui = TaUI.class, productionMode = false)
    public static class MyUIServlet extends VaadinServlet {
    }
}
