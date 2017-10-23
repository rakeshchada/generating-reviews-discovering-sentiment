from encoder import Model
import utils
import numpy as np
from prompt_toolkit import prompt
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
    print "average_value =", np.average(char_by_char_values_arr[0])
    print "all chars value =", char_by_char_values_arr[0]
    return char_by_char_values_arr[0]


def plot_neuron_heatmap(text, values):
    preprocessed_text = utils.preprocess(text)
    n_limit = 64
    num_chars = len(preprocessed_text)

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
        fig, ax = plt.subplots(figsize=(20,0.5))
        ax = sns.heatmap(data, annot = labels, fmt = '', annot_kws={"size":15}, vmin=-1, vmax=1, cmap='RdYlGn')
        fig.savefig("output-fig.png")
        ax.savefig("output.png")

if __name__ == "__main__":
    model = Model()
    while (True):
        input_text = prompt(u"What's on your mind? ")
        values = get_tracked_neuron_values_for_a_review(model, input_text)
        y_n = prompt(u"Would you like to plot the heatmap? ")
        if y_n[0].lower() == "y":
            plot_neuron_heatmap(input_text, values)
        else:
            print "Not plotting"

