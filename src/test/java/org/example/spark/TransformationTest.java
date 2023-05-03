package org.example.spark;

import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.RowFactory;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.types.StructField;
import org.apache.spark.sql.types.StructType;
import org.example.SparkTestSession;
import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.assertEquals;

public class TransformationTest {
    @Test
    public void counter() {
        SparkSession spark = SparkTestSession.get();
        List<String[]> stringAsList = new ArrayList<>();
        stringAsList.add(new String[]{"bar1.1", "bar2.1"});
        stringAsList.add(new String[]{"bar1.2", "bar2.2"});

        JavaSparkContext sparkContext = new JavaSparkContext(spark.sparkContext());

        JavaRDD<Row> rowRDD = sparkContext.parallelize(stringAsList).map(RowFactory::create);

        StructType schema = DataTypes.createStructType(new StructField[]{DataTypes.createStructField("foe1", DataTypes.StringType, false), DataTypes.createStructField("foe2", DataTypes.StringType, false)});

        Dataset<Row> df = spark.sqlContext().createDataFrame(rowRDD, schema).toDF();

        Transformation transformation = new Transformation();
        long result = transformation.count(df);
        assertEquals(2, result);
    }
}
