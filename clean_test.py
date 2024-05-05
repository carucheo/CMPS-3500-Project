import pandas as pd
import numpy as np


# set full dataframe for display
'''
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
'''

# Read and assign csv data into 'raw_data' variable
raw_data = pd.read_csv('US_Accidents_data.csv')

# Create a data frame from our csv datafile
data_frame = pd.DataFrame(raw_data, columns = ['ID', 'Severity', 'Start_Time', 'End_Time', 'Distance(mi)', 
                                               'Description', 'City', 'County', 'State', 'Zipcode', 'Country', 
                                               'Timezone', 'Weather_Timestamp', 'Temperature(F)', 'Humidity(%)', 
                                               'Pressure(in)', 'Visibility(mi)', 'Precipitation(in)', 'Weather_Condition'])

def cleanDataFrame():
    # Eliminate all rows with data missing in the followign columns: 
    # ID | Severity | Zipcode | Start_Time | End_Time | Visibility(mi) | Weather_Condition | Country
    columns_to_check = ['ID', 'Severity', 'Start_Time', 'End_Time', 'Zipcode', 'Country', 'Visibility(mi)', 'Weather_Condition']
    cleaned_once = data_frame.dropna(subset = columns_to_check)

    # Eliminate rows with data missing in 3 or more columns
    eliminate_rows = len(cleaned_once.columns) - 2
    cleaned_twice = cleaned_once.dropna(thresh = eliminate_rows)

    # Eliminate rows with distance equal to zero
    cleaned_thrice = cleaned_twice[cleaned_twice['Distance(mi)'] != 0]

    # Create a copy of cleaned_thrice dataframe to resolve a runtime error
    cleaned_four = cleaned_thrice.copy()
    # Only consider the first 5 digits of the zip code and reassign them back to column
    cleaned_four['Zipcode'] = cleaned_four['Zipcode'].str[:5]

    # Create 'datetime objects' for arithmetic operations & elim. rows equal to 0 mins
    cleaned_four['Start_Time'] = pd.to_datetime(cleaned_four['Start_Time'])
    cleaned_four['End_Time'] = pd.to_datetime(cleaned_four['End_Time'])
    fully_cleaned_df = cleaned_four[(cleaned_four['End_Time'] - cleaned_four['Start_Time']).dt.total_seconds() / 60 > 0]

    return fully_cleaned_df

def question10(df):
    print("\n10. What was the longest accident (in hours) recorded in Las Vegas in" + 
          " the Spring (March, April, and May)?")
    print("Displaying the longest accidents of each month in Spring per year:")
    df['Start_Time'] = pd.to_datetime(df['Start_Time'],
                                      format='%-m/%-d/%Y %-H:%-M %p')
    df['End_Time'] = pd.to_datetime(df['End_Time'],
                                      format='%-m/%-d/%Y %-H:%-M %p')

    min_year = df['Start_Time'].dt.year.min()
    max_year = df['Start_Time'].dt.year.max()

    for year in range(min_year, (max_year + 1)):
        print("\n\nThe longest accident recorded in Las Vegas in Spring of",
              year, "was :")
        march = df[(df['Start_Time'].dt.month == 3) & 
                   (df['Start_Time'].dt.year == year)].copy()
        april = df[(df['Start_Time'].dt.month == 4) &
                   (df['Start_Time'].dt.year == year)].copy()
        may = df[(df['Start_Time'].dt.month == 5) &
                   (df['Start_Time'].dt.year == year)].copy()
        if not march.empty:
            march['Time_in_Hours'] = (march['End_Time'] - 
                                      march['Start_Time']).dt.total_seconds() / 3600
            max_time_march = march.loc[march['Time_in_Hours'].idxmax()]
            max_time_id1 = max_time_march['ID']
            row_max_march = df[df['ID'] == max_time_id1]
            print("\nMarch: ", max_time_march['Time_in_Hours'], "hours")
            print(row_max_march)
        else:
            print("\nMarch: No accidents in", year)
        if not april.empty:
            april['Time_in_Hours'] = (april['End_Time'] -
                                      april['Start_Time']).dt.total_seconds() / 3600
            max_time_april = april.loc[april['Time_in_Hours'].idxmax()]
            max_time_id2 = max_time_april['ID']
            row_max_april = df[df['ID'] == max_time_id2]
            print("\nApril: ", max_time_april['Time_in_Hours'], "hours")
            print(row_max_april)
        else:
            print("\nApril: No accidents in", year)
        if not may.empty:
            may['Time_in_Hours'] = (may['End_Time'] -
                                    may['Start_Time']).dt.total_seconds() / 3600
            max_time_may = may.loc[may['Time_in_Hours'].idxmax()]
            max_time_id3 = max_time_may['ID']
            row_max_may = df[df['ID'] == max_time_id3]
            print("\nMay: ", max_time_may['Time_in_Hours'], "hours")
            print(row_max_may)
        else:
            print("\nMay: No accidents in", year)

        #empty the dataframes of each month
        march = pd.DataFrame()
        april = pd.DataFrame()
        may = pd.DataFrame()

def searchStateCityZip(df):
    # Get input from user for the state, city, and zipcode
    print("\nEnter state's abbreviation. For example, CA for California.")
    state = input("Press 'Enter' if no state: ")
    city = input("Enter city. Press 'Enter' if no city: ")
    zipcode = input("Enter zipcode. Press 'Enter' if no zipcode: ")

    # Searches dataframe based on input collected for state, city, and zipcode
    # If no input is inserted for an input, it will be ignorned.
    # If no input is inserted for all 3, exit the function
    if state and city and zipcode:
        search = df[(df['State'] == state) & (df['City'] == city) 
                    & (df['Zipcode'] == zipcode)]
    elif state and city:
        search = df[(df['State'] == state) & (df['City'] == city)]
    elif state and zipcode:
        search = df[(df['State'] == state) & (df['Zipcode'] == zipcode)]
    elif city and zipcode:
        search = df[(df['City'] == city) & (df['Zipcode'] == zipcode)]
    elif state:
        search = df[(df['State'] == state)]
    elif city:
        search = df[(df['City'] == city)]
    elif zipcode:
        search = df[(df['Zipcode'] == zipcode)]
    else:
        print("\nYou have entered nothing for state, city, and zipcode.")
        print("Exiting search...")
        return
    
    # print dataframe after search is done. 
    if search.empty:
        print('\n')
        print("No results found")
    else:
        print('\n')
        print(search)

def checkMonth(month):
    if (int(month) >= 1) and (int(month) <= 12):
        return True
    else:
        print("Value entered for month is not valid.")
        return False

def checkDay(day):
    if (int(day) >= 1) and (int(day) <= 31):
        return True
    else:
        print("Value entered for day is not valid.")
        return False

def searchYearMonthDay(df):
    # Get input from user for the year, month, and day
    print("\n")
    year = input("Enter 4-digit year. Press 'Enter' if no year: ")
    print("Enter month. For example, '3' for March.")
    month = input("Press 'Enter' if no month: ")
    day = input("Enter day. Press 'Enter' if no day: ")

    df['Start_Time'] = pd.to_datetime(df['Start_Time'], 
                                      format='%-m/%-d/%Y %-H:%-M %p')

    # Searches dataframe based on input collected for month, day, and year
    # If no input is inserted for an input, it will be ignorned.
    # If no input is inserted for all 3, exit the function
    if month and day and year: 
        check1 = checkDay(day)
        check2 = checkMonth(month)
        if check1 and check2:
            match = df[(df['Start_Time'].dt.month == int(month)) & 
                       (df['Start_Time'].dt.day == int(day)) & 
                       (df['Start_Time'].dt.year == int(year))]
        else:
            print("Exiting search...")
            return
    elif month and day:
        check1 = checkDay(day)
        check2 = checkMonth(month)
        if check1 and check2:
            match = df[(df['Start_Time'].dt.month == int(month)) & 
                       (df['Start_Time'].dt.day == int(day))]
        else:
            print("Exiting search...")
            return
    elif month and year:
        check1 = checkMonth(month)
        if check1:
            match = df[(df['Start_Time'].dt.month == int(month)) & 
                       (df['Start_Time'].dt.year == int(year))]
        else:
            print("Exiting search...")
            return
    elif day and year:
        check1 = checkDay(day)
        if check1:
            match = df[(df['Start_Time'].dt.day == int(day)) & 
                       (df['Start_Time'].dt.year == int(year))]
        else:
            print("Exiting search...")
            return
    elif month:
        check1 = checkMonth(month)
        if check1:
            match = df[(df['Start_Time'].dt.month == int(month))]
        else:
            print("Exiting search...")
            return
    elif day:
        check1 = checkDay(day)
        if check1:
            match = df[(df['Start_Time'].dt.day == int(day))]
        else:
            print("Exiting search...")
            return
    elif year:
        match = df[(df['Start_Time'].dt.year == int(year))]
    else:
        print("\nNo month, day, or year entered. Exiting search...")
        return

    # print dataframe after search is done.
    if match.empty:
        print('\n')
        print("No results found")
    else:
        print('\n')
        print(match)


def main():
    complete_df = cleanDataFrame()

    # Print cleaned data frame
    print(complete_df)

    question10(complete_df)

    #searchStateCityZip(complete_df)

    searchYearMonthDay(complete_df)

main()
