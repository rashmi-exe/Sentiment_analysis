import tweepy
import requests
import re
from collections import defaultdict
from textblob import TextBlob

# Set up Twitter API credentials
consumer_key = 'JvmVjhfeNYM9tZ4s3Rn1hd7R2'
consumer_secret = '4IdQJUglKL3QYzEmNNV6jXjgW9OnRVyLDVlqKvif8YbCuLi0Fc'
access_token = '4648876814-ImrJngHnwoJWA0Gmcpp8JjoU4ThQKEpQcOYM7vc'
access_token_secret = 'P126XSdK5VqVOklko3d4mUJ3mYUiNsK2fdLjuEyRj0Rq2'

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Define emotions and initialize counters
emotions = ["happy", "sad", "angry"]
emotion_counts = defaultdict(lambda: defaultdict(int))

# Define a function to clean tweet text


def clean_tweet_text(text):
    # Remove URLs, mentions, and special characters
    text = re.sub(r'http\S+|@\w+|#\w+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


# Fetch user's timeline tweets
user_timeline = api.user_timeline(screen_name='twitterusername', count=100)

# Iterate through tweets
for tweet in user_timeline:
    # Clean and tokenize tweet text
    cleaned_text = clean_tweet_text(tweet.text)
    words = cleaned_text.split()

    # Analyze sentiment using TextBlob (you can use a more advanced sentiment analysis tool)
    sentiment = TextBlob(cleaned_text).sentiment.polarity

    # Classify tweet into an emotion category
    if sentiment > 0.2:
        emotion = "happy"
    elif sentiment < -0.2:
        emotion = "sad"
    else:
        emotion = "angry"

    # Count words and hashtags associated with the emotion
    for word in words:
        if word.startswith('#'):
            emotion_counts[emotion]["hashtags"][word] += 1
        else:
            emotion_counts[emotion]["words"][word] += 1

# Print the results
for emotion in emotions:
    print(f"Emotion: {emotion}")
    print("Most Frequent Words:")
    for word, count in sorted(emotion_counts[emotion]["words"].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{word}: {count}")
    print("Most Frequent Hashtags:")
    for hashtag, count in sorted(emotion_counts[emotion]["hashtags"].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"{hashtag}: {count}")
    print("\n")
