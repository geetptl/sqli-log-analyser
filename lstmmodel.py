import torch
import torch.nn as nn
import numpy as np

class LSTM1(nn.Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers):
        super(LSTM1, self).__init__()
        self.num_classes = num_classes #number of classes
        self.num_layers = num_layers #number of layers
        self.input_size = input_size #input size
        self.hidden_size = hidden_size #hidden state

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                          num_layers=num_layers, batch_first=True,bidirectional=False) #lstm
        self.fc_1 =  nn.Linear(hidden_size, 128) #fully connected 1
        self.fc = nn.Linear(128, num_classes) #fully connected last layer

        self.relu = nn.ReLU()

    def forward(self,x):
        h_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size) #hidden state
        c_0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size) #internal state
        # Propagate input through LSTM
        output, (hn, cn) = self.lstm(x, (h_0, c_0)) #lstm with input, hidden, and internal state
        hn = hn.view(-1, self.hidden_size) #reshaping the data for Dense layer next
        out = self.relu(hn)
        out = self.fc_1(out) #first Dense
        out = self.relu(out) #relu
        out = self.fc(out) #Final Output
        return out

def load_lstm():
    print('loading pre-trained lstm...')
    save_path = 'models/lstm.pt'
    model_state_dict = torch.load(save_path)
    model = LSTM1(1,300,100,1)
    model.load_state_dict(model_state_dict)
    print('pre-trained lstm ready...')
    return model

def load_glove():
    print('loading glove embeddings...')
    glove_file = 'models/glove.840B.300d.txt'
    glove_embeddings = {}
    with open(glove_file, 'r', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            if len(values) != 301:
                continue
            word = values[0]
            vector = np.asarray(values[1:], dtype='float32')
            glove_embeddings[word] = vector
    print('glove embeddings ready...')
    return glove_embeddings

def embed_fn(line, glove_embeddings):
    weighted_sum = np.zeros((300,)) #embedding of whole sentence
    count = 0
    for word in line:
        count += 1
        embedding = glove_embeddings.get(word, np.zeros(300,))
        weighted_sum += embedding
    if count > 0:
        weighted_sum = (weighted_sum / count)
    return torch.tensor(weighted_sum).unsqueeze(0)

def apply_model(line, model, glove_embeddings):
    outputs = model(embed_fn(line, glove_embeddings).unsqueeze(1).to(torch.float))
    outputs = nn.functional.sigmoid(outputs) # Apply sigmoid activation so that values are between 0 and 1
    predicted = torch.round(outputs).int()
    return predicted.item()
