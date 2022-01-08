# "The Onion" tweet generation

By Louise MERLAUD and Sebastien MILLET


Objective : The Onion is parodic news website, aimed at creating funny news stories. On its twitter page, the Onion gives the headlines of its articles with a link to its page. Each headline is thus freely available and a humorous take on the news.
Given the parodic nature of their headlines, we want to attempt to generate new headlines by building a model that can automatically generate a tweet given the first word. 

To do so, we have obtained all the tweets from @TheOnion (around 75,000 tweets) but only use 33% of it for performance.

Our approach will use a Bidirectional Long-Short Term Memory model in order to generate the headlines.

## Word preprocessing 

### Cleaning and tokenization
We first import all the tweets in a Pandas and clean them by removing special characters. We then proceed to a tokenization of the sentences by establishing a dictionnary for the characters, and its inverse dictionnary for the indexes generated. This will allow us to go from text to vectors and from vectors to text.

### Sentence creation

Our aim is to predict the following characters after a given to create a headline. Therefore, we need to train the model to predict what the next character is. We create sentences of length 50 characters, and then go through the entire dataset step by step using a sliding filter. We thus give N characters and want to predict the N+1 character. 



## Model : LSTM



![alt text](https://github.com/louisemld/theonion-tweet-generation/blob/main/img/LSTM.png?raw=true)


![alt text](https://github.com/louisemld/theonion-tweet-generation/blob/main/img/LSTM.png?raw=true)

