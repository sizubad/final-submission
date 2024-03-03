import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load data
day_df = pd.read_csv("dashboard\day.csv")

# Set style seaborn
sns.set(style='dark')

# Rename columns
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Map numeric values to categorical labels
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['weather_cond'] = day_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

# Sidebar - Date selection
st.sidebar.title('Date Range Selection')
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()
start_date, end_date = st.sidebar.date_input("Select range", [min_date, max_date])

# Filter data based on selected dates
main_df = day_df[(day_df['dateday'] >= str(start_date)) & (day_df['dateday'] <= str(end_date))]

# Display header
st.title('Bike Rental Dashboard 🚲')

# Daily Rentals
st.header('Daily Rentals')
st.subheader('Total Rentals')
st.metric('Total Rentals', main_df['count'].sum())
st.subheader('Breakdown by User Type')
st.metric('Casual Users', main_df['casual'].sum())
st.metric('Registered Users', main_df['registered'].sum())

# Monthly Rentals
st.header('Monthly Rentals')
monthly_rent_df = main_df.groupby('month')['count'].sum().reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
fig, ax = plt.subplots()  # Create a Matplotlib figure
sns.barplot(x=monthly_rent_df.index, y=monthly_rent_df.values, ax=ax)
plt.title('Monthly Rentals')
plt.xlabel('Month')
plt.ylabel('Total Rentals')
plt.xticks(rotation=45)
st.pyplot(fig)  # Pass the figure to st.pyplot()

# Seasonal Rentals
st.header('Seasonal Rentals')
season_rent_df = main_df.groupby('season')[['registered', 'casual']].sum()
fig, ax = plt.subplots()  # Create a Matplotlib figure
sns.barplot(data=season_rent_df, x=season_rent_df.index, y='registered', color='skyblue', label='Registered', ax=ax)
sns.barplot(data=season_rent_df, x=season_rent_df.index, y='casual', color='orange', label='Casual', ax=ax)
plt.title('Seasonal Rentals')
plt.xlabel('Season')
plt.ylabel('Total Rentals')
plt.legend()
st.pyplot(fig)  # Pass the figure to st.pyplot()

# Weather-wise Rentals
st.header('Weather-wise Rentals')
weather_rent_df = main_df.groupby('weather_cond')['count'].sum()
fig, ax = plt.subplots()  # Create a Matplotlib figure
sns.barplot(x=weather_rent_df.index, y=weather_rent_df.values, palette='viridis', ax=ax)
plt.title('Weather-wise Rentals')
plt.xlabel('Weather Condition')
plt.ylabel('Total Rentals')
plt.xticks(rotation=45)
st.pyplot(fig)  # Pass the figure to st.pyplot()

# Weekday, Workingday, and Holiday Rentals
st.header('Weekday, Workingday, and Holiday Rentals')
weekday_rent_df = main_df.groupby('weekday')['count'].sum().reindex(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
workingday_rent_df = main_df.groupby('workingday')['count'].sum()
holiday_rent_df = main_df.groupby('holiday')['count'].sum()
fig, axes = plt.subplots(3, 1, figsize=(10, 15))

# Weekday Rentals
axes[0].bar(weekday_rent_df.index, weekday_rent_df.values, color='skyblue')
axes[0].set_title('Rentals by Weekday')
axes[0].set_xlabel('Weekday')
axes[0].set_ylabel('Total Rentals')

# Workingday Rentals
axes[1].bar(workingday_rent_df.index.map({0: 'Holiday', 1: 'Workingday'}), workingday_rent_df.values, color='orange')
axes[1].set_title('Rentals by Workingday')
axes[1].set_xlabel('Day Type')
axes[1].set_ylabel('Total Rentals')

# Holiday Rentals
axes[2].bar(holiday_rent_df.index.map({0: 'Non-Holiday', 1: 'Holiday'}), holiday_rent_df.values, color='green')
axes[2].set_title('Rentals by Holiday')
axes[2].set_xlabel('Day Type')
axes[2].set_ylabel('Total Rentals')

plt.tight_layout()
st.pyplot(fig)  # Pass the figure to st.pyplot()

# Footer
st.markdown('© 2024 Siti Zubaidah. All rights reserved.')

