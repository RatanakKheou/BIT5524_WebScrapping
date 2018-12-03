import numpy as np
import matplotlib.pyplot as plt

# data to plot
n_groups = 3
Academic = (7, 46, 69)
Events = (7, 0, 43)
Special = (7, 0, 0)
Conference = (0, 40, 0)
Seminar = (0, 40, 0)
Service = (0, 0, 49)
# August = Academic 7, events 7, special 7
#
#
# September = Academic 46, Conference 40, Seminar 40
#
#
# October = Academic 69, Service 49, Event 43
# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.25
opacity = 0.8

rects1 = plt.bar(index, Academic, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Academic')
rects2 = plt.bar(index + bar_width, Events, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Events')
rects2 = plt.bar(index + 2*bar_width, Special, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Special')
rects4 = plt.bar(index + bar_width, Conference, bar_width,
                 alpha=opacity,
                 color='black',
                 label='Conference')
rects5 = plt.bar(index + 2*bar_width, Seminar, bar_width,
                 alpha=opacity,
                 color='yellow',
                 label='Seminar')
rects5 = plt.bar(index + 2*bar_width, Service, bar_width,
                 alpha=opacity,
                 color='purple',
                 label='Service')

plt.xlabel('Months')
plt.ylabel('Frequency')
plt.title('Top Three CategoryID per Month')
plt.xticks(index + bar_width, ('August', 'September', 'November'))
plt.legend()
plt.tight_layout()
plt.show()
