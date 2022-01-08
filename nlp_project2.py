# -*- coding: utf-8 -*-
"""NLP_Project2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q85xo3S7cFiEniKuoUKAseKXu6W0BYQk

#NLP Project 
##Louise MERLAUD - Sebastien MILLET

### Text generation of tweets from The Onion
"""

import numpy as np
 import pandas as pd
 import re
 import sys
 import random
 import matplotlib.pyplot as plt
 
 from keras.models import Sequential
 from keras.layers import Dense
 from keras.layers import LSTM
 from keras.layers import Dropout
 from keras.models import Model
 from keras.layers import Input, Activation, Embedding, LSTM, Dense, Dropout, Bidirectional
 from tensorflow.keras.optimizers import RMSprop
 from tensorflow.keras.optimizers import Adam
 from keras.callbacks import LambdaCallback
 from keras.preprocessing.text import Tokenizer
 from tensorflow.keras.utils import to_categorical
 from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import optimizers

"""# Import the tweets


"""

df = pd.read_csv("/content/tweets.csv")

df

"""Only keep the first 25,000 tweets"""

df = df.loc[0:25000]

df = df[['Text']]

"""# Clean the text"""

def clean(text):

    #     remove urls
    text = re.sub(r'http\S+', " ", text)

    #     remove mentions
    text = re.sub(r'@\w+',' ',text)

    #     remove hastags
    text = re.sub(r'#\w+', ' ', text)

    #     remove html tags
    text = re.sub(r'<.*?>',' ', text)
        
    return text

text=df['Text'].apply(lambda x:x.lower())
text= text.apply(clean)
text = text.apply(lambda x: x.encode('ascii', 'ignore').decode('ascii'))

text

"""# Tokenize the text

Create a dictionnary to associate a number to each character

Create the reverse dictionnary to go from numbers to characters
"""

chars = sorted(list(set(''.join(text))))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

"""Number of different characters"""

len(chars)

"""One of the dictionnaries"""

char_indices

"""# Create sequences of text"""

maxlen = 50
sentences = []
next_chars = []
for x in text:
  for i in range(0,len(x)-maxlen):
    sentences.append(x[i:i+maxlen])
    next_chars.append(x[i+maxlen])
len(sentences)

"""Example of 3 sequences, shift by 1 character"""

for i in range(3):
  print(sentences[i], '      ', next_chars[i])

"""We will use the sentences as input and the next character as the output"""

x=np.zeros((len(sentences),maxlen,len(chars)),dtype=np.bool)
y=np.zeros((len(sentences),len(chars)),dtype=np.bool)

x.shape

"""821650 sentences

50 characters maximum in one sentence (length of one sentence)

59 characters in total

59 matrixes of dim 821650x50
"""

y.shape

"""1 matrix of dim 821650x59

1 if its the next character of the given sentence

for each line, there is the value 1 for the next character in the sentence
"""

for i, sentence in enumerate(sentences):
  for t, char in enumerate(sentence):
    x[i,t,char_indices[char]]=1
  y[i,char_indices[next_chars[i]]]=1

"""for one matrix (which corresponds to one character), there is a value 1 if this character is in a given sentence at a given place

# Bidirectional LSTM

## Build model
"""

def build_lstm_model(length, characters):

    inp = Input(shape=(length,characters))

    # Build a Bi-LSTM layer with 128 dimensions
    x=Bidirectional(LSTM(128))(inp)

    # Create the Dense output layer with sigmoid activation function
    out = Dense(len(chars),activation="softmax")(x)

    model = Model(inputs=inp, outputs=out)
    opt = optimizers.Adam(lr=0.005)
    model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

    return model

lstm=build_lstm_model(maxlen, len(chars))

"""## Summary of model"""

lstm.summary()

"""## Fit the model"""

history=lstm.fit(x,y,batch_size=2048, epochs=5, verbose=1, validation_split=0.1)

def plot_history(hist):
  plt.plot(hist.history['loss'], label='train')
  plt.plot(hist.history['val_loss'], label='val')
  plt.legend()
  plt.ylim((0,2))
  plt.title('Loss evolution')
  plt.show()
  plt.plot(hist.history['accuracy'], label='train')
  plt.plot(hist.history['val_accuracy'], label='val')
  plt.legend()
  plt.ylim((0,1))
  plt.title('Accuracy evolution')
  plt.show()

plot_history(history)

"""# Predict new tweets"""

sentence=input()
for i in range(70):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.

lstm.predict(x_pred, verbose=0)

def generate_text(model, start_string):

    num_generate = 50
    x=np.zeros((len(sentences),maxlen,len(chars)),dtype=np.bool)
    for t, char in enumerate(start_string):
     x[0,t,char_indices[char]]=1

    text_generated = []

    temperature = 0.1

    for i in range(num_generate):
        predictions = model.predict(x)

        predictions = predictions / temperature
        predicted_id = np.argmax(predictions)

        x = indices_char[predicted_id]
        text_generated.append(x)

    return (start_string + ''.join(text_generated))

generate_text(lstm, 'covid')

sentence=input()
generated=''
generated += sentence

x=np.zeros((len(sentences),maxlen,len(chars)),dtype=np.bool)
for t, char in enumerate(sentence):
  x[0,t,char_indices[char]]=1


for i in range(50):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(generated):
            x_pred[0, t, char_indices[char]] = 1.

        preds = lstm.predict(x_pred, verbose=0)
        next_index = np.argmax(preds)
        next_char = indices_char[next_index]

        generated += next_char
        print(next_index)
        print(next_char)
        print(generated)

maxlen

def generate_w_seed(sentence):
    sentence = sentence[0:maxlen]
    generated = ''
    generated += sentence

    for i in range(30):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(sentence):
            x_pred[0, t, char_indices[char]] = 1.

        preds = lstm.predict(x_pred, verbose=0)
        next_index = np.argmax(preds)
        next_char = indices_char[next_index]

        generated += next_char
        sentence = sentence + next_char
    print(sentence)

generate_w_seed('help')