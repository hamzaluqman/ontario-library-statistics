# ENSF 592 Spring 2021 Term Project
# Authors: Hamza Luqman & Uzair Anjum - Group 18
# To run this program, download/clone the repository and keep this .py file just outside the Ontario Public Library folder.

# Importing libraries to be used in the program
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
idx = pd.IndexSlice #index slice object

# Function gets the user to input a valid library name and checks if the library name is in the index of the
# dataframe or not and prompts accordingly using try catch
# Input Parameter: df dataframe object to check library names
# Returns a valid library name
def get_library_name(df):
    """
    A function that is used to to prompt the user to input a valid library name from the dataset. A valid library name is one that
    is present in the final dataset after the merge operations and filtering of data has been done. If an invalid
    library name is entered by the user the program will not terminate and will continue to prompt user for valid input.

        Attributes:
            df (Pandas DataFrame): DataFrame that will be used to check if user input library name is present in it.

        Returns:
            returns the valid library name
    """
    check = 1
    while check: #check is true initally and will not be false until valid input
        try:
            library_name = input("Please enter library name (in Ontario, example: Ajax) for which you would like to see stats for : ")
            if library_name in df.index.get_level_values(0): # get_level_values gets the values of the Library Name index
                check = 0 # if input is in the index values, makes check 0 and exits out the while loop
            else:
                raise ValueError # raises the ValueError as per requirements
        except ValueError:
            print('You must enter a valid library name! example, Ajax')
    return library_name

# Function gets the user to input a year that the user wants the stats for 
# Input Parameter: df dataframe object to check valid years
# Returns a valid year for which the data exists
def get_year_input(df, library_name):
    """
    A function that is used to to prompt the user to input a valid year from the dataset. If there is no data for the user requested year
    in the DataFrame for the user requested library name, the input is considered invalid.

        Attributes: 
            df (Pandas DataFrame): DataFrame that will be used to check if user input year is present in it.
            library_name (str) : String representing a valid library name input by the user

        Returns:
            return a valid year for which data exists
    """

    check = 1
    while check: #check is true initally and will not be false until valid input
        try:
            library_year = int(input("For which year would you like to see the stats for? (2017, 2018, 2019): "))
            if library_year in df.loc[idx[library_name,:,:], idx[:]].index.get_level_values(2): #get_level_values gets the values of the index Sub Region ????
                check = 0 # if input is in the index values, makes check 0 and exits out the while loop
            else:
                raise ValueError # raises the ValueError as per requirements

        except ValueError:
            print('You have entered an invalid year, or there is no data available for that year\n \
                Please enter another year from 2017, 2018, 2019!')
    return library_year

# Main function
def main():

    # Importing three excel sheets consisting of Data for years 2017, 2018 and 2018 into a pandas dataframe
    data_2017 = pd.read_excel(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2017.xlsx")
    data_2018 = pd.read_excel(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2018.xlsx")
    data_2019 = pd.read_excel(r".\Ontario Public Library Datasets\ontario_public_library_statistics_2019.xlsx")

    all_data = data_2017.merge(data_2018, how = 'outer') # Merging data_2017 and data_2018 and assigning to all_data

    all_data = all_data.merge(data_2019, how = 'outer') # Merging data_2018 and data_2019 and re-assigning to all_data

    all_data = all_data.set_index(["Library Full Name", "Library Number", "Year"]) # Setting index to "Library Full Name", "Library Number", "Year"

    master_df = all_data.sort_index() # Sorting the dataframe by index

    # Filtering out the library with 0 carholders and 0 data
    filtered_df = master_df[master_df['No. Cardholders'] > 0].copy()
    # Filling all remainder missing data with "Data not available"
    filtered_df = filtered_df.fillna("Data not available")

    # Adding two new columns to the dataset
    # Total Titles represents the sum of all E-books and E-auido Titles and the Total Print Titles Held
    # Total Titles per Cardholder is all E-books and E-auido Titles and the Total Print Titles Held
    # divided by the No. Cardholders. This tells us the average number of books every card holder has for the library
    filtered_df['Total Titles'] = (filtered_df['Total E-book and E-audio Titles'] + filtered_df['Total Print Titles Held'])
    filtered_df['Total Titles per Cardholder'] = (filtered_df['Total E-book and E-audio Titles'] + filtered_df['Total Print Titles Held'])/filtered_df['No. Cardholders']

    # Prompting the user to input a valid library name by calling the get_library_name function
    library_name = get_library_name(filtered_df)
    # Prompting the user to input a valid year by calling the get_year_input function
    library_year = get_year_input(filtered_df, library_name)


    # Printing the stats for the library and year chosen
    print("\n\nYear {} stats for the {} library branch are: \n".format(library_year, library_name))
    print(filtered_df.loc[idx[library_name,:,library_year], idx[:]].T)

    # Printing the Total Print Titles Held, Total E-book and E-audio Titles, Total Titles and Total Titles per Cardholder
    # for the chosen library across the years for which data is available.
    library_data = filtered_df.loc[idx[library_name,:,:], idx[:]]
    print("\nTotal Print Titles, E-book and E-audio Titles, Total Titles and Total Titles per Cardholder data for {} library:" .format(library_name))
    print("\n", library_data.pivot_table(['Total Print Titles Held', 'Total E-book and E-audio Titles', 
    'Total Titles', 'Total Titles per Cardholder'], index = ["Year", "No. Cardholders"])) # index are Year and No. Cardholders


    # Print stats for the library chosen accross multiple years. Also checks if there are multiple years or not
    # if there are no multiple years data available for the chosen library, "Not enough yearly data to display general change stats" 
    # message will be printed
    print("\nYearly change in No. Cardholders and Total Titles for the {} library branch: \n".format(library_name))
    no_of_years_available = filtered_df.loc[idx[library_name,:,:], idx[:]].index.get_level_values(2)
    if len(no_of_years_available) == 1: # If only one year data is available, cannot calculate annual change information
        print('Not enough yearly data to display general change stats')
    else:
        for i in no_of_years_available:
            if i == no_of_years_available[-1]: # Loop breaks when i equals to last value of the year for which data is available for the library
                break
            else:
                print( "Change in No. Cardholders from {} to {}: {}\n" \
                        "Change in Total Titles from {} to {}: {}\n".format(i,i+1,
                filtered_df.loc[idx[library_name,:,i+1], idx['No. Cardholders']][0] - filtered_df.loc[idx[library_name,:,i], idx['No. Cardholders']][0],
                i,i+1,
                filtered_df.loc[idx[library_name,:,i+1], idx['Total Titles']][0] - filtered_df.loc[idx[library_name,:,i], idx['Total Titles']][0]))

    # Printing aggregate stats for the entire dataset
    print('General Library infromation')
    print('\nAggregate stats for the entire dataset: \n')
    print(filtered_df.describe().T)  

    # Printing the sum of all columns data for years 2017, 2018 and 2019, across all libraries
    print(" \nThe sum of all column data for years 2017, 2018 and 2019 across all libraries: \n ")
    print(filtered_df.groupby('Year').sum())

    # Printing the maximum and minimum number of card holders for all libraries accross all years
    print("\nThe maximum and minimum number of card holders for all libraries across all years: \n ")
    print(filtered_df.groupby('Library Full Name')[['No. Cardholders']].aggregate([max, min]))

    # Export the master df to an excel file print filtered_df
    filtered_df.to_excel("filtered_dataframe_export.xlsx")

    # End of terminal display data
    # The codes below are used to generate line graph and bar graph

    # Getting data from plotting
    sum_print_titles = (filtered_df.loc[idx[:,:,:], idx['Total Print Titles Held']].sum(level = 2))
    sum_e_titles = (filtered_df.loc[idx[:,:,:], idx['Total E-book and E-audio Titles']].sum(level = 2))
    cardholders = (filtered_df.loc[idx[:,:,:], idx['No. Cardholders']].sum(level = 2))
    
    # Create subplot
    fig, data1 = plt.subplots() # data 1 is the first axis
    # Since we will be plotting the cardholders on the secondary y axis, we can twin the xaxix since it also
    # has the same years
    data2 = data1.twinx() # data 2 is the secondary y axis
    # Plotting the three data sets, total print titles, e-titles, and carholders
    data1.plot(sum_print_titles, '-', color = 'red', label = 'Total Print Titles Held', linewidth=2) # first axis
    data1.plot(sum_e_titles, '-', color = 'black', label = 'Total E-book and E-audio Titles', linewidth=2) # first axis
    data2.plot(cardholders, '-', color = 'green', label = 'No. Cardholders', linewidth=2) # secondary axis

    # Setting labels
    data1.set_xlabel('Year')
    data1.set_ylabel('No. of Titles')
    data2.set_ylabel('Cardholders')

    # Setting the index tick points 
    plt.xticks(sum_print_titles.index)
    # Adding both axis legends
    data1.legend(loc = 'upper left') # Setting location for legend in graph
    data2.legend(loc = 'upper right') # Setting location for legend in graph
    fig.savefig('Data_line_graph.png') # Saving the line graph figure
    
    # Getting the sum of No. Cardholders,Total Print Titles Held, Total E-book and E-audio Titles Bar Graph
    # across all years to use in the bar graph
    # Storing the sum data in bar_data
    bar_data = filtered_df.groupby('Year')[['No. Cardholders','Total Print Titles Held', 'Total E-book and E-audio Titles']].sum()

    bar_data.T.plot(kind='bar', figsize=(9,9)) # plotting the bar graph with specifies size
    plt.ylabel("Number") # Labeling the bar graph
    plt.title('Bar Graph') # labeling the title of the bar graph
    plt.xticks(rotation=20) # Setting the angle of the x-asis labels
    plt.savefig('Data_bar_graph.png') # Saving the bar graph figure

    # Showing the plots
    plt.show()
    

if __name__ == '__main__':
    main()