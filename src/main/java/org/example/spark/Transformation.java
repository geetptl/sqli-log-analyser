package org.example;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;

public class Transformations {
    public long count(Dataset<Row> dataset) {
        return dataset.count();
    }
}
