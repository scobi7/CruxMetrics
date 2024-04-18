import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

def normalizeDifficulty(difficulty):
    ranges = {
        (10, 12): 0,
        (13, 14): 1,
        (15, 15): 2,
        (16, 17): 3,
        (18, 19): 4,
        (20, 21): 5,
        (22, 22): 6,
        (23, 23): 7,
        (24, 25): 8,
        (26, 26): 9,
        (27, 27): 10,
        (28, 28): 11,
        (29, 29): 12,
        (30, 30): 13,
        (31, 31): 14,
        (32, 32): 15,
        (33, 33): 16,
    }
    for range, value in ranges.items():
        if range[0] <= difficulty <= range[1]:
            return value
        
def plot_holds(r_frames, holdsfilepath: str='holds.csv'):
    # Create dictionary from holds csv
    with open(holdsfilepath, mode='r') as infile:
        reader = csv.reader(infile)
        holddict = dict((rows[0],[rows[1],rows[2]]) for rows in reader)

    # Parse frames and plot holds at correct x/y
    for frame in r_frames.split("p")[1:]:
        hold_id = (frame[0:4])
        
        x = int(holddict[hold_id][0])
        y = int(holddict[hold_id][1])

        color = int(frame[6:7])
        if color == 2:
            dot = 'g'
        elif color == 3:
            dot = 'b'
        elif color == 4:
            dot = 'm'
        else:
            dot = 'y'
        
        plt.scatter(x, y, s=150, facecolors='none', edgecolors=dot)

def visualize_route(routesfilepath: str='routes.csv', holdsfilepath: str='holds.csv', random=True):
    # Read in routes to df.
    routes = pd.read_csv(routesfilepath)

    img = plt.imread("assets/kilterbg.jpg")
    
    # Random Sample
    if (random == True):
        routes = routes.sample(1)
        idx, route = next(routes.iterrows())
    # In order of df
    else:
        idx, route = next(routes.iterrows())
    r_name = route['name']
    r_angle = route['angle']
    r_difficulty = normalizeDifficulty(round(route['difficulty_average']))
    plot_holds(route['frames'], holdsfilepath)

    plt.title(f'{r_name}, V{r_difficulty}, angle: {r_angle}')

    # Extent changes x/y scale, still wonky but looks pretty good ?
    plt.imshow(np.flipud(img), origin='lower', extent=[0, 143.625, 0, 158])
    plt.show()