# Ontario Library Statistics

The Ontario Public Library Dataset was utilized for this project. This dataset consists of Libraries in Ontario and their region, service type, address and book inventory information. The dataset spans over the years 2017 – 2019 inclusive. However, not all libraries have data available for all three of these years, hence only the years within 2017 – 2019 of which data is available is used.

The annual data was present in three separate excel sheets. Data from each of these sheets were merged within the program. The merged dataset was filtered to delete libraries with no book inventory information and any other missing data was replaced with “Data not available”. The dataset is indexed according to “Library Full Name”, “Library Number” and ‘Year”.In the program, the user is prompted for two inputs. The first user input is for a valid Library Name from the merged and filtered data set. The second user input is for a year between 2017 – 2019 inclusive.

The output of the program consists of user requested library and year specific information as well as general dataset wide information. For the user requested library name and year, all the available column information from the dataset, a pivot table consisting of annual information for Total Print Titles, E-book and E-audio Titles, Total Titles and Total Titles per Cardholder followed by a calculation of the change in the number of cardholders for each available year from 2017 – 2019 inclusive is displayed. For the dataset wide information aggregate stats are printed out followed by sum of all column data for years 2017, 2018 and 2019 across all libraries. The maximum and minimum number of card holders for all libraries across all years is then printed out. Finally, the annual change in “No. Cardholders”, “Total Print Titles” and “Total E-Titles” is displayed in a line graph and bar graph form.

## Contributors
- Hamza Luqman
- Uzair Anjum
