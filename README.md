## ConvereAI

**The Grammarly of soft skills!**

**Problem statement:**

Imagine presenting a project when your anxiousness, lack of preparation, and fear of public speaking hit 
you all at once. Social phobia, also called social anxiety disorder, is the third most common mental 
health disorder after depression and substance abuse, affecting as many as 10 million Indians.
In India, there is a growing concern about the lack of soft skills among students. While the education 
system in India emphasizes academic excellence, there is often a neglect of the development of soft 
skills. As a result, many Indian students struggle to communicate effectively, work in teams, and manage 
their time efficiently.

**Solution:**

Converse AI is a full-stack web application that determines how well you presented when you recorded 
yourself giving a speech on the app. It examines your presentation over five research-based metrics and 
scores you on each. It looks for whether you have used filler words, gesture noise, gesture frequency, 
pace, and the consistency of your speech overall. It is intended to be used as a tool for users to prepare 
for a real-life presentation that they might have to deliver.

**Features:**

One major component of our application is the set of algorithms, both classical and machine learning, that use either the audio, transcript, or video (next step) as training modalities to compute useful presentation metrics.

Our approach was to systematically research metrics that are indicative of high-quality presenters, and design a means to compute each of them algorithmically. The metrics can be broken down into the following categories: rating classification, passion, brevity, cadence, diction, diversity of language, and engagement. Below, we break down how we calculate each metric.

*Rating Classification: TED Talk Model*

For most of us, when we think of speeches, TED Talks are our ‘go-to’.

Our approach utilizes the voluminous, information rich TED Talk Dataset from Kaggle containing transcripts from past speeches in order to implement a multi-label classification algorithm to process transcripts and output ratings such as 'Beautiful', 'Confusing', 'Courageous', 'Funny', 'Informative', 'Ingenious', 'Inspiring', 'Longwinded', 'Unconvincing', 'Fascinating', 'Jaw-dropping', 'Persuasive', 'OK', 'Obnoxious'.

*The pipeline is defined as such:*

For each transcript, use the Word2Vec algorithm (pre-trained model from gensim), to convert each word in the transcript to a 300-feature vector .
We average these vectors in the axis of the number of words in order to get one 300-vector to represent the entire transcript.
We parse the dataset to obtain clean rating labels for each of our transcripts. We set the top-4 ratings as one, and the rest are zero.
Last but not least, we train the model using this engineered dataset, and evaluate on test data to obtain a top-k categorical accuracy of ~0.85.
*Passion/Urgency: Are you passionate about your words, or are you putting your audience to sleep?

For this category, we develop algorithms to analyze each of the data modalities.


We also train a convolutional neural network to classify snippets of audio as either neutral, or passionate/expressive. We used the Ryerson Audio-Visual Database of Emotional Speech and Song (RAVDESS) dataset from Kaggle to classify the emotional intensity, or the lack thereof (monotony) of audio files by transforming audio wav files into spectrograms, which are then used to train two CNNs.

*Facial Emotion Recognition*
Lastly, we used the facial expression dataset on Kaggle(FER 2013) to train a CNN to classify neutral or expressive facial expressions. The algorithm is applied to the user’s mp4 file to help them improve their expression of enthusiasm for their speeches.

*Brevity:*

The question we try to answer here is, “How many unnecessary filler words or phrases are you using?”

We compute a metric for brevity by creating two master lists containing sets of phrases or words that are commonly known in the english language as filler words. Using these lists, we iterate through the AI-generated transcript, and count the number of usages of each phrase.

*Cadence: How fast are you speaking?*

We compute cadence by measuring the words / minute. Using the outputs from the Google Cloud Speech-to-Text API (abv. As GCST), we calculate both the number of words, and manually compute the duration of the audio file using GCST’s timestamps.

We also calculate the number of pauses throughout the speech based on the per-word time outputs from the GCST. On average, we speak one word in 0.5 seconds. We compute the amount of time it takes for the user to say one word. If it’s greater than our predefined threshold, we classify it as a pause.

*Gaze Tracking Module:*
To track your eyes and engagement with the audience.


