import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul','Aug','Sep','Oct','Nov','Dec']

for month in months:
    data_orig = pd.read_csv('by_months_prob_08/ranks/'+ 'by_months_prob_08'+month +'_rank_by_counts.csv', names = 'ab')

    data_top20 = data_orig.sort_values(by = ['b'],ascending= False)[0:20]
    #data.column_name = ['a', 'language', 'count']
    data = data_top20['b']
    print(data.values)
    #column_name = 'count'
    x_pos = np.arange(len(data))
    x_pos_labels = data_top20['a']


    fig, ax = plt.subplots(figsize=(12,5))
    #ax.bar(x_pos, e_mean, yerr=e_std, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.bar(x_pos, data, align='center', alpha=0.5, ecolor='black', capsize=10)

    ax.set_ylabel('Frequency of Terms Appeared')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_pos_labels, rotation=60)
    ax.set_title(' Top 20 Terms Derived from Photos Taken in Lund in ' + month )
    ax.yaxis.grid(True)

    for i, v in enumerate(data):
        ax.text(i - 0.15, v+0,  str(v), color='blue', fontweight='bold')
    # Save the figure and show
    plt.tight_layout()
    plt.savefig('by_months_prob_08/plots/' + 'by_months_prob_08'+month + 'rank_top20' + '.png')
    #plt.show()
    #plt.close()

