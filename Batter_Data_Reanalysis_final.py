import pandas as pd
import sqlite3
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
import time

# Function to scale points by inning
def inning_scale(inning):
    # Linear interpolation from 1 to 1.5 for innings 1 to 9
    return 1 + 0.0625 * (inning - 1)

# Function to execute analysis based on user input
def execute_analysis():
    progress_bar.grid(row=4, column=0, columnspan=2, pady=5)
    progress_bar.start()
    analysis_thread = threading.Thread(target=analyze_data)
    analysis_thread.start()

def analyze_data():
    conn = sqlite3.connect('statcast.db')
    selected_player = player_combobox.get()
    selected_year = year_combobox.get()

    query_player = f'''
    SELECT 
      strftime('%Y', game_date) AS year, 
      inning,
      des,
      post_home_score,
      post_away_score,
      on_1b,
      on_2b,
      on_3b,
      outs_when_up
    FROM statcast_data
    WHERE inning BETWEEN 1 AND 9 AND batter_name LIKE '{selected_player}' AND strftime('%Y', game_date) LIKE '{selected_year}'
    '''
    df_player = pd.read_sql_query(query_player, conn)

    query_others = f'''
    SELECT 
      strftime('%Y', game_date) AS year, 
      inning,
      des,
      post_home_score,
      post_away_score,
      on_1b,
      on_2b,
      on_3b,
      outs_when_up
    FROM statcast_data
    WHERE inning BETWEEN 1 AND 9 AND batter_name NOT LIKE '{selected_player}' AND strftime('%Y', game_date) LIKE '{selected_year}'
    '''
    df_others = pd.read_sql_query(query_others, conn)

    df_player['points'] = df_player['des'].apply(update_run_exp)
    df_player['points_scaled'] = df_player.apply(lambda x: scale_points(x['points'], x['outs_when_up'], x['inning']), axis=1)
    avg_run_expectancy_player = df_player['points_scaled'].mean()

    df_others['points'] = df_others['des'].apply(update_run_exp)
    df_others['points_scaled'] = df_others.apply(lambda x: scale_points(x['points'], x['outs_when_up'], x['inning']), axis=1)
    avg_run_expectancy_others = df_others['points_scaled'].mean()

    conn.close()
    result_label.config(text=f"Average run expectancy per play for {selected_player}: {avg_run_expectancy_player}\nAverage run expectancy per play for other players: {avg_run_expectancy_others}")
    progress_bar.stop()
    progress_bar.grid_forget()

def update_run_exp(description):
    if description is None:
        return 0
    description = description.lower()
    points = {
        'walks': 1, 'single': 2, 'to 1st.': 2, 'to 2nd.': 4,
        'doubles': 4, 'to 3rd.': 6, 'triples': 6, 'homers': 10,
        'scores': 7, 'strikes out': -2, 'lines out': -2,
        'pops out': -2, 'called out on strikes': -2, 'flies out': -2,
        'grounds out': -2, 'out at 1st.': -2, 'out at 2nd.': -4, 'out at 3rd.': -6
    }
    return sum(description.count(key) * value for key, value in points.items())

def scale_points(points, outs, inning):
    scale_factors = {0: 1, 1: 1.5, 2: 2} if points > 0 else {0: 2, 1: 1.5, 2: 1}
    inning_factor = inning_scale(inning)
    return points * scale_factors.get(outs, 1) * inning_factor

# GUI setup
root = tk.Tk()
root.title("Baseball Analytics")

# Player selection
player_label = ttk.Label(root, text="Select Player:")
player_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
players = ['Aaron Judge', 'Mike Trout', 'Dexter Fowler', 'Jacob Stallings']
player_combobox = ttk.Combobox(root, values=players, state="readonly")
player_combobox.grid(row=0, column=1, padx=10, pady=5)

# Year selection
year_label = ttk.Label(root, text="Select Year:")
year_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
years = ['2018', '2019', '2020', '2021', '2022']
year_combobox = ttk.Combobox(root, values=years, state="readonly")
year_combobox.grid(row=1, column=1, padx=10, pady=5)

# Button to execute analysis
analyze_button = ttk.Button(root, text="Analyze", command=execute_analysis)
analyze_button.grid(row=2, column=0, columnspan=2, pady=10)

# Label to display results
result_label = ttk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2, pady=5)

# Progress bar
progress_bar = ttk.Progressbar(root, mode="indeterminate", length=200)

root.mainloop()
