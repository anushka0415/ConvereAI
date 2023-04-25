import numpy as np
import tensorflow as tf
import librosa
import matplotlib.pyplot as plt
import pydub

import IPython.display as ipd
import librosa.display
from librosa import feature

import soundfile as sf
import io
import os


class AudioAnalysis:
    def __init__(self):
        self.audio_model_filepath = '/Users/Asus/Documents/fer2013/audio_analysis/harvard.wav'
        self.emotion_intensity_model_filepath = '/Users/Asus/Documents/fer2013/audio_analysis'
        self.audio_model = tf.keras.models.load_model('/Users/Asus/Documents/fer2013/audio_analysis')
        self.emotion_intensity_model = tf.keras.models.load_model('/Users/Asus/Documents/fer2013/audio_analysis/emotiona_intensity')
    
    def read_wav(self, file_path):
        data, sample_rate = librosa.load(file_path)
        if len(data.shape) == 1: 
            left_channel = data[:]  # I assume the left channel is column zero
        elif len(data.shape) == 2: 
            left_channel = data[:, 0]  # I assume the left channel is column zero

        # enable play button in datalab notebook
        aud = ipd.Audio(left_channel, rate=sample_rate)
        return aud, data, sample_rate
    
    def get_spectrogram(self, y, sr):
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        return spectrogram

    def center_crop(self, spec, length):
        spec_size = spec.shape[-1]
        mid = spec_size // 2
        length_mid = length // 2
        start = mid - length_mid 
        end = mid + length_mid
        return spec[:, start:end]

    def create_datasets(self, file_path):
        X = []
        data, sample_rate = librosa.load(file_path)
        spectrogram = self.get_spectrogram(data, sample_rate)
        spectrogram = self.center_crop(spectrogram, 124)
        X.append(spectrogram)
        X = np.array(X)
        return X
    
    def get_audio_analysis(self, audio_analysis):
        audio_categories = []
        total = 0
        sums = {'Neutral': 0, 'Happy': 0, 'Sad': 0, 'Very Expressive': 0}
        for analysis in audio_analysis: 
            index = np.argmax(analysis)
            if index == 0 or index == 1:
                audio_categories.append('Neutral')
                sums['Neutral'] += 1
            elif index == 2:
                audio_categories.append('Happy')
                sums['Happy'] += 1
            elif index == 3: 
                audio_categories.append('Sad')
                sums['Sad'] += 1
            else: 
                audio_categories.append('Very Expressive')
                sums['Very Expressive'] += 1
            total += 1

        percentages = {
            'Neutral': sums['Neutral'] / total, 
            'Happy': sums['Happy'] / total, 
            'Sad': sums['Sad'] / total,
            'Very Expressive': sums['Very Expressive'] / total,
        }
        return audio_categories, percentages

    def get_intensity_analysis(self, emotion_intensity):
        emotions = []
        total = 0
        sums = {0: 0, 1: 0}
        for emotion in emotion_intensity: 
            if emotion[0] >= 0.5:
                emotions.append('Passionate')
                sums[1] += 1
            else:         
                emotions.append('Neutral')
                sums[0] += 1
            total += 1

        percentages = {
            'Passionate': sums[1] / total, 
            'Neutral': sums[0] / total,
        }
        return emotions, percentages

    def predict_emotion(self, file_path):
        X = self.create_datasets(file_path)
        audio_analysis = self.audio_model.predict(X)
        emotion_intensity = self.emotion_intensity_model.predict(X)
        audio_categories, audio_percentages = self.get_audio_analysis(audio_analysis)
        intensity_categories, intensity_percentages = self.get_intensity_analysis(emotion_intensity)
        return {
            'audio_categories': audio_categories,
            'audio_percentages': audio_percentages,
            'intensity_categories': intensity_categories,
            'intensity_percentages': intensity_percentages,
        }


