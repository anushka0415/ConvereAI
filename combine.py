from audio import AudioAnalysis
from eye import EyeTracker
from text import TEDTalkAnalyzer

ak = AudioAnalysis()
print(ak.predict_emotion(r'/Users/Asus/Documents/fer2013/audio_analysis/harvard.wav'))
tracker = EyeTracker("eye tracking/video.mp4")
frames, images_eyes = tracker.track_eyes()
print(images_eyes)

analyzer = TEDTalkAnalyzer()
transcript="I want to share with you a message of inspiration and encouragement. Life can be challenging at times, and we all face obstacles and setbacks on our journey. But I want you to know that you are capable of overcoming these challenges and achieving your dreams.You have the strength and the resilience to face any adversity that comes your way. You have the power to transform your life and make a positive impact on the world around you. It may not be easy, but with hard work, dedication, and perseverance, you can accomplish anything you set your mind to."

ted_dict = analyzer.perform_analysis(transcript)
print(ted_dict)
