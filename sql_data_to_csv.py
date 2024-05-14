import sqlite3
import scipy.sparse as sp
import numpy as np
import csv
from preview_routes import normalizeDifficulty, plot_holds
import pandas as pd
import matplotlib.pyplot as plt
import h5py

def scrape_routes(filepath: str='csv/routes.csv', ascensionist_filter: int=50, quality_filter: float=2.0, is_listed: int=1, layout_id: int=1):
    # Connect to the SQLite database
    conn = sqlite3.connect('db/kilter.db')

    # SQL Query for uuid, route name, path, angle, completions, avg diff., avg quality
    sql_query = f"""
    SELECT c.uuid, c.name, c.frames, cs.angle, cs.ascensionist_count, cs.difficulty_average, cs.quality_average
    FROM climbs c
    JOIN climb_stats cs ON c.uuid = cs.climb_uuid
    WHERE c.is_listed = {is_listed}
    AND c.layout_id = {layout_id};
    """

    df = pd.read_sql_query(sql_query, conn)
    conn.close()

    # Removing duplicates
    df = df.drop_duplicates(subset='uuid', keep='first')

    # Filter climbs with "ascensionist_count" over 50 and "quality_average" over 2.0
    df_filtered = df[(df['ascensionist_count'] > ascensionist_filter) & (df['quality_average'] > quality_filter)]

    # Sort the filtered DataFrame by "difficulty_average"
    df_filtered_sorted = df_filtered.sort_values(by='difficulty_average')
    df_filtered_sorted.to_csv(filepath, index=False)

def scrape_holds(filepath: str='csv/holds.csv'):
    # Connect to the SQLite database
    conn = sqlite3.connect('db/kilter.db')

    # SQL Query for uuid, route name, path, angle, completions, avg diff., avg quality
    sql_query = """SELECT p.id, h.x, h.y
    FROM placements p
    JOIN holes h ON p.hole_id = h.id
    """

    df = pd.read_sql_query(sql_query, conn)
    conn.close()

    df.to_csv(filepath, index=False)

def create_hdf5(filepath: str='csv/routes.csv', ascensionist_filter: int=20, quality_filter: float=1.5):
    # Connect to the SQLite database
    conn = sqlite3.connect('db/kilter.db')

    # SQL Query for uuid, route name, path, angle, completions, avg diff., avg quality
    sql_query = f"""
    SELECT climbs.frames, climb_stats.angle, climb_stats.difficulty_average
    FROM climb_stats
    INNER JOIN climbs ON climb_stats.climb_uuid = climbs.uuid
    WHERE climbs.is_listed = 1 
        AND climbs.layout_id = 1 
        AND climb_stats.ascensionist_count > {ascensionist_filter} 
        AND climb_stats.quality_average > {quality_filter}
    """

    df_routes = pd.read_sql_query(sql_query, conn)
    conn.close()

    routes = df_routes.iterrows()
    matrices = []
    labels = []
    with open('csv/holds.csv', mode='r') as holds_csv:
        # index, route = next(routes)        
        reader = csv.reader(holds_csv)
        holddict = dict((rows[0],[rows[1],rows[2]]) for rows in reader)
        for index, route in routes:
            mat = sp.lil_matrix((168, 168))

            r_angle = route['angle']
            r_label = normalizeDifficulty(round(route['difficulty_average']))
            r_frames = route['frames']

            for frame in r_frames.split("p")[1:]:
                hold_id = (frame[0:4])
                
                x = int(holddict[hold_id][0])# // 4
                y = int(holddict[hold_id][1])# // 4

                mat[x, y] = 1

            matrices.append(mat)
            labels.append(r_label)

            # print(mat, r_label)

            # img = plt.imread("assets/kilterbg.jpg")
            # plot_holds(route['frames'], 'csv/holds.csv')
            # plt.title(f'V{r_label}, angle: {r_angle}')
            # plt.imshow(np.flipud(img), origin='lower', extent=[0, 143.625, 0, 158])
            # plt.show()
                        
    hf = h5py.File('data.h5', 'w')

    ds = np.array([(matrix, label) for matrix, label in zip(matrices, labels)])

    print(ds.astype(np.int64))

    hf.create_dataset('routes', data=ds)

    hf.close


create_hdf5()