prerprocessing.py is the code for preprocessing the data (it may hvae some bugs) the preprocessed data.zip is the result of preprocessing 
the dataset we used is kaggle based its over 25mb so i will share the link please download it from kaggle https://www.kaggle.com/datasets/carlosgdcj/genius-song-lyrics-with-language-information/data 
First run the *preprocessing.py* file in kaggle notebook(or any other environment). This removes the unwanted texts(NLP techniques like lemmatization and tokenization).
Then run the *emotionallabeling.py*.
Run any of the 3 models: *BERT.py*, *T5.py*, *gpt.py*. Each of these models will ask for a seed word and emotion(like joy, love, anger, etc..).                          
