package technicals.mdl;

import com.google.common.collect.Lists;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;

import java.util.Collection;
import java.util.Date;

/**
 * Created by dean.high on 20/11/2016.
 */
public class Workflow {
    private String id;
    private String name;
    private Date create_date = new Date();

    public Collection<Measure> getMeasures() {
        return measures;
    }

    public void setMeasures(Collection<Measure> measures) {
        this.measures = measures;
    }

    private Collection<Measure> measures = Lists.newArrayList();

    public Workflow(String name) {
        this.name = name;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Date getCreate_date() {
        return create_date;
    }

    public void setCreate_date(Date create_date) {
        this.create_date = create_date;
    }
}
