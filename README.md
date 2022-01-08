# "The Onion" tweet generation

By Louise MERLAUD and Sebastien MILLET


Objective : The Onion is parodic news website, aimed at creating funny news stories. On its twitter page, the Onion gives the headlines of its articles with a link to its page. Each headline is thus freely available and a humorous take on the news.
Given the parodic nature of their headlines, we want to attempt to generate new headlines by building a model that can automatically generate a tweet given the first word. 

To do so, we have obtained all the tweets from @TheOnion (around 75,000 tweets) but only use 33% of it for performance.

Our approach will use a Bidirectional Long-Short Term Memory model in order to generate the headlines.

## The Onion Tweets

@TheOnion tweets are usually short headlines, with a humoristic spin.
Here is an example of one we use : 

"‘You’re Going To Want To Take 3 Quick Lefts’ Says Passenger Expertly Hiding That He Fucked Up Directions"


## Word preprocessing 

### Cleaning and tokenization
We first import all the tweets in a Pandas and clean them by removing special characters. We then proceed to a tokenization of the sentences by establishing a dictionnary for the characters, and its inverse dictionnary for the indexes generated. This will allow us to go from text to vectors and from vectors to text.

Here is our dictionnary for the characters we have
METTRE SCREEN DICTIONNARY OU COPIER COLLER


### Sentence creation

Our aim is to predict the following characters after a given to create a headline. Therefore, we need to train the model to predict what the next character is. We create sentences of length 50 characters, and then go through the entire dataset step by step using a sliding filter. We thus give N characters and want to predict the N+1 character. 
For the example we gave above, for a 10 character sentence, the first sentence would be : "you re goi". With a step of 1, the next sentence would thus be : "ou re goin", adding the next character "n" and removing the first "y". By decomposing the text in this way, the model will be able to train itself to predict the next character. 


## Model : LSTM

Long Short Term Memory is a type of Recurrent Neural Network, avoiding the long-term dependencies problem. Instead of having one single neural network layer, we have 4 of them, which interact between each other. 
![alt text](https://github.com/louisemld/theonion-tweet-generation/blob/main/img/LSTM.png?raw=true)


The cell state is the horizontal line running through the top of the diagram. The LSTM model can add or remove information to this line, and is regulated by gates. The gate has the ability to decide which component is important or not to let through. 
We have 3 types of gates : Forget, Input and Output.

- The first one indicates how much of the past to remember
![alt text](https://github.com/louisemld/theonion-tweet-generation/blob/main/img/Forget.png?raw=true)

- The second one tells us how much to include of the input in the model
![alt text](https://github.com/louisemld/theonion-tweet-generation/blob/main/img/Input.png?raw=true)

- The last one gives us the part of the cell output to keep
![alt text](https://github.com/louisemld/theonion-tweet-generation/blob/main/img/Output.png?raw=true)


We decided to use Bidirectional LSTM. It is an additional step to better this kind of model by processing the data in both directions using separate hidden layers. This helps us predict the next character using past and future context, bettering our prediction. 


![alt text](https://github.com/louisemld/theonion-tweet-generation/blob/main/img/Bidirectional_LSTM.png?raw=true)


## Results

