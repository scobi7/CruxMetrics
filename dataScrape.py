#transferring all the important data into csv file
import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('kilterdata.sqlite')
#combining the sqlquerys
sql_query = """
SELECT c.uuid, c.name, c.frames, cs.angle, cs.ascensionist_count, cs.difficulty_average, cs.quality_average
FROM climbs c
JOIN climb_stats cs ON c.uuid = cs.climb_uuid;
"""

df = pd.read_sql_query(sql_query, conn)
conn.close()

#removing duplicates
df = df.drop_duplicates(subset='uuid', keep='first')

# Filter climbs with "ascensionist_count" over 50 and "quality_average" over 2.0
df_filtered = df[(df['ascensionist_count'] > 50)]
#add for quality average
#& (df['quality_average'] > 2.0)]

# Sort the filtered DataFrame by "difficulty_average"
df_filtered_sorted = df_filtered.sort_values(by='difficulty_average')
df_filtered_sorted.to_csv('noquality_sorted.csv', index=False)
