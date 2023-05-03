package org.example;

import org.apache.spark.sql.SparkSession;

public class SparkTestSession {
    private static SparkSession sparkSession;

    static {
        sparkSession = SparkSession.builder().appName("sqli-log-analyser-test").master("local[*]").getOrCreate();
    }

    public static SparkSession get() {
        if (sparkSession == null) {
            sparkSession = SparkSession.builder().appName("sqli-log-analyser-test").master("local[*]").getOrCreate();
        }
        return sparkSession;
    }
}
