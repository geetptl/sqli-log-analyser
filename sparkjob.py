def countpositives(lines, model, sc):
    lines_ = sc.parallelize(lines)
    counts = lines_.map(lambda x: (model(x), 1)).reduceByKey(lambda a, b: a + b)
    counts = counts.collect()
    return dict(counts)
