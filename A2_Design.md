# A2 – DESIGN THE CLEANING AND NORMALISATION

## A2.1 – Cleaning Rules

The air-quality data collected from different monitoring stations may contain missing values, incorrect readings, duplicate records and different temperature units. Cleaning is necessary before storing and analysing the data.

### 1. Handling Missing Values

Missing values may appear as blank fields or NA in the CSV file.

**Rule:**
- For a short missing gap, use the previous valid reading from the same station and same measurement, provided the previous reading is recent.
- If a previous value is not available, use the median reading of the same station for that measurement, calculated from valid observations.
- If neither method is reliable, leave the reading missing and exclude it from calculations.

**Justification:**

Using a previous value can help handle short sensor interruptions. The median is less affected by unusually high or low readings than the mean. However, filling should not be used when it may hide a sudden pollution change.

### 2. Handling Impossible Values

**Rule:**
- Identify negative pollution readings and readings outside the valid sensor or domain limits.
- Reject readings that are physically impossible or exceed the accepted sensor range.
- Do not replace an invalid reading with an arbitrary value.

**Justification:**

Negative pollution readings and faulty extremely large values can distort averages and charts. Removing invalid readings helps maintain reliable analysis. The accepted limits should be based on sensor specifications and domain rules.

### 3. Removing Duplicate Records

**Rule:**
- Identify duplicate records using station ID, date and hour.
- Keep only one valid record for each station and time.
- If duplicate records contain conflicting values, retain the record that passes validation and has the most reliable source information. If reliability cannot be established, flag the record for review.

**Justification:**

Duplicate readings can increase the reading count and produce incorrect daily averages. Removing duplicates ensures that each station contributes only one reading for a particular time.

### 4. Converting Fahrenheit to Celsius

Two monitoring stations report temperature in Fahrenheit instead of Celsius.

**Rule:**

Convert Fahrenheit readings into Celsius using the formula:

Celsius = (Fahrenheit - 32) × 5 / 9

**Example:**

If the temperature is 95°F:

Celsius = (95 - 32) × 5 / 9

Celsius = 35°C

**Justification:**

All temperature readings must use the same unit before comparison and analysis. Converting Fahrenheit to Celsius provides consistent temperature data across all stations.

## A2.2 – Normalisation

Normalisation and standardisation are used to transform PM2.5 readings into comparable numerical values for analysis.

### 1. Min–Max Normalisation

Min–max normalisation scales PM2.5 readings into a range between 0 and 1.

**Formula:**

Normalized Value = (X - Xmin) / (Xmax - Xmin)

Where:

- X = Original PM2.5 reading
- Xmin = Minimum PM2.5 reading
- Xmax = Maximum PM2.5 reading

**Example:**

Consider PM2.5 readings:

10, 30, 50

Minimum = 10

Maximum = 50

For the reading 30:

Normalized Value = (30 - 10) / (50 - 10)

Normalized Value = 20 / 40 = 0.5

The normalised values are:

0.0, 0.5, 1.0

**When is it appropriate?**

Min–max normalisation is appropriate when values need to be converted into a fixed range, especially when comparing measurements with different scales. It is sensitive to extreme values because the minimum and maximum determine the range.

If all readings are equal, the denominator becomes zero. In that case, the system should handle the values separately rather than divide by zero.

### 2. Z-Score Standardisation

Z-score standardisation transforms PM2.5 readings based on their mean and standard deviation.

**Formula:**

Z = (X - Mean) / Standard Deviation

Where:

- X = Original PM2.5 reading
- Mean = Average of PM2.5 readings
- Standard Deviation = Measure of variation in the readings

**Example:**

Consider PM2.5 readings:

10, 20, 30

Mean = 20

Population Standard Deviation ≈ 8.165

For the reading 30:

Z = (30 - 20) / 8.165

Z ≈ 1.225

**When is it appropriate?**

Z-score standardisation is useful when analysing how far a reading is from the average. It is useful for identifying unusual readings and preparing data for certain statistical and machine-learning methods.

If the standard deviation is zero, the values should be handled separately because division by zero is not possible.

### 3. Comparison of Both Methods

| Feature | Min–Max Normalisation | Z-Score Standardisation |
|---|---|---|
| Transformation | Scales values | Centres and scales values |
| Result | Usually between 0 and 1 | Can be negative or positive |
| Uses | Minimum and maximum | Mean and standard deviation |
| Suitable for | Fixed-range comparison | Statistical analysis |
| Sensitivity | Sensitive to extreme values | Also affected by extreme values |

## A2.3 – Formatting

To maintain consistency, the cleaned data will follow standard formats.

### 1. Date Format

All dates will be stored in:

YYYY-MM-DD

Example: 2026-10-01

This format avoids confusion between different date representations.

### 2. Station Name Format

- Station names will use consistent spelling.
- Leading and trailing spaces will be removed.
- Station names will follow a consistent naming convention.

Examples:

- Adyar
- Guindy
- T Nagar

Station names will be matched with the station records in the database.

### 3. Number Format

- PM2.5, PM10, NO2 and temperature will be stored as numeric values.
- Floating-point measurements will use the REAL data type in SQLite.
- Missing values will be represented as NULL in the database if they cannot be reliably filled.
- Temperature will always be stored in Celsius.
- The hour will use the integer format from 0 to 23.

## Alternative Concept and Complexity Analysis

### Dropping Missing Readings Instead of Filling Them

If missing readings were dropped instead of being filled with previous values or the median, the cleaning process would simply remove records that do not contain valid measurements.

**1. Effect on Daily Averages**

- Dropping missing readings reduces the number of available observations.
- If many readings are missing, daily averages may become less representative.
- If the missing readings are not random, the calculated average may be biased.
- Filling short gaps can preserve more observations, but may hide real changes in pollution.

Therefore, the method should be selected based on the amount of missing data and the reliability of the replacement value.

**2. Time Complexity**

| Method | Time Complexity | Explanation |
|---|---|---|
| Dropping missing values | O(n) | Each reading is checked once |
| Forward filling | O(n) | Readings are checked in sequence |
| Computing median by sorting | O(n log n) | Values are sorted before finding the median |

Here, n represents the number of readings.

**3. Space Complexity**

- Dropping values can be performed with O(1) extra space if the data is processed in place, excluding the output storage.
- Forward filling requires only the previous valid value, so it uses O(1) extra space in a streaming process.
- Computing a median may require O(n) additional space to store the valid readings, depending on the implementation.

### Conclusion

The proposed cleaning method handles missing readings, impossible values, duplicates and temperature-unit differences before analysis. Min–max normalisation is useful for scaling values into a fixed range, while z-score standardisation is useful for statistical analysis. Standard date, station-name and numeric formats help maintain consistency throughout the air-quality monitoring system.