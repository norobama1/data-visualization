import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the merged Excel file
data = pd.read_excel('merged_output.xlsx')

# Convert Date column to datetime format if it's not already
data['Date'] = pd.to_datetime(data['Date'])

# Calculate the 30-day moving average for PR
data['30d_MA_PR'] = data['PR'].rolling(window=30).mean()

# Calculate the budget line
start_date = pd.to_datetime('2019-07-01')
data['Year'] = ((data['Date'] - start_date).dt.days / 365.25).astype(int)
data['Budget_PR'] = 73.9 * (1 - 0.008) ** data['Year']

# Color code based on GHI values
conditions = [
    (data['GHI'] < 2),
    (data['GHI'] >= 2) & (data['GHI'] < 4),
    (data['GHI'] >= 4) & (data['GHI'] < 6),
    (data['GHI'] >= 6)
]
colors = ['navy', 'lightblue', 'orange', 'brown']
data['Color'] = np.select(conditions, colors)

# Create the plot
plt.figure(figsize=(16, 10))

# Plot the scatter points with GHI color coding
plt.scatter(data['Date'], data['PR'], c=data['Color'], label='PR values')

# Plot the 30-day moving average line
plt.plot(data['Date'], data['30d_MA_PR'], color='red', linewidth=2, label='30-Day Moving Average of PR')

# Plot the budget line
plt.plot(data['Date'], data['Budget_PR'], color='darkgreen', linewidth=2, label='Target Budget Yield Performance Ratio')

# Add labels, title, and subtitle
plt.title('Performance Ratio Evolution\nFrom 2019-07-01 to 2022-03-24', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Performance Ratio [%]', fontsize=14)

# Set y-axis limits from 0 to 100
plt.ylim(0, 110)  # Zooming into the y-axis range for better visibility

# Manually adding the GHI legend in a straight line above the text
plt.text(data['Date'].min(), 100, 'Daily Irradiation [kWh/m²]', fontsize=12)

# Scatter points and their corresponding labels on the same line
x_text_position = data['Date'].min() + pd.Timedelta(days=10)

plt.scatter([x_text_position], [95], color='navy')
plt.text(x_text_position + pd.Timedelta(days=5), 95, '< 2', fontsize=12, verticalalignment='center')

plt.scatter([x_text_position + pd.Timedelta(days=60)], [95], color='lightblue')
plt.text(x_text_position + pd.Timedelta(days=65), 95, '2 - 4', fontsize=12, verticalalignment='center')

plt.scatter([x_text_position + pd.Timedelta(days=120)], [95], color='orange')
plt.text(x_text_position + pd.Timedelta(days=125), 95, '4 - 6', fontsize=12, verticalalignment='center')

plt.scatter([x_text_position + pd.Timedelta(days=180)], [95], color='brown')
plt.text(x_text_position + pd.Timedelta(days=185), 95, '> 6', fontsize=12, verticalalignment='center')

yearly_budgets = [
    (1, 73.9),
    (2, 73.9 * (1 - 0.008)),
    (3, 73.9 * (1 - 0.008) ** 2)
]

budget_text = "Target Budget Yield Performance Ratio\n" + "[" + \
              " | ".join([f"1Y={yearly_budgets[0][1]:.1f}%, 2Y={yearly_budgets[1][1]:.1f}%, 3Y={yearly_budgets[2][1]:.1f}%"]) + "]"

# Center the text annotations
mid_date = data['Date'].median()
plt.text(mid_date, 28, budget_text, color='darkgreen', fontsize=8, ha='center')
plt.text(mid_date, 35, '30-d moving average of PR', color='red', fontsize=8, ha='center')

# Annotation for Points above Target Budget PR in the center
points_above_budget = data[data['PR'] > data['Budget_PR']].shape[0]
total_points = data.shape[0]
percentage_above = (points_above_budget / total_points) * 100
plt.text(mid_date, 24, f'Points above Target Budget PR = {points_above_budget}/{total_points} = {percentage_above:.1f}%', fontsize=8, color='black', ha='center')

# Annotations for Average PR over different periods
average_text = (
    f"Average PR last 7-d: {data['PR'].tail(7).mean():.1f} %\n"
    f"Average PR last 30-d: {data['PR'].tail(30).mean():.1f} %\n"
    f"Average PR last 60-d: {data['PR'].tail(60).mean():.1f} %\n"
    f"Average PR last 90-d: {data['PR'].tail(90).mean():.1f} %\n"
    f"Average PR last 365-d: {data['PR'].tail(365).mean():.1f} %\n"
    f"Average PR Lifetime: {data['PR'].mean():.1f} %"
)

plt.text(data['Date'].max(), 35, average_text, fontsize=10, color='black', ha='right')
# Adding grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)

# Show the plot
plt.show()
