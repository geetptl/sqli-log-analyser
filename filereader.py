import subprocess
import random
import time
import datetime
import sparktorch
from pyspark import SparkConf, SparkContext
from sparkjob import countpositives
import re

conf = SparkConf()
        # .setAll([('spark.executor.memory', '8g'), ('spark.executor.cores', '3'), ('spark.cores.max', '3'), ('spark.driver.memory','8g')])
sc = SparkContext(conf=conf)

FILE_SIZES = [1024]*6 + [2**i for i in range(11, 22)]
size_ind = 0

pattern = r"(\s*([\0\b\'\"\n\r\t\%\_\\]*\s*(((select\s*.+\s*from\s*.+)|(insert\s*.+\s*into\s*.+)|(update\s*.+\s*set\s*.+)|(delete\s*.+\s*from\s*.+)|(drop\s*.+)|(truncate\s*.+)|(alter\s*.+)|(exec\s*.+)|(\s*(all|any|not|and|between|in|like|or|some|contains|containsall|containskey)\s*.+[\=\>\<=\!\~]+.+)|(let\s+.+[\=]\s*.*)|(begin\s*.*\s*end)|(\s*[\/\*]+\s*.*\s*[\*\/]+)|(\s*(\-\-)\s*.*\s+)|(\s*(contains|containsall|containskey)\s+.*)))(\s*[\;]\s*)*)+)"

def model(line):
    return 1 if re.search(pattern, line) else 0    

def test_models(current, model, sc):
    t1 = time.time()
    normal = sum(list(map(model, current)))
    t1 = time.time() - t1

    t0 = time.time()
    positives = countpositives(current, model, sc)
    t0 = time.time() - t0
    total = positives.get(0, 0) + positives.get(1, 0)
    percentage = positives.get(1, 0) * 100 / total
    return t0, t1

output = []
with subprocess.Popen(['tail', '-F', 'web.log'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
    current = []
    while True:
        line = proc.stdout.readline().decode().strip()
        if not line:
            break
        current.append(line)
        if len(current) > FILE_SIZES[size_ind]:
            t0, t1 = test_models(current, model, sc)
            output.append((FILE_SIZES[size_ind], t0, t1))
            print(output[-1])
            current.clear()
            size_ind += 1
