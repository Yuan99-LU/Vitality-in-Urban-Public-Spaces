import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data_orig = pd.read_csv('sort_by_group_mean_count_restaurants.csv')

data = data_orig.sort_values(by = ['count'])[8:]
#data.column_name = ['a', 'language', 'count']
column_name = 'count'

names = {'author_contributions_mean': 'Normalized Contributions of Reviewers', 'author_votes_mean':'Normalized Helpful Votes of Reviewers',
         'rating_csore_mean': 'Normalized Review Score', 'basic_sentiment_text_mean':'Normalized Basic Sentiment Text Analysis', 'count':'Number of Reviews',
         'basic_sentiment_title_mean':'Normalized Basic Sentiment Title Analysis'}

languages = np.array(data['review language'])
x_pos = np.arange(len(languages))
#x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
#df = data[column_name + '_mean']
df = data[column_name ]
#e_mean =np.array((df-df.min())/(df.max()-df.min()))
e_mean = np.array(df/df.sum())
#e_mean =  np.array(data[column_name + '_mean'])
print(len(e_mean))
e_std = list([0]*len(languages))
'''
if(column_name == 'basic_sentiment'):   
    e_std = list([0]*len(languages))
else:
     e_std = np.array(data[column_name + '_std'])
print(e_std)
'''

fig, ax = plt.subplots(figsize=(12,5))
#ax.bar(x_pos, e_mean, yerr=e_std, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.bar(x_pos, e_mean, align='center', alpha=0.5, ecolor='black', capsize=10)
if(column_name == 'count'):
    ax.set_ylabel(names[column_name])
else:
    ax.set_ylabel('Average & Deviation of ' + names[column_name])
ax.set_xticks(x_pos)
ax.set_xticklabels(languages, rotation=60)
ax.set_title(names[column_name] + ' by Different Languages')
ax.yaxis.grid(True)

for i, v in enumerate(e_mean):
    ax.text(i - 0.25, v+0,  str(round(v*100, 1))+'%', color='blue', fontweight='bold')
# Save the figure and show
plt.tight_layout()
plt.savefig('plot/' + names[column_name] + '.png')
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

