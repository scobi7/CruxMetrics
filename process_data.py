import pandas as pd
import csv
import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
from preview_routes import normalizeDifficulty, plot_holds, visualize_route

routes = pd.read_csv('routes.csv')

all_x = set()
all_y = set()


mat = sp.csr_array((168, 168))

routes = routes.iterrows()
index, route = next(routes)
# for index, route in routes.iterrows():

r_angle = route['angle']
r_label = normalizeDifficulty(round(route['difficulty_average']))
r_frames = route['frames']

with open('holds.csv', mode='r') as infile:
    reader = csv.reader(infile)
    holddict = dict((rows[0],[rows[1],rows[2]]) for rows in reader)


for frame in r_frames.split("p")[1:]:
    hold_id = (frame[0:4])
    
    x = int(holddict[hold_id][0])# // 4
    y = int(holddict[hold_id][1])# // 4
    all_x.add(x)

    all_y.add(y)

    mat[x, y] = 1

print(mat)

r_name = route['name']
r_angle = route['angle']
r_difficulty = normalizeDifficulty(round(route['difficulty_average']))
plot_holds(route['frames'], 'holds.csv')

plt.title(f'{r_name}, V{r_difficulty}, angle: {r_angle}')

# Extent changes x/y scale, still wonky but looks pretty good ?
img = plt.imread("assets/kilterbg.jpg")

plt.imshow(np.flipud(img), origin='lower', extent=[0, 143.625, 0, 158])
plt.show()


# # Extent changes x/y scale, still wonky but looks pretty good ?
# plt.imshow(np.flipud(img), origin='lower', extent=[0, 143.625, 0, 158])
# plt.show()
        
# print(len(all_x)) #42
# print(len(all_y)) #38

# plot_holds(r_frames)
# visualize_route()