# Jacob Clement
# Telling stories With Data 

import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt  
import os
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from PIL import Image, ImageDraw, ImageFont

# read in the datasets

car = pd.read_excel(r'data\\carbitrage-data.xlsx')

dram = pd.read_excel(r'data\\Data Viz Assignment_ Dram Shop.xlsx')

hmis = pd.read_excel(r'data\\Data Viz Assignment_ Missoula Unhoused Data.xlsx')

'''
Carbitrage Visualization Tasks
• (Easy) Build a visualization that illustrates what makes and models of cars are most
popular.
• (Easy) Build a visualization that illustrates the rate at which new cars are posted by day
or by week. Optionally, add information on location.
• (Easy) Build a visualization that communicates the different rates at which cars are
posted across the Craigslist locations. For instance, you could look at number of posts
per week for a set of locations.
• (Medium) Build a visualization that attempts to answer this question: When do cars tend
to be posted by location? Highlight an interesting feature of the data.
• (Difficult) Ultimately, one way people will interact with this data set is when they arrive at
a hosted site that helps them understand car prices and helps them find a good deal on
a car. For this task, assume that the user has given you a make and model to focus on
and optionally, a range of years. Create a visualization that captures the interplay
between age and mileage for a given make and model.

Dram Visualization Tasks
• (Easy) Build a visualization that illustrates the popularity of various beer types (in the
Category field) over time.
• (Easy) Build a visualization that illustrates the patterns in purchases by day of week for
both the Front Street and Central locations.
• (Easy) Build a visualization that illustrates the patterns in purchases by time of day for
both the Front Street and Central locations. Feel free to limit your analysis to either
working days (M-Th) or weekends (Fr-Su).
• (Medium) Build a visualization that compares the performance of the two locations (Front
and Central) across the entire history of the Dram Shop.
• (Difficult) Build a visualization that explores trends in beer consumption. (I recommend
you use the “category” data in the spreadsheets, but if you would like item-level data, let
me know.) Your goal is to analyze the types of beers that consumers are purchasing and
build a visualization that highlights patterns you have found.

City Visualization Tasks
• (Easy) Build a visualization that explores an aspect of client age, potentially across time.
• (Easy) Build a visualization that visualizes the annual pattern of entries into the HMIS.
• (Easy) Build a visualization demonstrating the change across time in the unhoused
population.
• (Medium) Build a visualization that illustrates the demographic make-up of clients across
ages and genders.
• (Difficult) Clients can enter the HMIS multiple times if they have multiple periods
unhoused. For each client, calculate their total time in the system. Build a visualization
that explores this measure of unhoused duration and illustrates a facet of the data that
you think merits discussion in our report at the end of the semester.

'''

# (Easy) Build a visualization that illustrates what makes and models of cars are most
# popular.

# car.columns

car['make'].unique()
car['model'].unique()

# Create a bar plot using seaborn
plt.figure(figsize=(10, 6))
sns.countplot(data=car, x='make')
plt.title('Distribution of Car Makes')
plt.xlabel('Make')
plt.ylabel('Count')
plt.show() # remember to close the plot! 

# A giant mess there are too many makes to put on one graph 

# Create a bar plot using seaborn
plt.figure(figsize=(10, 6))
sns.countplot(data=car, x='model')
plt.title('Distribution of Car Models')
plt.xlabel('model')
plt.ylabel('Count')
plt.show() # remember to close the plot!


# Count the number of occurrences of each make
top_makes = car['make'].value_counts().nlargest(5).index
top_makes_data = car[car['make'].isin(top_makes)]

# Plot for Top Makes
plt.figure(figsize=(10, 6))
sns.countplot(data=top_makes_data, x='make', order=top_makes)
plt.title('Top 5 Car Makes', loc='left', fontsize=16, pad=20)
plt.xlabel('Make')
plt.ylabel('Count')
sns.despine(top=True, right=True)
plt.savefig(r'graphs//top_5_makes.png')

# the top 5 makes are ford, chevrolet, toyota, honda, nissan. I would like to plot the top 5 models for each make.

# Ensure 'graphs' folder exists
if not os.path.exists('graphs'):
    os.makedirs('graphs')

# Define the top 5 makes
makes = ['ford', 'chevrolet', 'toyota', 'honda', 'nissan']

# Loop through each make and create a plot for the top 5 models
for make in makes:
    # Filter the data for the current make
    make_data = car[car['make'].str.lower() == make]

    # Get the top 5 models for the current make
    top_5_models = make_data['model'].value_counts().nlargest(5).index

    # Filter data for only the top 5 models
    top_models_data = make_data[make_data['model'].isin(top_5_models)]

    # Create the plot
    plt.figure(figsize=(10, 6))
    sns.countplot(data=top_models_data, x='model', order=top_5_models)
    plt.title(f'Top 5 Models for {make.capitalize()}', loc='left', fontsize=16, pad=20)
    plt.xlabel('Model')
    plt.ylabel('Count')

    sns.despine(top=True, right=True)
    # Save the plot to the 'graphs' folder
    plt.savefig(f'graphs/{make}_top_5_models.png')
    plt.close()  # Close the plot to avoid display issues in loops


# Create a figure with subplots (2 rows x 3 columns)
fig, axes = plt.subplots(2, 3, figsize=(18, 12))  # Adjust the figsize as needed
fig.suptitle('Top 5 Makes and Their Top 5 Models', fontsize=20, y=1.02)

# Custom colors for each make
colors = sns.color_palette('husl', len(top_makes))

# Plot for top 5 makes in the first subplot
ax = axes[0, 0]
top_makes_data = car[car['make'].isin(top_makes)]
sns.countplot(data=top_makes_data, x='make', order=top_makes, palette=colors, ax=ax)
ax.set_title('Top 5 Car Makes', loc='left', fontsize=14, pad=10)
# ax.set_xlabel('Make')
# ax.set_ylabel('Count')
sns.despine(ax=ax, top=True, right=True)

# Plot for top 5 models of each make in the remaining subplots
for i, make in enumerate(top_makes):
    # Determine subplot position (skip the first one)
    ax = axes[(i + 1) // 3, (i + 1) % 3]

    # Filter data for the current make
    make_data = car[car['make'].str.lower() == make.lower()]

    # Get the top 5 models for the current make
    top_5_models = make_data['model'].value_counts().nlargest(5).index

    # Filter data for only the top 5 models
    top_models_data = make_data[make_data['model'].isin(top_5_models)]

    # Create the count plot for the top 5 models of the current make
    sns.countplot(data=top_models_data, x='model', order=top_5_models, color=colors[i], ax=ax)

    # Customize each plot
    ax.set_title(f'Top 5 Models for {make.capitalize()}', loc='left', fontsize=14, pad=10)
    # ax.set_xlabel('Model') # gets in the way
    # ax.set_ylabel('Count')
    sns.despine(ax=ax, top=True, right=True)

# Hide any remaining empty subplots
if len(top_makes) < 5:
    for j in range(len(top_makes), 5):
        fig.delaxes(axes[(j + 1) // 3, (j + 1) % 3])

# Adjust layout to prevent overlap
plt.tight_layout()
plt.subplots_adjust(top=0.9)  # Adjust top to accommodate the main title
plt.savefig('graphs/top_makes_and_models_combined.png', bbox_inches='tight')
plt.show() # remember to close the plot! 

# (Easy) Build a visualization that visualizes the annual pattern of entries into the HMIS.

# Convert Date column to datetime
hmis['Date Identified'] = pd.to_datetime(hmis['Date Identified'])

print(hmis)

# Step 3: Extract year and month from the datetime column
hmis['year'] = hmis['Date Identified'].dt.year
hmis['month'] = hmis['Date Identified'].dt.month

# Create a 'year_month' column for grouping
hmis['year_month'] = hmis['Date Identified'].dt.to_period('M').astype(str)
# Group by 'year_month' and count the number of observations. Also create a count by year.
monthly_counts = hmis.groupby('year_month').size().reset_index(name='count')
yearly_counts = hmis.groupby('year').size().reset_index(name='count')

monthly_counts
#  Plot the line plot using Plotly
fig = px.line(monthly_counts, x='year_month', y='count', title='Monthly Observation Counts')

# Show the initial plot
# fig.show() this takes a minute

# Step 6: Forecasting

# Convert 'year_month' back to a datetime format for forecasting
monthly_counts['year_month'] = pd.to_datetime(monthly_counts['year_month'])

# Use Exponential Smoothing for forecasting
model = ExponentialSmoothing(
    monthly_counts['count'], 
    seasonal='add', 
    seasonal_periods=12
).fit()

# Generate forecast for the next 12 months
forecast = model.forecast(12)

# Create a DataFrame for the forecasted values
forecast_df = pd.DataFrame({
    'year_month': pd.date_range(start=monthly_counts['year_month'].iloc[-1] + pd.offsets.MonthBegin(), periods=12, freq='M'),
    'count': forecast
})

# Append the forecast to the original data
combined_df = pd.concat([monthly_counts, forecast_df], ignore_index=True)

# Step 7: Plot the combined data with forecast
fig_forecast = px.line(combined_df, x='year_month', y='count', title='Monthly Observation Counts with Forecast')
fig_forecast.add_scatter(x=forecast_df['year_month'], y=forecast_df['count'], mode='lines', name='Forecast', line=dict(dash='dash'))

# Show the plot with forecast
# fig_forecast.show()

fig_forecast.write_html( r'html\\bad_line_chart.html', 
                   auto_open=True )

# Plot the combined data with forecast
fig = go.Figure()

# Plot the historical data
fig.add_trace(go.Scatter(
    x=monthly_counts['year_month'], 
    y=monthly_counts['count'], 
    mode='lines',
    name='Historical Data',
    line=dict(color='royalblue')
))

# Plot the forecasted data
fig.add_trace(go.Scatter(
    x=forecast_df['year_month'], 
    y=forecast_df['count'], 
    mode='lines', 
    line=dict(dash='dash', color='firebrick'),
    name='Forecast'
))

# Shade the forecast area
fig.add_shape(
    type="rect",
    x0=forecast_df['year_month'].min(), 
    x1=forecast_df['year_month'].max(), 
    y0=0, 
    y1=max(combined_df['count']),
    fillcolor="lightgray", 
    opacity=0.3, 
    line_width=0
)

# Directly label the forecast line
fig.add_annotation(
    x=forecast_df['year_month'].iloc[-1], 
    y=forecast_df['count'].iloc[-1],
    text='Forecast', 
    showarrow=True, 
    arrowhead=1
)

# Customize the layout
fig.update_layout(
    title='Trends in Homeless Management Information System (HMIS) Entry',
    yaxis_title='Number Processed',
    plot_bgcolor='white',  # Remove grey background
    showlegend=False  # Remove the legend
)

# save an html of the graph. 
fig.write_html( r'html\\better_line_chart.html', 
                   auto_open=True )


#(Easy) Build a visualization that illustrates the patterns in purchases by time of day for
# both the Front Street and Central locations. Feel free to limit your analysis to either
# working days (M-Th) or weekends (Fr-Su).

# Convert 'date' to datetime to extract day of the week
dram['date'] = pd.to_datetime(dram['date'])
dram['day_of_week'] = dram['date'].dt.day_name()

# Filter for the desired locations
filtered_locations = ["The Dram Shop Front St.", "The Dram Shop", "The Dram Shop Central"]
dram_filtered = dram[dram['location'].isin(filtered_locations)]

# Remove negative gross sales values
dram_filtered = dram_filtered[dram_filtered['gross_sales'] >= 0]

# Define a function to create and save the plot
def create_bar_chart(day_data, day_name, location):
    # Aggregate sales data by hour
    hourly_sales = day_data.groupby('hour')['gross_sales'].sum().reset_index()
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(hourly_sales['hour'], hourly_sales['gross_sales'], color='skyblue', edgecolor='black')
    plt.title(f'Sales by Hour for {day_name} at {location}', loc='left', fontsize=14)
    plt.xlabel('Hour', fontsize=12)
    plt.ylabel('Gross Sales', fontsize=12)
    
    # Remove grid lines for a minimalistic look
    plt.grid(False)
    plt.xticks(hourly_sales['hour'])
    
    # Remove top and right spines for a cleaner look
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Create a safe filename by replacing spaces and special characters
    safe_location = location.lower().replace(" ", "_").replace(".", "")
    safe_day_name = day_name.lower().replace(" ", "_")
    file_name = f'sales_by_hour_{safe_day_name}_{safe_location}.png'
    
    # Save the figure to the graphs folder
    plt.savefig(f'graphs/{file_name}')
    plt.close()

# Group data by location and then by day of the week
locations = dram_filtered['location'].unique()

for location in locations:
    location_data = dram_filtered[dram_filtered['location'] == location]
    days = location_data['day_of_week'].unique()
    
    for day in days:
        day_data = location_data[location_data['day_of_week'] == day]
        create_bar_chart(day_data, day, location)

print("Graphs have been saved to the 'graphs' folder.")

# look at the averages:

# Define a function to create and save the plot for average sales
def create_bar_chart(day_data, day_name, location):
    # Calculate average sales data by hour
    hourly_sales_avg = day_data.groupby('hour')['gross_sales'].mean().reset_index()
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(hourly_sales_avg['hour'], hourly_sales_avg['gross_sales'], color='skyblue', edgecolor='black')
    plt.title(f'Average Sales by Hour for {day_name} at {location}', loc='left', fontsize=14)
    plt.xlabel('Hour', fontsize=12)
    plt.ylabel('Average Gross Sales', fontsize=12)
    
    # Remove grid lines for a minimalistic look
    plt.grid(False)
    plt.xticks(hourly_sales_avg['hour'])
    
    # Remove top and right spines for a cleaner look
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Create a safe filename by replacing spaces and special characters
    safe_location = location.lower().replace(" ", "_").replace(".", "")
    safe_day_name = day_name.lower().replace(" ", "_")
    file_name = f'average_sales_by_hour_{safe_day_name}_{safe_location}.png'
    
    # Save the figure to the graphs folder
    plt.savefig(f'graphs/{file_name}')
    plt.close()

# Group data by location and then by day of the week
locations = dram_filtered['location'].unique()

for location in locations:
    location_data = dram_filtered[dram_filtered['location'] == location]
    days = location_data['day_of_week'].unique()
    
    for day in days:
        day_data = location_data[location_data['day_of_week'] == day]
        create_bar_chart(day_data, day, location)

print("Graphs for average sales by hour have been saved to the 'graphs' folder.")

# save 6 of the best 
# first filter to Friday, Saturday and Sund

# Filter for the desired locations and days
filtered_days = ["Friday", "Saturday", "Sunday"]
filtered_locations = ["The Dram Shop Central", "The Dram Shop Front St."]
dram_filtered = dram[
    (dram['day_of_week'].isin(filtered_days)) &
    (dram['location'].isin(filtered_locations)) &
    (dram['hour'] >= 11) &
    (dram['hour'] <= 24) &
    (dram['gross_sales'] >= 0)
]

# Define a function to create and save the plot for average sales
def create_filtered_bar_chart(day_data, day_name, location):
    # Calculate average sales data by hour
    hourly_sales_avg = day_data.groupby('hour')['gross_sales'].mean().reset_index()
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.bar(hourly_sales_avg['hour'], hourly_sales_avg['gross_sales'], color='skyblue', edgecolor='black')
    plt.title(f'Average Sales by Hour for {day_name} at {location}', loc='left', fontsize=14)
    plt.xlabel('Hour', fontsize=12)
    plt.ylabel('Average Sales', fontsize=12)
    
    # Remove grid lines for a minimalistic look
    plt.grid(False)
    plt.xticks(hourly_sales_avg['hour'])
    
    # Remove top and right spines for a cleaner look
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Create a safe filename by replacing spaces and special characters
    safe_location = location.lower().replace(" ", "_").replace(".", "")
    safe_day_name = day_name.lower().replace(" ", "_")
    file_name = f'filtered_average_sales_by_hour_{safe_day_name}_{safe_location}.png'
    
    # Save the figure to the graphs folder
    plt.savefig(f'graphs/{file_name}')
    plt.close()
    
    # Return the file name for tracking
    return file_name

# List to store filenames of the created graphs
file_names = []

# Group data by location and then by day of the week
locations = dram_filtered['location'].unique()

for location in locations:
    location_data = dram_filtered[dram_filtered['location'] == location]
    days = location_data['day_of_week'].unique()
    
    for day in days:
        day_data = location_data[location_data['day_of_week'] == day]
        file_name = create_filtered_bar_chart(day_data, day, location)
        file_names.append(file_name)

# Print the list of filenames for the next function
print("Generated filenames:")
print(file_names)
# Define the directory containing the saved graphs
graphs_folder = 'graphs'
output_image_path = 'graphs/combined_graphs.png'

# List of graph filenames to be combined (make sure these files exist in the directory)
graph_files = [
    'filtered_average_sales_by_hour_friday_the_dram_shop_front_st.png', 
    'filtered_average_sales_by_hour_saturday_the_dram_shop_front_st.png',
    'filtered_average_sales_by_hour_sunday_the_dram_shop_front_st.png',    
    'filtered_average_sales_by_hour_friday_the_dram_shop_central.png',
    'filtered_average_sales_by_hour_saturday_the_dram_shop_central.png',  
    'filtered_average_sales_by_hour_sunday_the_dram_shop_central.png'
]

# Open images and store them in a list
images = [Image.open(os.path.join(graphs_folder, file)) for file in graph_files]

# Determine the dimensions of the grid and each subplot
images_per_row = 3  # Number of images per row
images_per_column = 2  # Number of rows
image_width, image_height = images[0].size  # Assuming all images are the same size

# Calculate the total width and height for the combined image
# Extra height for the title
title_height = 120
total_width = image_width * images_per_row
total_height = image_height * images_per_column + title_height

# Create a new blank image with the total dimensions and a white background
combined_image = Image.new('RGB', (total_width, total_height), color='white')

# Draw the title
draw = ImageDraw.Draw(combined_image)
title = "Similar Weekend Business Patterns Across Locations"
title_font_size = 40

# Use a default PIL font for demonstration purposes
try:
    title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", title_font_size)  # Using a bold, default font
except IOError:
    title_font = ImageFont.load_default()

# Calculate title width and position to center it
title_width, title_height_actual = draw.textsize(title, font=title_font)
title_x = (total_width - title_width) // 2
title_y = (title_height - title_height_actual) // 2

# Draw the title onto the combined image
draw.text((title_x, title_y), title, font=title_font, fill='black')

# Paste each image into the combined image canvas in a grid layout
for idx, img in enumerate(images):
    # Calculate x and y position for each image
    x_offset = (idx % images_per_row) * image_width
    y_offset = title_height + (idx // images_per_row) * image_height
    
    # Paste the image into the combined image
    combined_image.paste(img, (x_offset, y_offset))

# Save the combined image
combined_image.save(output_image_path)
print(f"Combined image saved as {output_image_path}")

# (Medium) Build a visualization that attempts to answer this question: When do cars tend
# to be posted by location? Highlight an interesting feature of the data.

# store car data as 'data'
data = car
# Ensure 'time_posted' is in datetime format
data['time_posted'] = pd.to_datetime(data['time_posted'])

# Extract day of the week, day of the month, and hour of the day
data['day_of_week'] = data['time_posted'].dt.day_name()
data['day_of_month'] = data['time_posted'].dt.day
data['hour_of_day'] = data['time_posted'].dt.hour

# Ensure the HTML folder exists
os.makedirs('HTML', exist_ok=True)

# Plot 1: Histogram by Day of the Week
fig1 = px.histogram(data, x='day_of_week', title='Number of Postings by Day of the Week',
                    labels={'day_of_week':'Day of the Week', 'count':'Number of Postings'})
fig1.update_layout(xaxis_title="Day of the Week", yaxis_title="Number of Postings", template="plotly_white")
fig1.write_html('HTML/histogram_day_of_week.html')

# Plot 2: Histogram by Day of the Month
fig2 = px.histogram(data, x='day_of_month', title='Number of Postings by Day of the Month',
                    labels={'day_of_month':'Day of the Month', 'count':'Number of Postings'})
fig2.update_layout(xaxis_title="Day of the Month", yaxis_title="Number of Postings", template="plotly_white")
fig2.write_html('HTML/histogram_day_of_month.html')

# Plot 3: Histogram by Hour of the Day
fig3 = px.histogram(data, x='hour_of_day', title='Number of Postings by Hour of the Day',
                    labels={'hour_of_day':'Hour of the Day', 'count':'Number of Postings'})
fig3.update_layout(xaxis_title="Hour of the Day", yaxis_title="Number of Postings", template="plotly_white")
fig3.write_html('HTML/histogram_hour_of_day.html')

# Interactive Visual - Filter by Location and Unit of Time
fig4 = px.histogram(data, x='time_posted', color='location', title='Interactive Postings Histogram',
                    labels={'time_posted':'Time Posted', 'count':'Number of Postings'},
                    facet_row='day_of_week', facet_col='hour_of_day')
fig4.update_layout(xaxis_title="Time Posted", yaxis_title="Number of Postings", template="plotly_white")
fig4.write_html('HTML/interactive_histogram.html')

print("Histograms have been saved in the HTML folder.")