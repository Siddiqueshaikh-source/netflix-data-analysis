# Netflix Data Analysis

Exploratory data analysis of 8,800+ Netflix movies and TV shows using Python, Pandas, Matplotlib, and Seaborn.

## Dataset
Netflix Movies and TV Shows dataset from Kaggle (`netflix_titles.csv`): title, type, director, cast, country, date added, release year, rating, duration, and genres.

## Questions Answered
- How is the catalog split between movies and TV shows?
- Which genres and countries produce the most content?
- How has the number of titles added changed over time?
- What are the most common ratings?
- How long is the average movie?

## Data Cleaning
- Filled missing director, cast, and country values with "Unknown"
- Fixed rows where duration was stored in the rating column
- Converted `date_added` to datetime and extracted year and month
- Split duration into number and unit (minutes vs seasons)
- Split multi-value genre and country columns for accurate counts

## Key Findings
- Movies make up X% of the catalog, TV shows the rest
- The top genre is X, followed by X
- X leads in content production, followed by X
- Content additions peaked in X
- The most common rating is X
- The average movie runs X minutes

## Charts
![Type split](charts/1_type_split.png)
![Top genres](charts/2_top_genres.png)
![Added per year](charts/4_added_per_year.png)

## Tools
Python, Pandas, Matplotlib, Seaborn

## How to Run
1. Clone the repo
2. `pip install pandas matplotlib seaborn`
3. Run `netflix_analysis.py`
