# Batter Metrics Analysis

This project is a **Baseball Analytics Application** that analyzes the performance of batters using Statcast data. The application is designed to provide a detailed breakdown of a player's average run expectancy, scaled by various factors such as innings and outs.

## Features

- **Player Selection**: Choose from a list of players (e.g., Aaron Judge, Mike Trout) for analysis.
- **Year Selection**: Select a specific year (from 2018-2022) for the data analysis.
- **Average Run Expectancy Calculation**: Computes and compares the average run expectancy for the selected player versus other players.
- **Custom Run Expectancy Scaling**: The application applies a scaling factor based on the inning and number of outs to better reflect the impact of each play in the game.

## Methodology

The application fetches data from a SQLite database (`statcast.db`) containing Statcast data. It calculates points based on the outcomes of plays (e.g., walks, singles, homers) and applies scaling factors to these points according to the inning and the number of outs.

### Data Analysis Workflow:
1. **User Input**: The user selects a player and a year.
2. **SQL Query Execution**: The application fetches player-specific data from the database for the given year.
3. **Run Expectancy Calculation**:
   - Points are assigned based on the description of the plays (e.g., walks, singles, homers).
   - Points are scaled based on the inning and number of outs using a custom function.
4. **Results Display**: The average run expectancy for the selected player and other players is displayed on the GUI.

### Run Expectancy Points

The points for each play are determined using the following system:

- **Positive Points**:
  - Walks: +1
  - Single: +2
  - Doubles: +4
  - Triples: +6
  - Homers: +10
  - Scores: +7
- **Negative Points** (for outs):
  - Strikeouts, Flyouts, Groundouts: -2
  - Outs at 2nd: -4
  - Outs at 3rd: -6

These points are then scaled based on the inning and outs for a more realistic evaluation of each play.

## Technology Stack

- **Python**: The core logic for the analysis and scaling of player performance is implemented in Python.
- **SQLite**: Statcast data is stored in a local SQLite database (`statcast.db`), from which relevant player data is fetched using SQL queries.
- **Tkinter**: A simple GUI built with Tkinter allows users to interact with the application by selecting players, years, and executing the analysis.
- **Pandas**: Data manipulation and analysis are performed using Pandas for reading SQL queries and performing operations on the data.

## GUI

The graphical user interface (GUI) allows the user to:
- Select a player from a dropdown menu.
- Choose a year for analysis.
- View a progress bar indicating that the analysis is being performed.
- Display the results directly on the interface once the analysis is complete.

## How It Works

The user selects a player and a year from the dropdowns and clicks the "Analyze" button. The application fetches the relevant Statcast data, 
calculates the player's run expectancy based on the description of the plays, and compares it to the average run expectancy of other players for that year. The results are displayed in real time on the application interface.

### Scaling by Innings and Outs

The run expectancy points are scaled based on:
- **Inning**: A linear interpolation scaling from 1 to 1.5 as innings progress.
- **Outs**: A different scale depending on whether the play results in positive or negative points (e.g., outs result in a more significant negative impact when fewer outs are present).

## Running the Project

1. Ensure you have Python 3.x installed.
2. Install the necessary libraries:
   ```bash
   pip install pandas sqlite3 tkinter
   ```
3. Run the `baseball_analytics.py` file to launch the GUI and start the analysis.

## Note About the Data

Due to the large file size and constant updates, the Statcast CSV file is **omitted** from this project. You can access the most up-to-date 
Statcast data through the [Baseball Savant Statcast Search](https://baseballsavant.mlb.com/statcast_search) to fetch the required CSV files.
Once the data is downloaded, you can integrate it into the `statcast.db` SQLite database for further analysis.
