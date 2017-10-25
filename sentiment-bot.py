from __future__ import print_function
import tweepy
import bot_credentials as bc
from encoder import Model
import utils
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
plt.style.use('ggplot')

__all__ = ["get_tracked_neuron_values_for_a_review"]

def get_tracked_neuron_values_for_a_review(model, review_text):
    feats, tracked_indices_values = model.transform(
        [review_text], track_indices=[2388])
    char_by_char_values_arr = np.array(
        [np.array(vals).flatten() for vals in tracked_indices_values])
    print("average_value =", np.average(char_by_char_values_arr[0]))
    print("all chars value =", char_by_char_values_arr[0])
    return char_by_char_values_arr[0]

def plot_neuron_heatmap(text, values):
    preprocessed_text = utils.preprocess(text)
    n_limit = 64
    num_chars = len(preprocessed_text)
    count = 0
    for i in np.arange(0, len(values), n_limit):
        count += 1
        if i + n_limit > num_chars:
            end_index = num_chars
        else:
            end_index = i+n_limit
    # What the hack is this? count+1? for subplots?
    if count > 1:
        fig, all_subplots = plt.subplots(nrows=count, figsize=(20, 2*count))
    else:
        fig, all_subplots = plt.subplots(nrows=count+1, figsize=(20, 2*count))
    print(all_subplots)
    axis_count = 0
    for i in np.arange(0, len(values), n_limit):
        if i + n_limit > num_chars:
            end_index = num_chars
        else:
            end_index = i+n_limit
        values_limited = values[i:end_index]
        values_reshaped = values_limited.reshape((1, end_index - i))
        chars_to_display = np.array(map(lambda x : str(x), list(preprocessed_text)[i:end_index])).reshape((1,end_index-i))
        data = values_reshaped
        labels = chars_to_display
        sns.heatmap(data, ax=all_subplots[axis_count], annot = labels, fmt = '', annot_kws={"size":15}, vmin=-1, vmax=1, cmap='RdYlGn')
        axis_count += 1
    fig.savefig("all-plots.png")

def status_update_with_media(status_text):
    print("status update with media")
    auth = tweepy.OAuthHandler(
        bc.provide_key("consumer_key"), bc.provide_key("consumer_secret"))
    auth.set_access_token(
        bc.provide_key("access_token"), bc.provide_key("access_token_secret"))
    api = tweepy.API(auth)
    try:
        media_id = api.media_upload("all-plots.png")
        api.update_status(status=status_text, media_ids=[media_id.media_id])
    except Exception as e:
        print("Oops", e)


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api, sentiment_model):
        model = sentiment_model()
        self.api = api
        self.model = model

    def on_status(self, status):
        print(status.text)

    def on_direct_message(self, status):
        dm_text = status.direct_message["text"].lower()
        values = get_tracked_neuron_values_for_a_review(self.model, dm_text)
        plot_neuron_heatmap(dm_text, values)
        status_update_with_media(dm_text)
        return

    def on_error(self, status_code):
        if status_code == 420:
            return False


def send_dm(screen_name, return_text):
    auth = tweepy.OAuthHandler(
        bc.provide_key("consumer_key"), bc.provide_key("consumer_secret"))
    auth.set_access_token(
        bc.provide_key("access_token"), bc.provide_key("access_token_secret"))
    api = tweepy.API(auth)
    try:
        api.send_direct_message(screen_name=screen_name, text=return_text)
    except Exception as e:
        print("Oops", e)


def twitter_stream():
    auth = tweepy.OAuthHandler(
        bc.provide_key("consumer_key"), bc.provide_key("consumer_secret"))
    auth.set_access_token(
        bc.provide_key("access_token"), bc.provide_key("access_token_secret"))
    api = tweepy.API(auth)

    twitter_stream_listener = MyStreamListener(api, Model)
    twitter_stream = tweepy.Stream(
        auth = api.auth, listener=twitter_stream_listener)
    # twitter_stream.filter(track=["python"])
    twitter_stream.userstream()

if __name__ == "__main__":
    twitter_stream()
