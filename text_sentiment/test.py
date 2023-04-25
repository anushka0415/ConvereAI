import tensorflow as tf
import numpy as np
import gensim.downloader as api
import string
transcript="I want to share with you a message of inspiration and encouragement. Life can be challenging at times, and we all face obstacles and setbacks on our journey. But I want you to know that you are capable of overcoming these challenges and achieving your dreams.You have the strength and the resilience to face any adversity that comes your way. You have the power to transform your life and make a positive impact on the world around you. It may not be easy, but with hard work, dedication, and perseverance, you can accomplish anything you set your mind to."
    
def clean(transcript): 
    cleaned = transcript.translate(str.maketrans('', '', string.punctuation))
    
    
    cleaned = cleaned.replace('Laughter', '')
    cleaned = cleaned.replace('Applause', '')

    cleaned = cleaned.replace('—', '')

    return cleaned.lower()
    
    
def load_wv():
    wv = api.load('word2vec-google-news-300')
    return wv

def create_embedding(transcript, wv):

    X = []
    found_words = []
    transcript = clean(transcript) 
    
    print(transcript)
    words = transcript.split()
    for word in words: 
        try:
            found_words.append(wv[word])
        except: 
            continue
            
    embedding = np.asarray(found_words)
    mean = np.mean(embedding, axis=0)
    mean = mean.tolist()

    if type(mean) == list: 
        X.append(mean)

    X = np.array(X)
    return X


def perform_analysis(transcript):
    wv = load_wv()
    embedding = create_embedding(transcript, wv)
    
    model_filepath = '/Users/Asus/Documents/fer2013/text_sentiment'
    model = tf.keras.models.load_model(model_filepath)
    
    pred = model.predict(embedding)[0]
    cols = ['Beautiful', 'Confusing', 'Courageous', 'Funny', 'Informative', 'Ingenious', 'Inspiring', 'Longwinded', 'Unconvincing', 'Fascinating', 'Jaw-dropping', 'Persuasive', 'OK', 'Obnoxious']
    
    ted_dict = {}
    for val, col in zip(pred, cols):
        ted_dict[col] = val
    return ted_dict # can be converted to a JSON
ted_dict = perform_analysis(transcript)
print(ted_dict)
    
    
    
    