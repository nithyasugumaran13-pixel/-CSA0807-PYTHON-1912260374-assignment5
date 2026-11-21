# A1 – DESIGN THE DATA ACQUISITION

## A1.1 – Inspect the Source

### 1. Structure of the CSV File

The city pollution control board operates 12 air-quality monitoring stations. Each station sends a CSV file every day containing date, hour, PM2.5, PM10, NO2 and temperature readings.

The expected CSV structure is:

| Column Name | Description | Example |
|---|---|---|
| date | Date of reading | 2026-10-01 |
| hour | Hour of reading | 10 |
| PM2.5 | Fine particulate matter reading | 48.5 |
| PM10 | Particulate matter reading | 75.2 |
| NO2 | Nitrogen dioxide reading | 18.4 |
| temperature | Temperature reading | 32.5 |

The station name or station ID can be obtained from the source file name or station information maintained by the board.

### 2. Expected Data-Quality Problems

The following data-quality problems may occur in the collected CSV files:

1. **Missing Values:** Some readings may be blank or contain NA.
   Example: PM2.5 = NA.

2. **Negative Values:** Sensor faults may produce negative pollution readings.
   Example: PM10 = -10.

3. **Impossibly Large Values:** Faulty sensors may generate unusually large readings.
   Example: PM2.5 = 1500.

4. **Duplicate Records:** The same station may send the same date and hour reading more than once.
   Example: Two identical records for Adyar on 2026-10-01 at 10:00.

5. **Different Temperature Units:** Two stations report temperature in Fahrenheit instead of Celsius.
   Example: Temperature = 95°F.

6. **Incorrect Data Types:** Numeric readings may be stored as text.
   Example: PM2.5 = "48.5".

7. **Inconsistent Date or Time Formats:** Date and hour values may not follow a common format.
   Example: 01/10/2026 instead of 2026-10-01.

These problems must be identified and handled before analysis to ensure reliable results.

## A1.2 – Design the Storage

### 1. SQLite Database Design

SQLite is selected to store the air-quality monitoring data in a structured format.

Two tables are proposed:

**Table 1: Stations**

| Column | Data Type | Description |
|---|---|---|
| station_id | INTEGER | Primary key |
| station_name | TEXT | Name of the monitoring station |

**Table 2: Readings**

| Column | Data Type | Description |
|---|---|---|
| reading_id | INTEGER | Primary key |
| station_id | INTEGER | Foreign key referencing Stations |
| date | TEXT | Date of the reading |
| hour | INTEGER | Hour of the reading |
| pm25 | REAL | PM2.5 reading |
| pm10 | REAL | PM10 reading |
| no2 | REAL | NO2 reading |
| temperature_c | REAL | Temperature converted to Celsius |

A unique constraint on station_id, date and hour prevents duplicate readings for the same station and time.

### 2. Primary Key and Foreign Key

- station_id is the primary key in the Stations table.
- reading_id is the primary key in the Readings table.
- station_id in the Readings table is a foreign key referencing the Stations table.
- A unique constraint on station_id, date and hour helps prevent duplicate records.

### 3. Mapping CSV Columns to SQLite

| CSV Column | SQLite Column |
|---|---|
| Station information | station_id and station_name |
| date | date |
| hour | hour |
| PM2.5 | pm25 |
| PM10 | pm10 |
| NO2 | no2 |
| temperature | temperature_c |

The temperature values reported in Fahrenheit will be converted into Celsius before storing them in the database.

Conversion formula:

Celsius = (Fahrenheit - 32) × 5 / 9

The date will be stored in YYYY-MM-DD format, and numeric readings will be stored using REAL data types.

## A1.3 – CSV or SQL?

### 1. Comparison Using Three Board Questions

**Question 1: What is the average PM2.5 reading at Adyar station in October?**

- CSV approach: Read the relevant CSV files, filter Adyar records for October, add the valid PM2.5 values and calculate their average.
- SQL approach: Use SELECT, AVG() and WHERE conditions to calculate the average directly from the Readings and Stations tables.

**Question 2: Which station recorded the highest PM10 reading on a particular day?**

- CSV approach: Read the files from all stations, compare their PM10 readings for the selected date and identify the highest value.
- SQL approach: Use ORDER BY PM10 DESC and LIMIT 1 to retrieve the highest reading.

**Question 3: How many valid readings were recorded by each station in October?**

- CSV approach: Read the files, count valid readings for each station and maintain separate counters.
- SQL approach: Use COUNT() and GROUP BY station_id to calculate the reading count for each station.

### 2. CSV and SQL Comparison

| Feature | CSV Files | SQLite Database |
|---|---|---|
| Storage | Plain text files | Structured database |
| Searching | Requires reading and filtering files | Supports SQL queries |
| Filtering | Performed using program logic | Performed using WHERE |
| Grouping | Requires loops or libraries | Supports GROUP BY |
| Indexing | No built-in database index | Supports indexes |
| Data consistency | More difficult to maintain | Supports constraints |
| Best use | Simple data exchange | Repeated queries and structured storage |

### 3. Alternative Concept: Pandas DataFrame Instead of SQLite

If the data were kept only in CSV files, the programmer could load the files into a pandas DataFrame whenever a question needs to be answered.

The DataFrame can filter, group and calculate averages using pandas operations.

However, loading and processing the data repeatedly may take more time and memory as the dataset grows.

### 4. Time and Space Complexity

**CSV and Pandas Approach:**

- Reading and scanning n records generally takes O(n) time per question.
- Loading the data into a DataFrame requires memory proportional to the dataset, approximately O(n).
- Repeated loading increases processing time.

**SQLite Approach:**

- Without an index, searching may require O(n) time.
- With a suitable index, searching can take approximately O(log n) time, depending on the query and index.
- Data is stored on disk, reducing the need to load the entire dataset into memory for every query.

### 5. Conclusion

SQLite is a suitable choice for the city's air-quality monitoring system because it stores data in structured tables and supports filtering, grouping and repeated queries. CSV files are useful for receiving and exchanging data, while SQLite provides more efficient management and retrieval for ongoing analysis. Therefore, the proposed system will acquire data from CSV files, clean it and store the valid readings in SQLite.