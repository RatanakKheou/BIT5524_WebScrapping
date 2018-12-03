import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pandas as pd
import nltk

x = pd.read_csv("combinedFile")
#events = x.ix[[2]]['CategoryID']


# August = [y for y in x['CategoryID'][1:31]]
# September = [y for y in x['CategoryID'][31:270]]
#x = [events + Days for events in x['CategoryID'] for Days in x['Days']]
#print(x)


events = []
i = 0
print(type(x['Date'].iloc[[100]]))
for event in x['CategoryID']:
    if x.ix[[i]]['Date'].split('/')[0] == '8':
        print(i, x['Date'].iloc[i])
        events.append(event)
    else:
        print('Here')
    i = i + 1



# print(len(events))
# freq = nltk.FreqDist(events)
#
# print(freq)
#
# freq.plot(20, cumulative = False)
