'''
This is my FINE3300 Assignment 2
Below is my CPI inflation calculator that uses the Bank of Canada's monthly Consumer Price Index (CPI) data
to find what a price in one month and year is worth in another month and year. It also graphs the CPI and
its annual percentage change from 1914 to 2026.
'''

# Imports pandas to read the CSV file, matplotlib to create the graph and numpy for calculations
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Creates the class InflationCalculator which reads the data file and extracts CPI information from it 
class InflationCalculator:
    # Reads the CPI data file and stores it as a private data frame
    def __init__(self, file_name):
        # The first 8 lines of the file are Bank of Canada notes, not data, so they are skipped
        self.__data = pd.read_csv(file_name, skiprows=8)
        
        # The data is monthly and recorded on the 1st of each month, so only rows where
        # the day (characters 9 and 10 of the date, e.g. '2002-01-01') is '01' are kept
        first_of_month = [date[8:10] == '01' for date in self.__data['date']]
        self.__data = self.__data[first_of_month]


    # Checks if a date entered as YYYY-MM exists in the data set
    # Adding '-01' matches the format of the data file, so a date in the wrong format
    # or outside of the data range will not be found and is therefore invalid
    def is_valid_date(self, date):
        return date + '-01' in list(self.__data['date'])


    # Looks up the CPI value for a specific month and year
    def get_cpi(self, month, year):
        # Builds the date in the same format as the data file, e.g. month 1 and year 2002 becomes '2002-01-01'
        date_string = "{}-{:02d}-01".format(year, month)

        # Filters the data frame down to the row with the matching date, then takes the CPI value from that row
        cpi = self.__data[self.__data['date'] == date_string]['STATIC_INFLATIONCALC'].iloc[0]
        return cpi


    # Calculates inflation the same way as the Bank of Canada inflation calculator, using months and years
    def calculate_inflation(self, cost, month1, year1, month2, year2):
        # Gets the CPI level for both dates
        cpi1 = self.get_cpi(month=month1, year=year1)
        cpi2 = self.get_cpi(month=month2, year=year2)

        # The cost in the second period grows (or shrinks) by the same ratio as the CPI
        equivalent_cost = cost * (cpi2 / cpi1)

        # Total percentage change in prices between the two dates
        percentage_change = ((equivalent_cost - cost) / cost) * 100

        # Counts the total number of months between the dates and converts it to years
        # e.g. January 2020 to July 2022 is 30 months, which is 2.5 years
        months_between = (year2 - year1) * 12 + (month2 - month1)
        years_between = months_between / 12

        # Average annual rate, found by solving cpi2 = cpi1 * (1 + rate) ** years for the rate
        # abs makes the number of years positive, so going back in time gives a negative rate like the Bank of Canada calculator
        average_annual_rate = ((cpi2 / cpi1) ** (1 / abs(years_between)) - 1) * 100

        # Returns all of the results in a dictionary so each value can be accessed by name
        return {
            'cost': cost,
            'equivalent_cost': equivalent_cost,
            'percentage_change': percentage_change,
            'years_between': years_between,
            'average_annual_rate': average_annual_rate,
            'cpi1': cpi1,
            'cpi2': cpi2}


    # Creates a graph of the CPI and its annual percentage change, then saves it as a png file
    def plot_cpi(self):
        # Converts the date column from text to real dates so the x-axis is spaced by year
        dates = pd.to_datetime(self.__data['date'])

        # Annual percentage change compares each month to the same month one year (12 rows) earlier
        annual_percentage_change = self.__data['STATIC_INFLATIONCALC'].pct_change(periods=12) * 100

        # Uses NumPy to find the average annual inflation rate over the whole data set
        average_inflation = np.mean(annual_percentage_change)
        print("Average annual inflation rate (1915-2026): " + format(average_inflation, '.2f') + "%")

        # Creates the figure and axes, tight layout stops the right axis label from being cut off
        fig, ax = plt.subplots(figsize=(10, 5), layout='tight')

        # Plots the CPI on the left y-axis
        ax.plot(dates, self.__data['STATIC_INFLATIONCALC'], label='CPI', color='tab:blue')
        ax.set_xlabel('Year')
        ax.set_ylabel('CPI (2002=100)')
        ax.set_title('Canada Consumer Price Index and Annual Inflation Rate (1914-2026)', fontsize=15)

        # Dotted line through the base level, where the CPI equals 100 (the 2002 average)
        ax.axhline(y=100, linestyle=':', color='tab:grey', label='Base Level (2002 = 100)')

        # twinx creates a second y-axis on the right that shares the same x-axis
        ax2 = ax.twinx()
        ax2.plot(dates, annual_percentage_change, label='Annual % Change', color='tab:orange')
        ax2.set_ylabel('Annual % Change')

        # Combines the legends from both axes into one, so the orange line cannot cover the legend
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='lower right')

        # Saves the graph before showing it, otherwise the saved image can be blank
        fig.savefig('cpi_graph.png')

        # Displays the graph, the program pauses here until the window is closed
        plt.show()


# Asks the user for the cost and keeps asking until a valid positive number is entered
def get_cost():
    while True:
        cost = input("Enter the cost of the goods or services: ")

        # Removes dollar signs, commas and spaces so inputs like $1,234.56 or 1 000 are accepted
        cost = cost.replace('$', '').replace(',', '').replace(' ', '')

        # Checks every character to make sure the input only contains digits and at most one decimal point
        valid = True
        decimal_points = 0
        for character in cost:
            if character == '.':
                decimal_points = decimal_points + 1
            elif character not in '0123456789':
                valid = False

        # Rejects letters or symbols, more than one decimal point, or an empty input
        if valid == False or decimal_points > 1 or cost == '' or cost == '.':
            print("Invalid input. Please enter a number.")
            continue

        # Converts the cleaned text into a number now that it is known to be valid
        cost = float(cost)
        
        # The cost must be greater than zero to calculate a meaningful result
        if cost <= 0:
            print("Invalid input. The cost must be greater than zero.")
            continue

        return cost


# Asks the user for a date in the format YYYY-MM and returns the month and year as integers
def get_date(prompt, calculator):
    while True:
        # The strip method ensures that any spaces entered with the date are ignored
        date = input(prompt).strip()

        # Keeps asking until the date is in the correct format and inside the data range
        if not calculator.is_valid_date(date):
            print("Invalid date. Please use the format YYYY-MM, between 1914-01 and 2026-09.")
            continue

        # Extracts the year (first 4 characters) and month (characters 6 and 7) from the date
        year = int(date[0:4])
        month = int(date[5:7])
        return month, year


if __name__ == "__main__":
    # Instantiates an InflationCalculator object that references the Bank of Canada CPI data file
    calculator = InflationCalculator(file_name='STATIC_INFLATIONCALC.csv')

    # Prompts the user for the cost and the two dates
    cost = get_cost()
    month1, year1 = get_date(prompt="Enter the first date (YYYY-MM): ", calculator=calculator)
    month2, year2 = get_date(prompt="Enter the second date (YYYY-MM): ", calculator=calculator)

    # The two dates must be different, otherwise the number of years is 0 and the annual rate cannot be calculated
    while month1 == month2 and year1 == year2:
        print("The second date must be different from the first date.")
        month2, year2 = get_date(prompt="Enter the second date (YYYY-MM): ", calculator=calculator)

    # Passes the user's inputs into calculate_inflation to calculate the results
    results = calculator.calculate_inflation(cost=cost, month1=month1, year1=year1, month2=month2, year2=year2)

    # Displays the results, rounded to the nearest penny with dollar signs and currency identifiers
    print()
    print("Results")
    print("$" + format(results['cost'], ',.2f') + " CAD in " + str(year1) + "-" + format(month1, '02') +
          " is equivalent to $" + format(results['equivalent_cost'], ',.2f') + " CAD in " +
          str(year2) + "-" + format(month2, '02'))
    print("Percentage change: " + format(results['percentage_change'], '.2f') + "%")
    # Number of years is negative when the second date is before the first, matching the Bank of Canada calculator
    print("Number of years: " + format(results['years_between'], '.2f'))
    print("Average annual rate of inflation: " + format(results['average_annual_rate'], '.2f') + "%")
    print("CPI in first period: " + format(results['cpi1'], '.1f'))
    print("CPI in second period: " + format(results['cpi2'], '.1f'))
    print("2002 CPI = 100.0")

    # Creates and saves the CPI graph (close the graph window to end the program)
    calculator.plot_cpi()