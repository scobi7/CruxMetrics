import pandas as pd
import csv
import numpy as np
import scipy.sparse as sp
import matplotlib.pyplot as plt
from preview_routes import normalizeDifficulty, plot_holds, visualize_route

routes = pd.read_csv('csv/routes.csv')

all_x = set()
all_y = set()

mat = sp.csr_matrix((168, 168), dtype=int)  # Specify dtype=int for consistency

routes = routes.iterrows()
index, route = next(routes)

r_angle = route['angle']
r_label = normalizeDifficulty(round(route['difficulty_average']))
r_frames = route['frames']

manual_difficulty_assignments = {
    (24, 56): 3,
    (32, 64): 1,    
    (40, 32): 3,    
    (48, 64): 4,     
    (56, 32): 6,     
    (64, 56): 8,    
    (64, 72): 2,    
    (80, 72): 6,    
    (88, 40): 2,    
    (88, 80): 1,   
    (112, 56): 5,    
    (120, 56): 3,    
    (136, 72): 4,    
    (152, 72): 7,   
    (152, 88): 3    
}

with open('csv/holds.csv', mode='r') as infile:
    reader = csv.reader(infile)
    holddict = dict((rows[0],[rows[1],rows[2]]) for rows in reader)

for frame in r_frames.split("p")[1:]:
    hold_id = (frame[0:4])
    
    x = int(holddict[hold_id][0])# // 4
    y = int(holddict[hold_id][1])# // 4

    all_x.add(x)
    all_y.add(y)

    #----- Binary Matrix
    mat[x, y] = 1

print(type(mat))

# plot_holds(r_frames)
# visualize_route()
#     #----- Non-binary Matrix
#     if (y, x) in manual_difficulty_assignments:
#         difficulty_value = manual_difficulty_assignments[(y, x)]
#     else:
#         # Assign a default value if coordinate not found in manual_difficulty_assignments
#         difficulty_value = 1  # You can adjust the default value as needed

#     mat[y, x] = difficulty_value

# dense_mat = mat.toarray()
# print(mat)