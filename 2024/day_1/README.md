# 30DayMapChallenge - Day 1
## Day 1: Points
**Date**: 01-11-2024

**Theme**: 30DayMapChallenge classic: A map with points. Start the challenge with points. Show individual locations—anything from cities to trees or more abstract concepts. Simple, but a key part of the challenge. 📍

**Description**: This project visualizes fire incidents in San Francisco for the year 2024 using Cartopy and Matplotlib. The data is fetched from San Francisco's open data API, and a scatter plot is created on a map to show the locations of these incidents.

### Requirements

- Python 3.x
- Required packages:
  - cartopy
  - matplotlib
  - pandas
  - requests

### Setup

1. Ensure you have Python 3.x installed.
2. Install the required packages using pip:
   ```bash
   pip install cartopy matplotlib pandas requests
   ```

### Usage

1. Run the script to fetch and visualize fire incidents:
   ```bash
   python plot_sf_fire_incidents.py
   ```
2. The output will be saved as `fire_incidents.png`.

### Project Structure

- `plot_sf_fire_incidents.py`: Main script for fetching and visualizing fire incidents.
- `utils.py`: Contains helper functions for data processing.

![Strava activities map from 2020 to 2024](visualization/fire_incidents.png)