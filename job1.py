from pyspark import SparkContext, SparkConf

conf = SparkConf().setMaster("spark://192.168.64.16:7077")

sc = SparkContext(conf=conf)

data = range(10)
dist_data = sc.parallelize(data)
print(dist_data.reduce(lambda a, b: a+b))
