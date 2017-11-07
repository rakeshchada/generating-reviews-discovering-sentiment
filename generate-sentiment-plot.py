from encoder import Model
import utils
import numpy as np
from prompt_toolkit import prompt
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
plt.style.use('ggplot')

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
    axes = []
    count = 0
    for i in np.arange(0, len(values), n_limit):
        count += 1
        if i + n_limit > num_chars:
            end_index = num_chars
        else:
            end_index = i+n_limit
    print "this is count", count
    fig, all_subplots = plt.subplots(nrows=count+1, figsize=(20, 2*count))
    print all_subplots, len(all_subplots)
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

if __name__ == "__main__":
    model = Model()
    while (True):
        input_text = prompt(u"What's on your mind? ")
        values = get_tracked_neuron_values_for_a_review(model, input_text)
        # input_text = "I am mad and sad at this event. Totally happy, didn't expect my life to turn in to this blunder."

        # values = np.array([
        #     0.01258736, 0.03544582, 0.04874653, 0.08836347, 0.09750156, 0.08503999,
        #     0.08408628, 0.08765027, 0.09645839, 0.08067882, -0.02273844, -0.01028589,
        #     -0.02871433, -0.00210926, -0.06486075, -0.02683137, -0.0249781,-0.02410605,
        #     -0.09755349, -0.07649951, -0.07852796, -0.07936801, -0.06561398, 0.07342028,
        #     0.07330813, 0.14010248, 0.03502839, 0.04184622, 0.02991394, 0.03446922,
        #     0.01806017, 0.02680984, -0.08430012, -0.17344463, -0.13404076, -0.13856064,
        #     -0.14816357, -0.14658745, -0.14931433, -0.14563316, -0.04043929, -0.03034576,
        #     0.00164839, 0.00251725, -0.00074493, 0.00167437, 0.04926455, 0.26916873,
        #     0.39678487, 0.39279276, 0.38606045, 0.39671212, 0.32895672, 0.34413135,
        #     0.33056283, 0.32195505, 0.29699713, 0.32991606, 0.33268163, 0.5773946,
        #     0.57362473, 0.57258505, 0.5398227, 0.53829151, 0.56116217, 0.57751662,
        #     0.57861549, 0.57841378, 0.58086473, 0.56623524, 0.55707943, 0.55603528,
        #     0.55520421, 0.55326682, 0.55508786, 0.56334972, 0.55514133, 0.58299601,
        #     0.57842195, 0.57965308, 0.58167124, 0.57191753, 0.57367766, 0.56776673,
        #     0.56171262, 0.5657258, 0.59859776, 0.59982187, 0.61652035, 0.60741204,
        #     0.6008631, 0.63727963, 0.63797879, 0.64072317, 0.60398412, 0.60691214,
        #     0.58915466, 0.31660399, 0.29023501, 0.29023501, 0.29023501, 0.29023501,
        #     0.29023501, 0.29023501, 0.29023501, 0.29023501, 0.29023501, 0.29023501,
        #     0.29023501, 0.29023501, 0.29023501, 0.29023501, 0.29023501, 0.29023501,
        #     0.29023501, 0.29023501, 0.29023501, 0.29023501, 0.29023501, 0.29023501,
        #     0.29023501, 0.29023501, 0.29023501, 0.29023501, 0.29023501, 0.29023501,
        #     0.29023501, 0.29023501])

        print type(values), len(values)
        print "Plotted"
        y_n = prompt(u"Would you like to plot the heatmap? ")
        if y_n[0].lower() == "y":
            plot_neuron_heatmap(input_text, values)
        else:
            print "Not plotting"

