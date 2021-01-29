package technicals.mdl;

import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;

/**
 * Created by dean.high on 20/11/2016.
 */
public class Input {
    @Id
    private ObjectId id;

    public ObjectId getId() {
        return id;
    }

    public void setId(ObjectId id) {
        this.id = id;
    }
}
