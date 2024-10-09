import pandas as pd
import sqlite3
from scipy.stats import linregress

# Read the CSV file into a DataFrame
df = pd.read_csv('statcast.csv', encoding='ISO-8859-1', engine='c', on_bad_lines='skip')

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('statcast.db')

# Save the DataFrame into the SQLite database
df.to_sql('statcast_data', conn, if_exists='replace', index=False)

# Close the connection to the database
conn.close()
