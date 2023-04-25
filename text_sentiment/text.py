import tensorflow as tf
import numpy as np
import gensim.downloader as api
import string

class TEDTalkAnalyzer:
    def __init__(self, model_filepath='/Users/Asus/Documents/fer2013/text_sentiment', wv_name='word2vec-google-news-300'):
        self.model_filepath = model_filepath
        self.wv_name = wv_name
        self.wv = api.load(self.wv_name)
        self.model = tf.keras.models.load_model(self.model_filepath)
        self.cols = ['Beautiful', 'Confusing', 'Courageous', 'Funny', 'Informative', 'Ingenious', 'Inspiring', 'Longwinded', 'Unconvincing', 'Fascinating', 'Jaw-dropping', 'Persuasive', 'OK', 'Obnoxious']
        
    def clean(self, transcript):
        cleaned = transcript.translate(str.maketrans('', '', string.punctuation))
        cleaned = cleaned.replace('Laughter', '')
        cleaned = cleaned.replace('Applause', '')
        cleaned = cleaned.replace('—', '')
        return cleaned.lower()

    def create_embedding(self, transcript):
        X = []
        found_words = []
        transcript = self.clean(transcript) 
        words = transcript.split()
        for word in words: 
            try:
                found_words.append(self.wv[word])
            except: 
                continue
        embedding = np.asarray(found_words)
        mean = np.mean(embedding, axis=0)
        mean = mean.tolist()
        if type(mean) == list: 
            X.append(mean)
        X = np.array(X)
        return X

    def perform_analysis(self, transcript):
        embedding = self.create_embedding(transcript)
        pred = self.model.predict(embedding)[0]
        ted_dict = {}
        for val, col in zip(pred, self.cols):
            ted_dict[col] = val
        return ted_dict # can be converted to a JSON


