# GROUP 6
# ASGT: Group Project
# ORGN: CSUB - CMPS 3500
# FILE: ClassProjectGroup6.py
# STUDENT 1: Alberto Munoz
# STUDENT 2: Everardo Robles Tena
# STUDENT 3: Karen Santiago
# STUDENT 4: Jose Zamora
# DATE: 05/05/2024

import pandas as pd
import numpy as np
import datetime as dtime
import time
import os

# Class for flags used in main menu
class Flag:
    def __init__(self):
        self.isDFLoaded = False
        self.isDFProccessed = False

flags = Flag()

# Class that helps with customizing printed text
class Text():
    def __init__(self):
        self.reset = "\033[0m"
        self.italic = "\033[3m"
        self.blink = "\033[5m"
        self.red = "\033[31m"
        self.green= "\033[32m"
        self.yellow = "\033[33m"
        self.blue = "\033[34m"

text = Text()

# Function to load data from a file
def loadData():
    # Display all available files in current directory
    print("")
    print("Here are all available files in the current directory: \n")
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    iterator = 0
    for f in files:
        print(f"({iterator}): {f}")
        iterator += 1

    # Ask user to input file name
    user_input = input("\nWhich file would you like to choose: ")

    try:
        if user_input.isalpha() or not user_input.isdigit() or int(user_input) > iterator or int(user_input) < 0:
            raise Exception(text.red + "\nError: Invalid input - NOT one of the selectable options." + text.reset)
    except Exception as err:
        print(err)
        return

    user_file = files[int(user_input)]

    print("\nLoading input data set:")
    print("***********************")

    # Set variables to track time
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")
    print(f"[{(current_time)}] Starting Script")

    try: 
        # Read and create a data frame from user file
        print(f"[{current_time}] Loading {user_file}")
        raw_data = pd.read_csv(user_file)
        data_frame = pd.DataFrame(raw_data, columns = ['ID', 'Severity', 'Start_Time', 'End_Time', 'Distance(mi)', 
                                                       'Description', 'City', 'County', 'State', 'Zipcode', 'Country', 
                                                       'Timezone', 'Weather_Timestamp', 'Temperature(F)', 'Humidity(%)', 
                                                       'Pressure(in)', 'Visibility(mi)', 'Precipitation(in)', 'Weather_Condition'])

        test_df = data_frame.dropna()
        if test_df.empty:
            raise Exception(text.red + "\nERROR: File did not load right. Please use an appropriate file." + text.reset)

        current_time = time.strftime("%H:%M:%S")
        print(f"[{current_time}] Total Columns Read: {len(data_frame.columns)}")
        print(f"[{current_time}] Total Rows Read: {len(data_frame)}")

        end_time = time.time()
        total_time = end_time - start_time

        print(text.blue + f"\nTime to load is: {total_time: .2f} seconds" + text.reset)
        flags.isDFLoaded = True
        return data_frame

    except FileNotFoundError:
        print(text.red + f"\nERROR: File '{user_file}' not found." + text.reset)
        flags.isDFLoaded = False
        return None

    except Exception as err:
        print(err)
        flags.isDFLoaded = False
        return

# Function to process/clean data from a file
def cleanDataFrame(data_frame):
    print("\nProcessing Input Data Set:")
    print("**************************")

    # Set variables to track time
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")

    print(f"[{current_time}] Starting Script")
    print(f"[{current_time}] Performing Data Clean Up")

    # Eliminate all rows with data missing in the following columns: 
    columns_to_check = ['ID', 'Severity', 'Start_Time', 'End_Time', 'Zipcode', 'Country', 'Visibility(mi)', 'Weather_Condition']
    cleaned_once = data_frame.dropna(subset = columns_to_check)

    # Eliminate rows with data missing in 3 or more columns
    eliminate_rows = len(cleaned_once.columns) - 2
    cleaned_twice = cleaned_once.dropna(thresh = eliminate_rows)

    # Eliminate rows with distance equal to zero
    cleaned_thrice = cleaned_twice[cleaned_twice['Distance(mi)'] != 0].copy()

    # Only consider the first 5 digits of the zip code and reassign them back to column
    cleaned_thrice['Zipcode'] = cleaned_thrice['Zipcode'].str[:5]

    # Create 'datetime objects' for arithmetic operations & elim. rows equal to zero mins
    cleaned_thrice['Start_Time'] = pd.to_datetime(cleaned_thrice['Start_Time'])
    cleaned_thrice['End_Time'] = pd.to_datetime(cleaned_thrice['End_Time'])
    fully_cleaned_df = cleaned_thrice[(cleaned_thrice['End_Time'] - cleaned_thrice['Start_Time']).dt.total_seconds() / 60 > 0]

    current_time = time.strftime("%H:%M:%S")
    print(f"[{current_time}] Total Rows Read After Cleaning Is: {len(fully_cleaned_df)}")

    end_time = time.time()
    total_time = end_time - start_time

    print(text.blue + f"\nTime to clean is: {total_time: .2f} seconds" + text.reset)
    flags.isDFProccessed = True
    return fully_cleaned_df

# QUESTION 1
def threeMonthsWithHighestAccidents(data_frame):
    print("\nAnswering Questions:")
    print("********************")

    # Set variables to track time
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")

    # Get the Year and Month from Start_Time column
    data_frame['Year'] = data_frame['Start_Time'].dt.year
    data_frame['Month'] = data_frame['Start_Time'].dt.month

    # Group by Year & Month, and count total accidents
    monthly_data = data_frame.groupby(['Year', 'Month']).size().reset_index(name = 'Total_Accidents')

    # Sort accidents by descending order to leave highest accidents on top rows
    sorted_monthly = monthly_data.sort_values(by = 'Total_Accidents', ascending = False)

    # Months with most accidents are now in the top 3 rows
    highest_accidents = sorted_monthly.head(3)

    end_time = time.time()
    total_time = end_time - start_time

    print()
    print("------------------------------------------------------------------")
    print(f"[{current_time}] 1. In what month were there more accidents reported?")
    print(f"[{current_time}] The top 3 months with the most accidents are:")
    for index, row in highest_accidents.iterrows():
        print(f"[{current_time}] Month: {row['Month']}, Total Accidents: {row['Total_Accidents']}")
    print("------------------------------------------------------------------")
    print()

# QUESTION 2
def yearWithHighestAccidents(data_frame):
    # Set variables to track time
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")

    # Group by year & count total accidents
    yearly_data = data_frame.groupby('Year').size().reset_index(name ='Total_Yearly_Accidents')

    top_year = yearly_data.loc[yearly_data['Total_Yearly_Accidents'].idxmax()]

    end_time = time.time()
    total_time = end_time - start_time

    print("------------------------------------------------------------------")
    print(f"[{current_time}] 2. What is the year with the highest amount of accidents reported?")
    print(f"[{current_time}] The year with the highest amount of accidents reported is:")
    print(f"[{current_time}] Year: {top_year['Year']}, Total Accidents: {top_year['Total_Yearly_Accidents']}")
    print("------------------------------------------------------------------")
    print()

# QUESTION 3
def statesWithSeverityOfTwo(data_frame):
    # Set variables to track time
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")

    # Get the Year from Start_Time column
    data_frame['Year'] = data_frame['Start_Time'].dt.year

    # Filter to only include severity 2 
    severity_2 = data_frame[data_frame['Severity'] == 2]

    # Group by year and state, count accidents
    yearly_state_accidents = severity_2.groupby(['Year', 'State']).size().reset_index(name='Total_Accidents')

    # Find the state with the most accidents for each year
    state_severity = yearly_state_accidents.loc[yearly_state_accidents.groupby('Year')['Total_Accidents'].idxmax()]

    # Sort by descending order
    sorted_state_severity = state_severity.sort_values( by = 'Year' , ascending = True)

    # Get states with highest accidents
    top_state_severity = sorted_state_severity

    end_time = time.time()
    total_time = end_time - start_time

    print("------------------------------------------------------------------")
    print(f"[{current_time}] 3. What is the state that had the most accidents of severity 2? Display the data per year.")
    print(f"[{current_time}] The states that had the most accidents of severity 2 per year is:\n")
    print(top_state_severity.to_string(index = False))
    print("------------------------------------------------------------------")
    print()

# QUESTION 4
def commonSeverityLevel(data_frame):
    # Set variables to track time
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")

    # Filter the data frame to include only accidents from VA, CA, and FL
    check_states = data_frame[data_frame['State'].isin(['VA', 'CA', 'FL'])]

    # Group the filtered data frame by severity and count the occurrences of each severity level
    severity_level = check_states['Severity'].value_counts()

    # Find the severity level with the highest count
    most_common_severity = severity_level.idxmax()

    end_time = time.time()
    total_time = end_time - start_time

    print("------------------------------------------------------------------")
    print(f"[{current_time}] 4. What severity is the most common in Virginia, California and Florida?")
    print(f"[{current_time}] The most common severity in VA, CA, and FL is:")
    print(f"[{current_time}] {most_common_severity}")
    print("------------------------------------------------------------------")
    print()

# QUESTION 5 
def californiaCityAccidents(data_frame):
    # Set variables to track time
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")

    #Filer the data frame to include only accidents in CA
    ca_accidents = data_frame[data_frame['State'].isin(['CA'])].copy()

    # Extract the year from 'Start_Time' dt object
    ca_accidents['Year'] = ca_accidents['Start_Time'].dt.year

    # Group by city and year, then count the number of accidents
    city_year_accidents = ca_accidents.groupby(['City', 'Year']).size().reset_index(name = 'Accident Count')
    city_year_accidents_sorted = city_year_accidents.sort_values(by = ['Year', 'Accident Count'], ascending = [True, False])

    end_time = time.time()
    total_time = end_time - start_time

    print("------------------------------------------------------------------")
    print(f"[{current_time}] 5. What are the 5 cities that had the most accidents in California? Display the data per year.")
    print(f"[{current_time}] The cities with the most accidents in CA per year are:\n")
    for year in city_year_accidents_sorted['Year'].unique():
        top_cities_year = city_year_accidents_sorted[city_year_accidents_sorted['Year'] == year].head(5)
        print(top_cities_year.to_string(index = False))
        if year != city_year_accidents_sorted['Year'].unique()[-1]:
            print()
    print("------------------------------------------------------------------")
    print()

# QUESTION 6
def avgHumidityAndTemperature(data_frame):
    # Set variables to track time
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")

    # Filter the data frame to include only accidents in the city of Boston and with severity 4
    boston_severity = data_frame[(data_frame['City'] == 'Boston') & (data_frame['Severity'] == 4)].copy()

    # Extract the month from the 'Start_Time' column
    boston_severity['Month'] = boston_severity['Start_Time'].dt.month

    # Group by month and calculate average humidity and temperature
    avg_humidity_temp = boston_severity.groupby('Month').agg({'Humidity(%)': 'mean', 'Temperature(F)': 'mean'}).reset_index()

    end_time = time.time()
    total_time = end_time - start_time

    print("------------------------------------------------------------------")
    print(f"[{current_time}] 6. What was the average humidity and average temperature of all accidents of severity 4 that occurred in the city of Boston? Display the data per month.")
    print(f"[{current_time}] The average humidity and temperature of severity 4 accidents in Boston per month are:\n")
    print(avg_humidity_temp.to_string(index=False))
    print("------------------------------------------------------------------")
    print()

# QUESTION 7
def nycWeatherConditionAccidents(data_frame):
    # Store and filter the inputted data frame
    # to only have accident reports from New York City
    raw_nyc_data = data_frame[data_frame['City'].isin(['New York'])]

    # create a version of raw data that can be changed however => will clean up later
    dirty_nyc_data = raw_nyc_data.copy()
    dirty_nyc_data['Month'] = \
            dirty_nyc_data['Start_Time'].apply(lambda x: "%d" % (x.month)).astype(int)

    # Cleaning up the data for outputting:
    # Copy out the month and weather_condition columns from dirty dataframe
    clean_nyc_data = dirty_nyc_data[['Month', 'Weather_Condition']].copy()

    # BEFORE CONTINUING, GET ANY EXTRA DATA FROM CLEANED UP DATAFRAME 
    # BEFORE IT IS TOO ALTERED:
    # Count the number of accidents per weather_condition and set up column "Accidents"
    top_weather_conditons = \
            clean_nyc_data.groupby(['Weather_Condition']).size().reset_index(name = 'Accidents')
    
    # Sort this dataframe by the number of accidents per weather condition and filter out the top 3
    top_weather_conditons = \
            top_weather_conditons.sort_values(by = 'Accidents', ascending = False).head(3)

    # Continue the cleaning up process:
    # Count the number of accidents per weather condition
    clean_nyc_data = \
            clean_nyc_data.groupby(['Month', 'Weather_Condition']).size().reset_index(name = 'Accidents')
    
    # Sort this dataframe by the 'Month' column => 'Accidents' is sorted from greatest to least
    clean_nyc_data = \
            clean_nyc_data.sort_values(by = ['Month', 'Accidents'], ascending = [True, False])

    now = dtime.datetime.now()
    now = now.strftime("%H:%M:%S")

    print("------------------------------------------------------------------")
    print(f"[{now}] 7. What are the 3 most common weather conditions (weather_conditions) when accidents occurred in New York city? Display the data per month.")
    print(f"[{now}] The 3 most common weather conditions when accidents occurred in New York city per month:\n")
    for month in clean_nyc_data['Month'].unique():
        weather_per_month = clean_nyc_data[clean_nyc_data['Month'] == month].head(3)
        print(weather_per_month.to_string(index = False)) 
        print()
    print(f"[{now}] Top Three Weather Condition seen across all months:\n")
    print(top_weather_conditons.to_string(index = False))
    print("------------------------------------------------------------------")
    print()

# QUESTION 8
def nhMaxVisibility(data_frame):
    # Store and filter the inputted data frame
    # to only have accident reports from New Hampshire
    nh_data = data_frame[data_frame['State'].isin(['NH'])]
    
    # Filter the data to only have instances where Severity was 2
    nh_data_by_sev_two = nh_data.loc[nh_data['Severity'] == 2]
    
    # Get the max Visibility from the previosuly-filtered out data
    nh_data_final = nh_data_by_sev_two['Visibility(mi)'].max()

    now = dtime.datetime.now()
    now = now.strftime("%H:%M:%S")

    print("------------------------------------------------------------------")
    print(f"[{now}] 8. What was the maximum visibility of all accidents of severity 2 that occurred in the state of New Hampshire?")
    print(f"[{now}] The maximum visibility of all accidents of severity 2 that occurred in the state of New Hampshire is:")
    print(f"[{now}] {nh_data_final} miles")
    print("------------------------------------------------------------------")
    print()

# QUESTION 9
def bakersfieldSeverityAccidents(data_frame):
    # Store and filter the inputted data frame
    # to only have accident reports from Bakersfield
    raw_bak_data = data_frame[data_frame['City'].isin(['Bakersfield'])]

    # create a version of raw data that can be changed however => will clean up later
    dirty_bak_data = raw_bak_data.copy()
    
    # add a Year column to the dataframe
    dirty_bak_data['Year'] = \
            dirty_bak_data['Start_Time'].apply(lambda x: "%d" % (x.year)).astype(int)

    # Cleaning up the data for outputting:
    # Copy out the year and severity columns from dirty dataframe
    clean_bak_data = dirty_bak_data[['Year', 'Severity']].copy()

    # BEFORE CONTINUING, GET ANY EXTRA DATA FROM CLEANED UP DATAFRAME 
    # BEFORE IT IS TOO ALTERED:
    # Count the number of accidents per severity and set up column "Accidents"
    total_per_severity = \
            clean_bak_data.groupby(['Severity']).size().reset_index(name = 'Accidents')
    
    # Sort this dataframe by the number of accidents per severity level
    total_per_severity = \
            total_per_severity.sort_values(by = 'Severity', ascending = True)

    # Continue the cleaning up process:
    # Count the number of accidents per severity
    clean_bak_data = \
            clean_bak_data.groupby(['Year', 'Severity']).size().reset_index(name = 'Accidents')
    
    # Sort this dataframe by the 'Year' column => 'Severity' is sorted from least to greatest
    clean_bak_data = \
            clean_bak_data.sort_values(by = ['Year', 'Severity'], ascending = [True, True])

    # print(clean_bak_data.to_string(index = False))
    # print(total_per_severity.to_string(index = False))

    now = dtime.datetime.now()
    now = now.strftime("%H:%M:%S")

    print("------------------------------------------------------------------")
    print(f"[{now}] 9. How many accidents of each severity were recorded in Bakersfield? Display the data per year.")
    print(f"[{now}] The number of accidents of each severity recorded in Bakersfield per year:\n")
    for year in clean_bak_data['Year'].unique():
        severity_per_year = clean_bak_data[clean_bak_data['Year'] == year]
        print(severity_per_year.to_string(index = False)) 
        print()
    print(f"[{now}] Total Number of Accidents in Bakersfield per each severity across all recorded years:\n")
    print(total_per_severity.to_string(index = False))
    print("------------------------------------------------------------------")

# QUESTION 10
def vegasLongestAccidents(data_frame):
    print("\n------------------------------------------------------------------")
    print("10. What was the longest accident (in hours) recorded in Las Vegas in" +
          " the Spring (March, April, and May)?")
    print("Displaying the longest accidents of each month in Spring per year:")
    data_frame['Start_Time'] = pd.to_datetime(data_frame['Start_Time'],
                                      format='%-m/%-d/%Y %-H:%-M %p')
    data_frame['End_Time'] = pd.to_datetime(data_frame['End_Time'],
                                      format='%-m/%-d/%Y %-H:%-M %p')

    min_year = data_frame['Start_Time'].dt.year.min()
    max_year = data_frame['Start_Time'].dt.year.max()

    for year in range(min_year, (max_year + 1)):
        print("\n\nThe longest accident recorded in Las Vegas in Spring of",
              year, "was :")
        march = data_frame[(data_frame['Start_Time'].dt.month == 3) &
                   (data_frame['Start_Time'].dt.year == year)].copy()
        april = data_frame[(data_frame['Start_Time'].dt.month == 4) &
                   (data_frame['Start_Time'].dt.year == year)].copy()
        may = data_frame[(data_frame['Start_Time'].dt.month == 5) &
                   (data_frame['Start_Time'].dt.year == year)].copy()
        if not march.empty:
            march['Time_in_Hours'] = (march['End_Time'] -
                                      march['Start_Time']).dt.total_seconds() / 3600
            max_time_march = march.loc[march['Time_in_Hours'].idxmax()]
            max_time_id1 = max_time_march['ID']
            print("March: ", max_time_march['Time_in_Hours'], "hours")
        else:
            print("March: No accidents in", year)
        if not april.empty:
            april['Time_in_Hours'] = (april['End_Time'] -
                                      april['Start_Time']).dt.total_seconds() / 3600
            max_time_april = april.loc[april['Time_in_Hours'].idxmax()]
            max_time_id2 = max_time_april['ID']
            print("April: ", max_time_april['Time_in_Hours'], "hours")
        else:
            print("April: No accidents in", year)
        if not may.empty:
            may['Time_in_Hours'] = (may['End_Time'] -
                                    may['Start_Time']).dt.total_seconds() / 3600
            max_time_may = may.loc[may['Time_in_Hours'].idxmax()]
            max_time_id3 = max_time_may['ID']
            print("May: ", max_time_may['Time_in_Hours'], "hours")
        else:
            print("May: No accidents in", year)

        #empty the dataframes of each month
        march = pd.DataFrame()
        april = pd.DataFrame()
        may = pd.DataFrame()

    print("------------------------------------------------------------------")

def checkState(state):
    try:
        if not state.isalpha() or len(state) != 2:
            raise ValueError(text.red + "\nERROR: Invalid state input. Must be state's abbreviation.\n" + text.reset)
    except ValueError as err:
        #print error message
        print(err)
        return False

    return True

def checkCity(city):
    try:
        if not all(char.isalpha() or char.isspace() for char in city):
            raise ValueError(text.red + "\nERROR: Invalid city input. Only letters can be entered for" + 
                             " the city.\n" + text.reset)
    except ValueError as err:
        #print error message
        print(err)
        return False

    return True

def checkZipcode(zipcode):
    try:
        # test_zip = int(zipcode)
        if not zipcode.isdigit() or (len(zipcode) != 5):
            raise ValueError(text.red + "\nERROR: Invalid Zipcode. Must be a 5-digit Zipcode.\n" + text.reset)
    except ValueError as err:
        #print error message
        print(err)
        return False

    return True

# SEARCH FUNCTION 1
def searchStateCityZip(df):

    # Get input from user for the state, city, and zipcode
    print("")
    print("Search Accidents:")
    print("******************")
    print("Enter state's abbreviation. For example, CA for California.")
    state = input("Press 'Enter' if no state: ")
    city = input("Enter city. Press 'Enter' if no city: ")
    zipcode = input("Enter 5-digit zipcode. Press 'Enter' if no zipcode: ")

    # Start the timer 
    start_time = time.time()

    # Searches dataframe based on input collected for state, city, and zipcode
    # If no input is inserted for an input, it will be ignorned.
    # If no input is inserted for all 3, exit the function
    if state and city and zipcode:
        check1 = checkState(state)
        check2 = checkCity(city)
        check3 = checkZipcode(zipcode)
        if check1 and check2 and check3:
            search = df[(df['State'] == state) & (df['City'] == city)
                        & (df['Zipcode'] == zipcode)]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif state and city:
        check1 = checkState(state)
        check2 = checkCity(city)
        if check1 and check2:
            search = df[(df['State'] == state) & (df['City'] == city)]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif state and zipcode:
        check1 = checkState(state)
        check2 = checkZipcode(zipcode)
        if check1 and check2:
            search = df[(df['State'] == state) & (df['Zipcode'] == zipcode)]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif city and zipcode:
        check1 = checkCity(city)
        check2 = checkZipcode(zipcode)
        if check1 and check2:
            search = df[(df['City'] == city) & (df['Zipcode'] == zipcode)]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif state:
        check1 = checkState(state)
        if check1:
            search = df[(df['State'] == state)]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif city:
        check1 = checkCity(city)
        if check1:
            search = df[(df['City'] == city)]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif zipcode:
        check1 = checkZipcode(zipcode)
        if check1:
            search = df[(df['Zipcode'] == zipcode)]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    else:
        print("\nYou have entered nothing for state, city, and zipcode.")
        print("Exiting search...\n")
        return

    # print dataframe after search is done.
    if search.empty:
        end_time = time.time()
        total_time = end_time - start_time
        print("")
        print("No results found\n")
        print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
    else:
        #Check total time
        end_time = time.time()
        total_time = end_time - start_time
        total_accidents = len(search)
        print("")
        print(f"There were {total_accidents} accidents\n")
        print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)

def checkYear(year):
    try:
        if not year.isdigit() or (len(year) != 4):
            raise ValueError(text.red + "\nERROR: Invalid input for year. Year must be 4 digits.\n" + text.reset)
    except ValueError as err:
        print(err)
        return False

    return True

def checkMonth(month):
    try:
        if not month.isdigit():
            raise ValueError(text.red + "\nERROR: Invalid input for month. Value must be between 1-12.\n" + text.reset)
        if (int(month) < 1) or (int(month) > 12):
            raise ValueError(text.red + "\nERROR: Invalid input for month. Value must be between 1-12.\n" + text.reset)
    except ValueError as err:
        print(err)
        return False

    return True

def checkDay(day):
    try:
        if not day.isdigit():
            raise ValueError(text.red + "\nERROR: Invalid input for day. Value must be between 1-31.\n" + text.reset)
        if (int(day) < 1) or (int(day) > 31):
            raise ValueError(text.red + "\nERROR: Invalid input for day. Value must be between 1-31.\n" + text.reset)
    except ValueError as err:
        print(err)
        return False

    return True

# SEARCH FUNCTION 2
def searchYearMonthDay(df):

    # Get input from user for the year, month, and day
    print("")
    print("Search Accidents:")
    print("******************")
    year = input("Enter 4-digit year. Press 'Enter' if no year: ")
    print("Enter month. For example, '3' for March.")
    month = input("Press 'Enter' if no month: ")
    day = input("Enter day. Press 'Enter' if no day: ")

    df['Start_Time'] = pd.to_datetime(df['Start_Time'],
                                      format='%-m/%-d/%Y %-H:%-M %p')

    # Start the timer 
    start_time = time.time()

    # Searches dataframe based on input collected for month, day, and year
    # If no input is inserted for an input, it will be ignorned.
    # If no input is inserted for all 3, exit the function
    if month and day and year:
        check1 = checkDay(day)
        check2 = checkMonth(month)
        check3 = checkYear(year)
        if check1 and check2 and check3:
            match = df[(df['Start_Time'].dt.month == int(month)) &
                       (df['Start_Time'].dt.day == int(day)) &
                       (df['Start_Time'].dt.year == int(year))]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif month and day:
        check1 = checkDay(day)
        check2 = checkMonth(month)
        if check1 and check2:
            match = df[(df['Start_Time'].dt.month == int(month)) &
                       (df['Start_Time'].dt.day == int(day))]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif month and year:
        check1 = checkMonth(month)
        check2 = checkYear(year)
        if check1:
            match = df[(df['Start_Time'].dt.month == int(month)) &
                       (df['Start_Time'].dt.year == int(year))]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif day and year:
        check1 = checkDay(day)
        check2 = checkYear(year)
        if check1 and check2:
            match = df[(df['Start_Time'].dt.day == int(day)) &
                       (df['Start_Time'].dt.year == int(year))]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif month:
        check1 = checkMonth(month)
        if check1:
            match = df[(df['Start_Time'].dt.month == int(month))]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif day:
        check1 = checkDay(day)
        if check1:
            match = df[(df['Start_Time'].dt.day == int(day))]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    elif year:
        check1 = checkYear(year)
        if check1:
            match = df[(df['Start_Time'].dt.year == int(year))]
        else:
            print("Exiting search...\n")
            end_time = time.time()
            total_time = end_time - start_time
            print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
            return
    else:
        print("\nNo month, day, or year entered. Exiting search...\n")
        end_time = time.time()
        total_time = end_time - start_time
        print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
        return

    # print dataframe after search is done.
    if match.empty:
        end_time = time.time()
        total_time = end_time - start_time
        print("")
        print("No results found\n")
        print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
    else:
        end_time = time.time()
        total_time = end_time - start_time
        total_accidents = len(match)
        print("")
        print(f"There were {total_accidents} accidents\n")
        print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)
        
# SEARCH FUNCTION 3
def accidentsUsingTempAndVisibility(df):
    print("")
    print("Search Accidents:")
    print("******************")

    # Set Up Variables to track time
    current_time = time.strftime("%H:%M:%S")

    # Get input and check if it is valid
    min_temp_input = input("Enter a Minimum Temperature (F): ")

    try:
        if min_temp_input.isalpha():
            raise TypeError(text.red + "\nERROR: Input is NOT an integer nor a float value." + text.reset)
    except TypeError as err:
        print(err)
        return

    max_temp_input = input("Enter a Maximum Temperature (F): ")

    try:
        if max_temp_input.isalpha():
            raise TypeError(text.red + "\nERROR: Input is NOT an integer nor a float value." + text.reset)
    except TypeError as err:
        print(err)
        return

    min_range_input = input("Enter a Minimum Visibility (mi): ")

    try:
        if min_range_input.isalpha():
            raise TypeError(text.red + "\nERROR: Input is NOT an integer nor a float value." + text.reset)
    except TypeError as err:
        print(err)
        return

    max_range_input = input("Enter a Maximum Visibility (mi): ")

    try:
        if max_range_input.isalpha():
            raise TypeError(text.red + "\nERROR: Input is NOT an integer nor a float value." + text.reset)
    except TypeError as err:
        print(err)
        return

    print("")

    # Start timer
    start_time = time.time()

    # Convert to float or set to None if empty
    min_temp = float(min_temp_input) if min_temp_input else None
    max_temp = float(max_temp_input) if max_temp_input else None

    # Check if temperature are in correct order
    try:
        if max_temp != None and max_temp < min_temp:
            raise Exception(text.red + "ERROR: Maximum temperature is smaller than minimum temperature" + text.reset)
    except Exception as err:
        print(err)
        return

    min_range = float(min_range_input) if min_range_input else None
    max_range = float(max_range_input) if max_range_input else None

    # Check if visibility are in correct order
    try:
        if max_range != None and max_range < min_range:
            raise Exception(text.red + "ERROR: Maximum visibility is smaller than minimum visibility" + text.reset)
    except Exception as err:
        print(err)
        return

    filtered_df = df

    if min_temp is not None:
        filtered_df = filtered_df[filtered_df['Temperature(F)'] >= min_temp]
    if max_temp is not None:
        filtered_df = filtered_df[filtered_df['Temperature(F)'] <= max_temp]
    if min_range is not None:
        filtered_df = filtered_df[filtered_df['Visibility(mi)'] >= min_range]
    if max_range is not None:
        filtered_df = filtered_df[filtered_df['Visibility(mi)'] <= max_range]

    #Count total accidents
    total_accidents = len(filtered_df)

    #Check total time
    end_time = time.time()
    total_time = end_time - start_time

    print(f"There were {total_accidents} accidents using the specified range")
    print("")
    print(text.blue + f"Time to perform search is: {total_time: .5f} seconds" + text.reset)

def main():
    data_frame = None
    fully_cleaned_df = None

    start_time = time.time()
    while True:
        print("\nMenu:")
        print("(1) Load Data")
        print("(2) Process Data")
        print("(3) Print Answers")
        print("(4) Search Accidents (City, State, and Zip Code)")
        print("(5) Search Accidents (Year, Month, and Day)")
        print("(6) Search Accidents (Temperatute Range and Visibility Range)")
        print("(7) Quit")

        choice = input("\nPlease enter your choice: ")

        if choice == '1':
            if not flags.isDFLoaded:
                data_frame = loadData()
            else:
                print(text.yellow + "\nWARNING: Data has already been loaded." + text.reset)
        elif choice == '2':
            if not flags.isDFProccessed and flags.isDFLoaded:
                fully_cleaned_df = cleanDataFrame(data_frame)
            elif not flags.isDFLoaded:
                print(text.yellow + "\nWARNING: Data needs to be loaded." + text.reset)
            else:
                print(text.yellow + "\nWARNING: Data has already been processed." + text.reset)
        elif choice == '3':
            if flags.isDFLoaded and flags.isDFProccessed:
                threeMonthsWithHighestAccidents(fully_cleaned_df) # Question 1
                yearWithHighestAccidents(fully_cleaned_df)        # Question 2
                statesWithSeverityOfTwo(fully_cleaned_df)         # Question 3
                commonSeverityLevel(fully_cleaned_df)             # Question 4
                californiaCityAccidents(fully_cleaned_df)         # Question 5
                avgHumidityAndTemperature(fully_cleaned_df)       # Question 6
                nycWeatherConditionAccidents(fully_cleaned_df)    # Question 7
                nhMaxVisibility(fully_cleaned_df)                 # Question 8
                bakersfieldSeverityAccidents(fully_cleaned_df)    # Question 9
                vegasLongestAccidents(fully_cleaned_df)           # Question 10
            elif flags.isDFLoaded and not flags.isDFProccessed:
                print(text.yellow + "\nWARNING: Data has been loaded, but not processed." + text.reset)
            elif not flags.isDFLoaded and not flags.isDFProccessed:
                print(text.yellow + "\nWARNING: Data needs to be loaded and processed." + text.reset)
        elif choice == '4':
            if not flags.isDFLoaded and not flags.isDFProccessed:
                print(text.yellow + "\nWARNING: Data needs to be loaded and processed." + text.reset)
            elif flags.isDFLoaded and not flags.isDFProccessed:
                print(text.yellow + "\nWARNING: Data has been loaded, but not processed." + text.reset)
            else:
                searchStateCityZip(fully_cleaned_df)
        elif choice == '5':
            if not flags.isDFLoaded and not flags.isDFProccessed:
                print(text.yellow + "\nWARNING: Data needs to be loaded and processed." + text.reset)
            elif flags.isDFLoaded and not flags.isDFProccessed:
                print(text.yellow + "\nWARNING: Data has been loaded, but not processed." + text.reset)
            else:
                searchYearMonthDay(fully_cleaned_df)
        elif choice == '6':
            if not flags.isDFLoaded and not flags.isDFProccessed:
                print(text.yellow + "\nWARNING: Data needs to be loaded and processed." + text.reset)
            elif flags.isDFLoaded and not flags.isDFProccessed:
                print(text.yellow + "\nWARNING: Data has been loaded, but not processed." + text.reset)
            else:
                accidentsUsingTempAndVisibility(fully_cleaned_df)
        elif choice == '7':
            print(text.green + text.blink + text.italic + "\nGoodbye" + text.reset)
            break
        else:
            print(text.red + "\nERROR: Invalid choice. Please enter a valid option." + text.reset)
            #Implement feauture to print Total Run Time
    end_time = time.time()
    total_time = end_time - start_time
    total_time = dtime.timedelta(seconds=round(total_time, 6))
    print(text.blue + f"\nTotal Running Time: {total_time}" + text.reset)

main()
