import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul','Aug','Sep','Oct','Nov','Dec']

group = []
for month in months:
    data_orig = pd.read_csv('by_months/ranks/'+ month +'_rank_by_counts.csv', names = 'ab')

    group.append(data_orig)


group_pd = pd.concat(group, axis = 1)

group_pd.to_csv('by_months/' +'concat_all_months.csv')
