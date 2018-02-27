import pickle
import matplotlib.pyplot as plt
from matplotlib import rc

files = ['2008-07', '2008-11', '2009-03', '2009-07', '2009-11', '2010-03', 
         '2010-07', '2011-03', '2011-07', '2011-11', '2012-03', '2012-07', 
         '2012-11']
cat_list = ['pics', 'funny', 'offbeat', 'reddit.com', 'WTF', 'gifs', 
            'atheism', 'gaming']
col_list = ['#ef4f94', '#914fef', '#4f84ef', '#4fe7ef', '#b1ef4f', '#efdc4f',
            '#ef9c4f', '#ef4f4f', '#c4c4c4']
'''
prints the top categories and their respective percentages for each snapshot
'''
def print_topcat(files):
    for file in files:
        print(file)
        percentage_list = []
        with open('./Stats/' + file + '.lists', 'rb') as f:
            percentage_list = pickle.load(f)['percentage']
        filtered_list = list(filter(lambda pair: pair[1] >= 0.05, 
                                    percentage_list))
        print(filtered_list)


'''
Helper function for plot_percentage_bar
'''
def make_lists(files, cat_list):
    data_dict = {}
    for cat in cat_list:
        data_dict[cat] = [0] * len(files)
    for file in files:
        percentage_list = []
        with open('./Stats/' + file + '.lists', 'rb') as f:
            percentage_list = (pickle.load(f))['percentage']
        for (cat, percent) in percentage_list:
            if percent >= 0.05 and cat in cat_list:
                data_dict[cat][files.index(file)] = percent * 100
    return data_dict


'''
visualizes the percentage frequency distribution of
interactions in different subreddits across snapshots.
'''
def plot_percentage_bar(files, data_dict, cat_list, col_list):
    indices = list(range(len(files)))
    others = []
    for i in range(len(files)):
        tmp = 100.0
        for cat in cat_list:
            tmp -= data_dict[cat][i]
        others.append(tmp)
    bar_width = 0.85
    new_dict = data_dict
    new_dict['other'] = others
    cats = cat_list + ['other']
    accum = [0] * len(files)
    for i in range(8, -1, -1):
        plt.bar(indices, data_dict[cats[i]], bottom=accum, color=col_list[i],
            edgecolor='white', width=bar_width, label=cats[i])
        accum = list(map(lambda x, y: x + y, accum, data_dict[cats[i]]))
    plt.xticks(indices, files)
    plt.xlabel('snapshots')
    plt.legend(loc='best', bbox_to_anchor=(1, 1), ncol=1)
    plt.title('Percentage Frequency Distribution of Interactions in Different Subreddits')
    plt.show()


if __name__ == '__main__':
    print_topcat(files)
    data_dict = make_lists(files, cat_list)
    plot_percentage_bar(files, data_dict, cat_list, col_list)
