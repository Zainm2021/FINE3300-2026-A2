# FINE3300 Assignment 2: CPI Inflation Calculator

## Overview
This repository contains my FINE3300 Assignment 2. The assignment includes a Python inflation calculator that uses the Bank of Canada's monthly Consumer Price Index (CPI) data to replicate the [Bank of Canada Inflation Calculator](https://www.bankofcanada.ca/rates/related/inflation-calculator/). It also creates a graph of the CPI and its annual percentage change from 1914 to 2026.
 
The Bank of Canada's calculator only lets users enter a year, even though the CPI data is recorded monthly. I enhanced the calculator so that users enter a full date (month and year) for each period, which allows for more precise comparisons. By using a class called `InflationCalculator` I was able to read the data, calculate the results and create the graph.

## Files
1. InflationCalculator.py : The Python code for the calculator and the graph 
2. STATIC_INFLATIONCALC.csv : Bank of Canada monthly CPI data (1914-01 to 2026-09), downloaded in CSV format from the Inflation Calculator page
3. CPI_and_Annual_Inflation_Graph.png : The CPI graph created by the program 
4. README.md : This write-up 

## How It Works

### The InflationCalculator Class
I created a class named `InflationCalculator` that reads the Bank of Canada CPI file into a Pandas data frame. The first 8 lines of the file are notes from the Bank of Canada rather than data, so they are skipped. The data frame is stored as a private member so it can only be accessed through the class's methods.

### The get_cpi and is_valid_date methods
The `get_cpi` method takes a month and year, builds a date in the same format as the data file (e.g. `2002-01-01`), filters the data frame down to that row and returns the CPI value. The `is_valid_date` method checks whether a date entered by the user exists in the data set, which confirms that the date is both in the correct format and within the data range.

### The calculate_inflation method
This method uses the CPI for both dates to produce the same results as the Bank of Canada calculator, using the same equations shown on the Bank of Canada's website:
- **Equivalent cost:** Cost₂ = Cost₁ × (CPI₂ / CPI₁)
- **Percentage change:** ((Cost₂ − Cost₁) / Cost₁) × 100
- **Number of years:** the total number of months between the two dates divided by 12 (e.g. January 2020 to July 2022 is 2.5 years)
- **Average annual rate of inflation:** found by solving CPI₂ = CPI₁ × (1 + rate)^years for the rate
All of the results are returned in a dictionary so each value can be accessed by name.

### The plot_cpi method
This method uses Matplotlib to graph the CPI on the left axis and the annual percentage change on the right axis, with a dotted line through the base level. The annual percentage change compares each month to the same month one year earlier. It also uses NumPy to calculate the average annual inflation rate over the whole data set. The graph is saved as `CPI_and_Annual_Inflation_Graph.png`.

### User Input and Validation
Outside of the class, the `get_cost` and `get_date` functions prompt the user for the cost and the two dates. Both functions keep asking until a valid input is entered:
- **Cost:** dollar signs, commas and spaces are accepted (e.g. `$1,234.56` or `1 000`). Letters, symbols, more than one decimal point, zero and negative numbers are rejected.
- **Dates:** must be entered as `YYYY-MM` and must be between `1914-01` and `2026-09`. The month and year are then extracted from the date.
- The two dates cannot be the same, since the number of years would be zero.


## How to Run
1. Clone this repository
2. Install the required libraries: `pip install numpy pandas matplotlib`
3. Open the folder in Visual Studio Code
4. Run `InflationCalculator.py`
5. Enter the cost, then the first and second dates in the format `YYYY-MM` when prompted
6. The results are displayed, and then the CPI graph opens in a new window. Close the graph window to end the program.

Dates can be entered in either order. If the second date is before the first, the percentage change, number of years and annual rate are negative, the same as the Bank of Canada calculator.

## CPI Graph
<img width="1000" height="500" alt="Figure_1" src="https://github.com/user-attachments/assets/84d18db9-9a69-42de-be56-c367989feef7" />

 
### Commentary
The CPI measures the price of a fixed basket of goods and services (such as food, shelter, clothing and transportation) relative to a base period. Statistics Canada uses 2002 as the base year, so the average CPI in 2002 equals 100. The dotted line on the graph marks this base level: values below 100 mean prices were lower than in 2002, and values above 100 mean prices were higher. In September 2026 the CPI was 170.0, meaning prices were about 70% higher than in 2002.
 
Some interesting parts of the graph:
- **World War I:** inflation rose sharply, peaking at about 21.6% in mid-1920.
- **Deflation in the 1920s and 1930s:** prices fell by about 17.8% in 1921 after the war, and again during the Great Depression, with annual inflation reaching about −12.0% in 1931.
- **After World War II:** inflation spiked to about 17.5% in 1948, and again to about 13.0% in 1951.
- **The 1970s and early 1980s:** inflation stayed high for over a decade, peaking at about 12.9% in 1981. This is also when the CPI line starts rising steeply.
- **Stability since the early 1990s:** after the Bank of Canada began targeting inflation in 1991, inflation stayed close to 2%, averaging about 1.76% from 1992 to 2020.
- **The 2022 spike:** inflation rose to about 8.1% in mid-2022 after the COVID-19 pandemic, the highest in about 40 years.
Using NumPy, the average annual inflation rate over the whole data set (1915–2026) is about **3.13%**.
 
## Sample Output
**Example 1: $100 from September 2002 to September 2025**
```
Enter the cost of the goods or services: 100
Enter the first date (YYYY-MM): 2002-09
Enter the second date (YYYY-MM): 2025-09
 
Results
$100.00 CAD in 2002-09 is equivalent to $163.43 CAD in 2025-09
Percentage change: 63.43%
Number of years: 23.00
Average annual rate of inflation: 2.16%
CPI in first period: 100.9
CPI in second period: 164.9
2002 CPI = 100.0
Average annual inflation rate (1915-2026): 3.13%
```
 
**Example 2: the same dates in reverse (going back in time)**
```
Enter the cost of the goods or services: 100
Enter the first date (YYYY-MM): 2025-09
Enter the second date (YYYY-MM): 2002-09
 
Results
$100.00 CAD in 2025-09 is equivalent to $61.19 CAD in 2002-09
Percentage change: -38.81%
Number of years: -23.00
Average annual rate of inflation: -2.11%
CPI in first period: 164.9
CPI in second period: 100.9
2002 CPI = 100.0
Average annual inflation rate (1915-2026): 3.13%
```
 
**Example 3: input validation**
```
Enter the cost of the goods or services: abc
Invalid input. Please enter a number.
Enter the cost of the goods or services: 0
Invalid input. The cost must be greater than zero.
Enter the cost of the goods or services: $1,250.50
Enter the first date (YYYY-MM): 2002/01
Invalid date. Please use the format YYYY-MM, between 1914-01 and 2026-09.
Enter the first date (YYYY-MM): 1900-01
Invalid date. Please use the format YYYY-MM, between 1914-01 and 2026-09.
Enter the first date (YYYY-MM): 2002-01
Enter the second date (YYYY-MM): 2002-01
The second date must be different from the first date.
Enter the second date (YYYY-MM): 2026-09
 
Results
$1,250.50 CAD in 2002-01 is equivalent to $2,178.12 CAD in 2026-09
Percentage change: 74.18%
Number of years: 24.67
Average annual rate of inflation: 2.28%
CPI in first period: 97.6
CPI in second period: 170.0
2002 CPI = 100.0
Average annual inflation rate (1915-2026): 3.13%
```
 
## Data Notes
- The CSV file begins with 8 lines of Bank of Canada notes (terms and conditions and the series description) before the data, so these lines are skipped when reading the file.
- The data is monthly and recorded on the 1st of each month. The file contains two irregular entries (1927-04-30 and 1932-04-30), which were excluded so that each month appears only once. This matters for the graph, since the annual percentage change compares each month to the row 12 positions earlier.

## References
- Bank of Canada, [Inflation Calculator](https://www.bankofcanada.ca/rates/related/inflation-calculator/) (data source and equations)
- Bank of Canada, [Understanding the consumer price index](https://www.bankofcanada.ca/2021/05/understanding-consumer-price-index/)
- Statistics Canada, [Consumer price indexes](https://www.statcan.gc.ca/en/subjects-start/prices_and_price_indexes/consumer_price_indexes)
- [Pandas documentation](https://pandas.pydata.org/docs/) (`read_csv` with `skiprows`, `to_datetime`, `pct_change`)
- [Matplotlib documentation](https://matplotlib.org/stable/) (`twinx`, `axhline`, `get_legend_handles_labels`)
 
