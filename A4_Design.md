# A4 – Debugging and Profiling Plan

## A4.1 Debugging Plan (2 Marks)

Debugging is the process of identifying and correcting errors in a program. In the air-quality data cleaning pipeline, debugging helps detect problems such as missing values, invalid sensor readings, duplicate records, incorrect temperature conversion, and database errors.

The following debugging techniques can be used:

### 1. Print Statements

Print statements display intermediate values during program execution.

**Example:**
```python
print("Original readings:", readings)
print("Cleaned readings:", cleaned_readings)
print("Invalid readings:", invalid_readings)
```

**Purpose:** They help compare original and cleaned data and identify where incorrect values appear.

### 2. Assert Statements

Assert statements check whether a condition is true. If the condition is false, Python raises an AssertionError.

**Example:**
```python
assert pm25 >= 0, "PM2.5 cannot be negative"
assert 0 <= hour <= 23, "Invalid hour"
```

**Purpose:** They help detect invalid sensor values and incorrect data formats during testing.

### 3. Logging Module

The logging module records program information, warnings, and errors. It is more suitable than using many print statements in large applications.

**Example:**
```python
import logging

logging.basicConfig(level=logging.INFO)

logging.info("Data cleaning started")
logging.warning("Missing PM2.5 value detected")
logging.error("Unable to load input file")
```

**Purpose:** It provides a record of important events and helps identify errors without displaying every intermediate value.

### 4. PDB or VS Code Debugger

The Python debugger (`pdb`) or VS Code debugger can be used to execute the program step by step.

Important debugging features include:
- Breakpoints: Pause execution at a selected line.
- Step Over: Execute the current line and move to the next line.
- Step Into: Enter a function to inspect its execution.
- Variable Inspection: Check the values stored in variables.
- Continue: Resume program execution.

**Purpose:** These features help identify the exact statement where incorrect data or unexpected behaviour occurs.

### Debugging Procedure

1. Load the air-quality CSV file.
2. Inspect the original records.
3. Check for missing and invalid values.
4. Verify duplicate removal.
5. Check Fahrenheit-to-Celsius conversion.
6. Verify the cleaned records before storing them in SQLite.
7. Use assertions to confirm that the cleaned data follows the expected rules.

## A4.2 Profiling Plan (2 Marks)

Profiling measures the execution time and performance of a program. It helps identify which part of the air-quality data pipeline takes the most time.

The following tools can be used:

### 1. time.perf_counter()

`time.perf_counter()` measures the elapsed execution time of a particular operation.

**Example:**
```python
import time

start = time.perf_counter()

# Execute the cleaning operation

end = time.perf_counter()

print("Execution time:", end - start, "seconds")
```

**Purpose:** It can measure the time required for CSV loading, data cleaning, and database insertion.

### 2. timeit

The `timeit` module measures how long a small section of code takes to execute. It can repeat the operation several times to obtain a more reliable timing result.

**Example:**
```python
import timeit

execution_time = timeit.timeit(
    "sum(range(1000))",
    number=1000
)

print("Total execution time:", execution_time)
```

**Purpose:** It can compare different methods of processing or calculating air-quality readings.

### 3. cProfile

The `cProfile` module analyses the execution time of different functions in a Python program.

**Example:**
```python
import cProfile

def clean_data():
    # Data cleaning operations
    pass

cProfile.run("clean_data()")
```

**Purpose:** It identifies functions that consume the most execution time and helps locate performance bottlenecks.

## Alternative Approach: Print Statements vs Logging and Debugger

Using print statements for every debugging operation is simple, but it becomes inefficient when processing thousands of sensor readings.

| Method | Advantages | Disadvantages |
|---|---|---|
| Print statements | Easy to use and understand | Produces excessive output |
| Logging | Supports different message levels and can write to a file | Requires configuration |
| Debugger | Allows step-by-step inspection | May take more time for manual debugging |

### Time and Performance Considerations

When thousands of print statements are executed, displaying output repeatedly can increase execution time and make the terminal difficult to inspect.

Logging can also introduce some overhead, especially when many messages are written to a file. However, logging levels can control which messages are recorded.

### Switching Off Debugging

- Print statements can be removed or commented out after testing.
- Logging can be disabled or reduced by changing the logging level.
- Debugger breakpoints can be removed or disabled after the errors are corrected.
- Assertions can remain during testing and validation; they can be disabled when Python is executed with optimization mode, but important data validation should still be performed explicitly.

## Conclusion

Debugging helps identify and correct errors in the data cleaning pipeline, while profiling identifies performance bottlenecks. Using print statements, assertions, logging, a debugger, `time.perf_counter()`, `timeit`, and `cProfile` makes the air-quality data processing system more reliable and efficient.