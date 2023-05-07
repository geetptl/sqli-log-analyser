import random
import time

words = ['select', 'hello', 'insert', 'data', 'lmao']

stop_after = 10000

with open('web.log', 'w') as f:
    while stop_after > 0:
        random.shuffle(words)
        f.write(' '.join(words[:3]))
        f.write('\n')
        f.flush()
        stop_after-=1