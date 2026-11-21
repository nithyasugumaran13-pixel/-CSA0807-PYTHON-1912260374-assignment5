# A3 – DESIGN THE ANALYSIS AND VISUALISATION

## A3.1 – Choose the Charts

The air-quality monitoring system collects PM2.5, PM10, NO2 and temperature readings from 12 monitoring stations. Charts are required to understand pollution trends, compare stations and identify periods of poor air quality.

The following chart types are selected for the board's questions.

### 1. Monthly Trend of PM2.5

**Selected Chart: Line Chart**

**Description:**

A line chart will be used to display the daily average PM2.5 readings over one month.

- X-axis: Date
- Y-axis: Average PM2.5 reading

**Justification:**

A line chart is suitable for time-based data because it connects daily readings in chronological order. It helps the board identify increasing or decreasing pollution trends and sudden changes during the month.

### 2. Comparison of Pollution Across Stations

**Selected Chart: Bar Chart**

**Description:**

A bar chart will compare the average PM2.5 readings recorded by different monitoring stations.

- X-axis: Station names
- Y-axis: Average PM2.5 reading

**Justification:**

A bar chart makes it easy to compare pollution levels across different stations. The board can identify stations with higher average PM2.5 readings and determine which areas may require attention.

### 3. Relationship Between Temperature and PM2.5

**Selected Chart: Scatter Plot**

**Description:**

A scatter plot will display the relationship between temperature and PM2.5 readings.

- X-axis: Temperature in Celsius
- Y-axis: PM2.5 reading

**Justification:**

A scatter plot helps identify whether temperature and PM2.5 readings show a possible relationship. A visible upward or downward pattern may indicate a positive or negative association. However, correlation does not necessarily mean that one variable causes the other.

### 4. Identification of the Hours with the Worst Air Quality

**Selected Chart: Bar Chart**

**Description:**

A bar chart will display the average PM2.5 reading for each hour of the day.

- X-axis: Hour of the day (0–23)
- Y-axis: Average PM2.5 reading

**Justification:**

A bar chart helps identify the hours with the highest average PM2.5 readings. The board can use this information to understand when pollution levels are generally higher and plan further monitoring.

### Summary of Chart Selection

| Board's Question | Selected Chart | Purpose |
|---|---|---|
| Monthly PM2.5 trend | Line Chart | Identify changes over time |
| Compare monitoring stations | Bar Chart | Compare average pollution levels |
| Temperature and PM2.5 relationship | Scatter Plot | Identify possible relationships |
| Worst pollution hours | Bar Chart | Identify high-pollution hours |

## A3.2 – Design the Summary Table

### 1. Purpose of the Summary Table

A daily summary table will be created to provide a quick overview of air-quality readings recorded by each monitoring station.

The table will contain the minimum, maximum and mean PM2.5 readings, along with the number of valid readings recorded for each station on a particular day.

### 2. Proposed Daily Summary Table

**Table Name: Daily_Pollution_Summary**

| Column Name | Data Type | Description |
|---|---|---|
| station_id | INTEGER | Monitoring station identifier |
| date | TEXT | Date of the readings |
| min_pm25 | REAL | Minimum valid PM2.5 reading |
| max_pm25 | REAL | Maximum valid PM2.5 reading |
| mean_pm25 | REAL | Average PM2.5 reading |
| valid_readings | INTEGER | Number of valid PM2.5 readings |

The combination of station_id and date can be used as a composite primary key because each station should have one daily summary for a particular date.

### 3. Method of Producing the Summary

The daily summary will be generated using SQL aggregate functions.

The following operations will be performed:

1. Retrieve valid PM2.5 readings from the Readings table.
2. Group the records by station_id and date.
3. Calculate the minimum reading using MIN().
4. Calculate the maximum reading using MAX().
5. Calculate the average reading using AVG().
6. Count the valid readings using COUNT().
7. Store or display the results in the Daily_Pollution_Summary table.

### 4. Example Summary

| Station | Date | Minimum | Maximum | Mean | Valid Readings |
|---|---|---:|---:|---:|---:|
| Adyar | 2026-10-01 | 20 | 60 | 40 | 24 |
| Guindy | 2026-10-01 | 25 | 75 | 50 | 24 |
| T Nagar | 2026-10-01 | 15 | 55 | 35 | 24 |

The above values are illustrative examples used to demonstrate the summary-table structure.

### 5. Alternative Concept: Python Loops Instead of SQL GROUP BY

If SQL GROUP BY were not used, the program could read all valid records into Python and calculate daily statistics using loops.

**Python Loop Approach:**

1. Read the records from the database or CSV file.
2. Create a dictionary using station ID and date as the key.
3. Maintain the minimum, maximum, total and count for each group.
4. Calculate the mean using total divided by count.
5. Display or store the resulting summary.

**SQL GROUP BY Approach:**

SQL can directly group the records by station and date and calculate MIN(), MAX(), AVG() and COUNT() using aggregate functions.

### 6. Time and Space Complexity Comparison

Let n represent the total number of readings and g represent the number of station-date groups.

| Feature | Python Loops | SQL GROUP BY |
|---|---|---|
| Time complexity | O(n) for one-pass aggregation | Typically O(n) for a full grouping operation; may vary with indexes and query plan |
| Extra memory | O(g) for the aggregation dictionary | Database-managed memory, depending on the query plan |
| Processing | Performed in Python | Performed by SQLite |
| Result | Daily summary values | Daily summary values |

**Explanation:**

The Python loop approach processes each reading and updates the corresponding group in a dictionary. It requires memory to maintain the summary information for each group.

The SQL GROUP BY approach performs aggregation inside the database. It avoids transferring every reading into Python just to calculate the summary. SQLite manages the resources needed for grouping and may use temporary storage depending on the query plan.

### Conclusion

Line charts, bar charts and scatter plots are selected to represent different aspects of air-quality data. The daily summary table provides important statistical information for each station. SQL GROUP BY is selected as the main approach because the readings are stored in SQLite and the database can perform the required aggregation efficiently.