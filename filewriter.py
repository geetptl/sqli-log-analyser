import random
import time
import pandas as pd

df = pd.read_csv('SQLiV3.csv')
df.info()
df.dropna(subset=['Sentence'], inplace=True)
df.info()
sentences = [str(i) for i in df['Sentence']]
random.shuffle(sentences)
index = 0
print(len(sentences))

stop_after = 10000000

with open('web.log', 'w') as f:
    while stop_after > 0:
        f.write(sentences[index])
        f.write('\n')
        f.flush()
        stop_after-=1
        index+=1
        if index==len(sentences):
            index=0
            random.shuffle(sentences)