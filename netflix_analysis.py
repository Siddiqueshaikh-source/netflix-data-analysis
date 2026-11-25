# %% [markdown]
# # Netflix Data Analysis
# Exploratory data analysis of the Netflix catalog (movies and TV shows).
# Dataset: netflix_titles.csv (Kaggle, "Netflix Movies and TV Shows")

# %% Imports
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
os.makedirs("charts", exist_ok=True)

# %% Load and inspect
df = pd.read_csv("netflix_titles.csv")
print("Shape:", df.shape)
df.info()
print(df.isnull().sum())

# %% Clean
df = df.drop_duplicates()

# Fill missing text columns
for col in ["director", "cast", "country"]:
    df[col] = df[col].fillna("Unknown")

# A few rows have the duration stored in the rating column (data glitch) - fix it
mask = df["rating"].str.contains("min", na=False)
df.loc[mask, "duration"] = df.loc[mask, "rating"]
df.loc[mask, "rating"] = "Unknown"
df["rating"] = df["rating"].fillna("Unknown")

# Dates
df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month

# Duration: number + unit (minutes for movies, seasons for TV shows)
df["duration_num"] = df["duration"].str.extract(r"(\d+)").astype(float)
df["duration_unit"] = df["duration"].str.extract(r"(min|Season)")

# One row per genre / per country (these columns hold comma-separated lists)
genres = df.assign(genre=df["listed_in"].str.split(", ")).explode("genre")
genres["genre"] = genres["genre"].str.strip()

countries = df[df["country"] != "Unknown"].assign(
    country=lambda d: d["country"].str.split(",")
).explode("country")
countries["country"] = countries["country"].str.strip()

print("Clean shape:", df.shape)
print(df.isnull().sum())

# %% 1. Movies vs TV Shows
type_counts = df["type"].value_counts()
print(type_counts)
plt.figure(figsize=(5, 4))
sns.barplot(x=type_counts.index, y=type_counts.values)
plt.title("Movies vs TV Shows on Netflix")
plt.ylabel("Number of titles")
plt.xlabel("")
plt.tight_layout()
plt.savefig("charts/1_type_split.png", dpi=150)
plt.show()

# %% 2. Top 10 genres
top_genres = genres["genre"].value_counts().head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=top_genres.values, y=top_genres.index)
plt.title("Top 10 Genres")
plt.xlabel("Number of titles")
plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/2_top_genres.png", dpi=150)
plt.show()

# %% 3. Top 10 content-producing countries
top_countries = countries["country"].value_counts().head(10)
plt.figure(figsize=(8, 5))
sns.barplot(x=top_countries.values, y=top_countries.index)
plt.title("Top 10 Countries by Number of Titles")
plt.xlabel("Number of titles")
plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/3_top_countries.png", dpi=150)
plt.show()

# %% 4. Content added per year
added = df.dropna(subset=["year_added"]).groupby(["year_added", "type"]).size().unstack(fill_value=0)
added.index = added.index.astype(int)
added.plot(kind="line", marker="o", figsize=(9, 5))
plt.title("Titles Added to Netflix per Year")
plt.xlabel("Year added")
plt.ylabel("Number of titles")
plt.tight_layout()
plt.savefig("charts/4_added_per_year.png", dpi=150)
plt.show()

# %% 5. Rating distribution
rating_order = df["rating"].value_counts().index
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x="rating", order=rating_order)
plt.title("Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of titles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/5_ratings.png", dpi=150)
plt.show()

# %% 6. Movie duration distribution
movies = df[df["type"] == "Movie"]
plt.figure(figsize=(8, 5))
sns.histplot(movies["duration_num"].dropna(), bins=30)
plt.title("Movie Duration Distribution (minutes)")
plt.xlabel("Minutes")
plt.tight_layout()
plt.savefig("charts/6_movie_duration.png", dpi=150)
plt.show()

# %% Key numbers for your findings
print("Movies share: {:.1f}%".format(100 * type_counts["Movie"] / len(df)))
print("Top genre:", top_genres.index[0], "-", top_genres.iloc[0], "titles")
print("Top country:", top_countries.index[0], "-", top_countries.iloc[0], "titles")
print("Peak year for additions:", int(df["year_added"].value_counts().idxmax()))
print("Most common rating:", df["rating"].value_counts().idxmax())
print("Average movie length: {:.0f} min".format(movies["duration_num"].mean()))
print("Most common TV show length:", df[df["type"] == "TV Show"]["duration"].value_counts().idxmax())

# %% [markdown]
# ## Key Findings
# Write 4-5 findings here in plain English using the numbers printed above.
