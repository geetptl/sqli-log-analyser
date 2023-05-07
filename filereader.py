import subprocess
import random
import time
import datetime
import sparktorch
from pyspark import SparkConf, SparkContext
from pyspark.serializers import MarshalSerializer
from sparkjob import countpositives
from lstmmodel import load_lstm, load_glove, apply_model
import sys

conf = SparkConf().setAll([('spark.executor.memory', '8g'), ('spark.executor.cores', '3'), ('spark.cores.max', '3'), ('spark.driver.memory','8g')])
sc = SparkContext(conf=conf, serializer = MarshalSerializer())

# spark = SparkSession.builder.appName("PySparkApp").getOrCreate()

## Handle cold start

FILE_SIZES = [10]*6 + [2**i for i in range(11, 22)]
size_ind = 0

output = []

lstm_model = load_lstm()
glove_embeddings = load_glove()

# def model(line):
#     return 1 if 'select' in line else 0

def test_models(current, model, sc):
    print(sc.getConf().getAll())
    print(sys.getsizeof(glove_embeddings))
    print(sys.getsizeof(lstm_model))

    print(f"\trunning normally @ {datetime.datetime.fromtimestamp(time.time())}")
    t1 = time.time()
    normal = sum(list(map(apply_model, current, [lstm_model]*len(current), [glove_embeddings]*len(current))))
    print(f"\tnormal result : {normal}")
    t1 = time.time() - t1

    print(f"\trunning on spark @ {datetime.datetime.fromtimestamp(time.time())}")
    t0 = time.time()
    positives = countpositives(current, apply_model, lstm_model, glove_embeddings, sc)
    t0 = time.time() - t0
    total = positives.get(0, 0) + positives.get(1, 0)
    percentage = positives.get(1, 0) * 100 / total
    return t0, t1

with subprocess.Popen(['tail', '-F', 'web.log'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
    current = []
    while True:
        line = proc.stdout.readline().decode().strip()
        if not line:
            break
        current.append(line)
        if len(current) > FILE_SIZES[size_ind]:
            t0, t1 = test_models(current, lstm_model, sc)
            output.append((FILE_SIZES[size_ind], t0, t1))
            print(output[-1])
            current.clear()
            size_ind += 1
