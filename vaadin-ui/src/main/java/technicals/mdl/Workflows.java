package technicals.mdl;

import com.google.common.collect.Lists;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Id;

import java.util.Collection;
import java.util.Date;

/**
 * Created by dean.high on 19/11/2016.
 */
public class Workflows {
        @Id private ObjectId id;
        private String name;
        private Date create_date;
        private Collection<Measure> measures = Lists.newArrayList();

        public Workflows() {}

        public ObjectId getId() {
                return id;
        }

        public void setId(ObjectId id) {
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
