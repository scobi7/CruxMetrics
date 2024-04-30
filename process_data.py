import pandas as pd
import csv
import scipy.sparse as sp
from preview_routes import normalizeDifficulty

routes = pd.read_csv('routes.csv')

all_x = set()
all_y = set()


mat = sp.coo_array((42, 42))

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
    
    x = int(holddict[hold_id][0]) // 4
    y = int(holddict[hold_id][1]) // 4
    all_x.add(x)

    all_y.add(y)

    mat[y, x] = 1
        
# print(len(all_x)) #42
# print(len(all_y)) #38

print(mat)
