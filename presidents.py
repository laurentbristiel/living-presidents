import argparse
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import matplotlib.dates as mdates


def plot_living_presidents(csv_file):
    presidents = pd.read_csv(csv_file, parse_dates=["Start Date", "End Date", "Date of Death"])
    #presidents = pd.read_csv("us_presidents_since_washington.csv", parse_dates=["Start Date", "End Date", "Date of Death"])

    # Skip first row if needed
    presidents = presidents.iloc[1:]

    # Sort data
    presidents = presidents.sort_values(by="Start Date")

    # Create Jan 1st dates from the first to the last year
    start_year = presidents["Start Date"].min().year
    end_year = pd.Timestamp("today").year
    jan_1st_dates = pd.date_range(start=f"{start_year}-01-01", end=f"{end_year}-01-01", freq='YS')

    # Build alive count and name list for each year
    counts = []
    alive_presidents_per_year = []

    for date in jan_1st_dates:
        alive_presidents = presidents[
            (presidents["Start Date"] <= date) &
            (presidents["Date of Death"].isna() | (presidents["Date of Death"] > date))
        ]["Full Name"].tolist()
        counts.append(len(alive_presidents))
        alive_presidents_per_year.append(alive_presidents)

    # Plot
    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        jan_1st_dates,
        counts,
        width=360,
        color="#1f77b4",
        edgecolor="#333",
        align="center"
    )

    plt.title("Number of Living Presidents on January 1st of Each Year", fontsize=16, weight="bold")
    plt.xlabel("Year", fontsize=12)
    plt.ylabel("Living Presidents", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.5)
    plt.tight_layout()

    # Hover interaction using nearest date matching
    cursor = mplcursors.cursor(bars, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        hover_date = mdates.num2date(sel.target[0]).replace(tzinfo=None)
        idx = min(range(len(jan_1st_dates)), key=lambda i: abs(jan_1st_dates[i] - hover_date))
    
        date_label = jan_1st_dates[idx].strftime('%Y-%m-%d')
        names = "\n".join(alive_presidents_per_year[idx])
    
        sel.annotation.set_text(f"Date: {date_label}\nAlive: {counts[idx]}\n\n{names}")
    
        # Set background to opaque yellow
        sel.annotation.get_bbox_patch().set(fc="lightyellow", alpha=1.0)

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot living presidents over time.")
    parser.add_argument("csv_file", help="Path to the presidents CSV file")
    args = parser.parse_args()

    plot_living_presidents(args.csv_file)    
