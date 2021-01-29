package technicals;

import static org.springframework.data.mongodb.core.query.Criteria.where;

import com.mongodb.MongoClient;
import org.springframework.data.mongodb.core.MongoOperations;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Query;
import technicals.mdl.Workflow;

import java.net.UnknownHostException;
import java.util.List;
import java.util.Optional;

/**
 * Created by dean.high on 20/11/2016.
 */
public class Config {
    private final String database;
    private MongoClient client;

    public Config(String database) throws UnknownHostException {
        if (database == null)
            this.database = "admin";
        else
            this.database = database;

        client = new MongoClient();
    }

    public static Optional<Config> client(String database) {
        try {
            Config mongo = new Config(database);
            return Optional.of(mongo);
        } catch (UnknownHostException e) {
            return Optional.empty();
        }
    }

    public void dropDatabase() {
        client.dropDatabase(database);
    }

    public String saveWorkflow(Workflow wf) {
        MongoOperations mongoOps = new MongoTemplate(client, database);
        mongoOps.insert(wf);
        return wf.getId();
    }

    public List<Workflow> getWorkflows() {
        MongoOperations mongoOps = new MongoTemplate(client, database);
        return mongoOps.find(new Query(), Workflow.class);
    }

    public Workflow getWorkflow(String id) {
        MongoOperations mongoOps = new MongoTemplate(client, database);
        return mongoOps.findOne(new Query(where("id").is(id)), Workflow.class);
    }
}
