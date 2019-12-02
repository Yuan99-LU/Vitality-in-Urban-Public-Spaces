import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_orig = pd.read_csv('by_months/ranks/Apr_rank_by_counts.csv', names = 'ab')

data_top20 = data_orig.sort_values(by = ['b'],ascending= False)[0:20]
#data.column_name = ['a', 'language', 'count']
data = data_top20['b']
print(data.values)
#column_name = 'count'
x_pos = np.arange(len(data))
x_pos_labels = data_top20['a']
'''
names = {'author_contributions_mean': 'Normalized Contributions of Reviewers', 'author_votes_mean':'Normalized Helpful Votes of Reviewers',
         'rating_csore_mean': 'Normalized Review Score', 'basic_sentiment_text_mean':'Normalized Basic Sentiment Text Analysis', 'count':'Number of Reviews',
         'basic_sentiment_title_mean':'Normalized Basic Sentiment Title Analysis'}

languages = np.array(data['review language'])
'''

fig, ax = plt.subplots(figsize=(12,5))
#ax.bar(x_pos, e_mean, yerr=e_std, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.bar(x_pos, data, align='center', alpha=0.5, ecolor='black', capsize=10)

ax.set_ylabel('Frequency of Terms Appeared')
ax.set_xticks(x_pos)
ax.set_xticklabels(x_pos_labels, rotation=60)
ax.set_title(' Top 20 Terms Derived from Photos Taken in Lund in' + month )
ax.yaxis.grid(True)

for i, v in enumerate(data):
    ax.text(i - 0.25, v+0,  str(v), color='blue', fontweight='bold')
# Save the figure and show
plt.tight_layout()
plt.savefig('by_months/plots/' + 'try' + '.png')
plt.show()

#plt.errorbar(x, e_mean, e_std, linestyle='None', marker='^')
#plt.show()


'''
x = np.array([1, 2, 3, 4, 5])
y = np.power(x, 2) # Effectively y = x**2
e = np.array([1.5, 2.6, 3.7, 4.6, 5.5])

plt.errorbar(x, y, e, linestyle='None', marker='^')

plt.show()
'''

