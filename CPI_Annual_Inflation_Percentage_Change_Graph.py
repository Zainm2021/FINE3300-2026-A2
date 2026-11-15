'''
This is my FINE3300 Assignment 2
Below is my CPI graph program that uses the Bank of Canada's monthly Consumer Price Index (CPI) data
to graph the CPI and its annual percentage change from 1914 to 2026.
'''


# Imports pandas to read the CSV file, matplotlib to create the graph and numpy for calculations
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Creates the class CPIGraph which reads the data file and graphs the CPI and its annual percentage change
class CPIGraph:
    # Reads the CPI data file and stores it as a private data frame
    def __init__(self, file_name):
        # The first 8 lines of the file are Bank of Canada notes, not data, so they are skipped
        self.__data = pd.read_csv(file_name, skiprows=8)
        
        # The data is monthly and recorded on the 1st of each month, so only rows where
        # the day (characters 9 and 10 of the date, e.g. '2002-01-01') is '01' are kept
        first_of_month = [date[8:10] == '01' for date in self.__data['date']]
        self.__data = self.__data[first_of_month]


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
        fig, ax = plt.subplots(figsize=(15, 8), layout='tight')

        # Plots the CPI on the left y-axis
        ax.plot(dates, self.__data['STATIC_INFLATIONCALC'], label='CPI', color='tab:blue')
        ax.set_xlabel('Year')
        ax.set_ylabel('CPI (2002=100)')
        ax.set_title('Canada Consumer Price Index and Annual Inflation Rate (1914-2026)', fontsize=15)

        # Dotted line through the base level, where the CPI equals 100 (the 2002 average)
        ax.axhline(y=100, linestyle=':', color='grey', label='Base Level (2002 = 100)')

        # twinx creates a second y-axis on the right that shares the same x-axis
        ax2 = ax.twinx()
        ax2.plot(dates, annual_percentage_change, label='Annual % Change (Inflation Rate)', color='orange')
        ax2.set_ylabel('Annual % Change (Inflation Rate)')

        # Combines the legends from both axes into one, so the orange line cannot cover the legend
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='lower right')

        # Saves the graph before showing it, otherwise the saved image can be blank
        fig.savefig('CPI_and_Annual_Inflation_Graph.png')

        # Displays the graph, the program pauses here until the window is closed
        plt.show()


if __name__ == "__main__":
    # Instantiates a CPIGraph object that references the Bank of Canada CPI data file
    cpi_graph = CPIGraph(file_name='STATIC_INFLATIONCALC.csv')

    # Creates, saves and displays the CPI graph
    cpi_graph.plot_cpi()