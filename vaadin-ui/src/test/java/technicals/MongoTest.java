package technicals;


import org.testng.Assert;
import org.testng.annotations.AfterTest;
import org.testng.annotations.Test;
import technicals.mdl.Workflow;

import java.util.List;


public class MongoTest {
    String testingDb  = "testing";

    @Test(groups = { "functest" })
    public void testing_mongo_workflow() {
        Config testing = Config.client(testingDb).get();
        testing.saveWorkflow(new Workflow("dean"));
        String id2 = testing.saveWorkflow(new Workflow("dean2"));
        List<Workflow> workflows = testing.getWorkflows();
        Assert.assertEquals(workflows.size(), 2);
        Workflow wf = testing.getWorkflow(id2);
        Assert.assertEquals(wf.getName(), "dean2");
    }

    @AfterTest
    public void dropTestingDB() {
        Config.client(testingDb).get().dropDatabase();
    }


}