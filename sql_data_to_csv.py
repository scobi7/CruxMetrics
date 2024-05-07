#transferring all the important data into csv file
import sqlite3
import pandas as pd

def scrape_routes(filepath: str='routes.csv', ascensionist_filter: int=50, quality_filter: float=2.0, is_listed: int=1, layout_id: int=1):
    #Connect to the SQLite database
    conn = sqlite3.connect('databases/kilter.db')

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

def scrape_holds(filepath: str='holds.csv'):
    #Connect to the SQLite database
    conn = sqlite3.connect('databases/kilter.db')

    # SQL Query for uuid, route name, path, angle, completions, avg diff., avg quality
    sql_query = """SELECT p.id, h.x, h.y
    FROM placements p
    JOIN holes h ON p.hole_id = h.id
    """

    df = pd.read_sql_query(sql_query, conn)
    conn.close()

    df.to_csv(filepath, index=False)

scrape_routes()