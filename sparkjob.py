def countpositives(lines, apply_model, lstm_model, glove_embeddings, sc):
    print(1)
    lines_ = sc.parallelize(lines)
    print(2)
    counts = lines_.map(lambda x: (apply_model(x, lstm_model, glove_embeddings), 1)).reduceByKey(lambda a, b: a + b)
    print(3)
    counts = counts.collect()
    print(4)
    return dict(counts)
