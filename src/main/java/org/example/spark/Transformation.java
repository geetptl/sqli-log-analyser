package org.example.spark;

import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;

public class Transformation {
    public long count(Dataset<Row> dataset) {
        return dataset.count();
    }
}
