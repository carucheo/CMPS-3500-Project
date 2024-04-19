## ######################################################################  ##
## GROUP 6                                                                 ##
## NAME: Alberto Munoz, Everardo Robles Tena, Karen Santiago, Jose Zamora  ##
## ASGT: Group Projec                                                      ##
## ORGN: CSUB - CMPS 3500                                                  ##
## FILE: clean_csv.py                                                      ##
## DATE: 04/19/2024                                                        ##
## #########################################################################

import pandas as pd
import numpy as np
import datetime as dtime

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

    # Create a copy of cleaned_thrice data frame to resolve a runtime error
    cleaned_four = cleaned_thrice.copy()
    # Only consider the first 5 digits of the zip code and reassign them back to column
    cleaned_four['Zipcode'] = cleaned_four['Zipcode'].str[:5]

    # Create 'datetime objects' for arithmetic operations & elim. rows equal to 0 mins
    cleaned_four['Start_Time'] = pd.to_datetime(cleaned_four['Start_Time'])
    cleaned_four['End_Time'] = pd.to_datetime(cleaned_four['End_Time'])
    fully_cleaned_df = cleaned_four[(cleaned_four['End_Time'] - cleaned_four['Start_Time']).dt.total_seconds() / 60 > 0]

    return fully_cleaned_df

# Checks for similiar severity in 3 States
def commonSeverity():
    # Store the data frame into a variable
    clean_df_one = cleanDataFrame()
    # Filter the data frame to include only accidents from VA, CA, and FL
    check_states = clean_df_one[clean_df_one['State'].isin(['VA', 'CA', 'FL'])]
    # Group the filtered data frame by severity and count the occurrences of each severity level
    severity_level = check_states['Severity'].value_counts()
    # Find the severity level with the highest count
    most_common_severity = severity_level.idxmax()

    print("The most common severity in VA, CA, and FL is: ", most_common_severity)
    print()

# Check for the top 5 cities with the most accidents in CA    
def californiaCityAccidents():
    # Store the data frame into a variable
    clean_df_two = cleanDataFrame()
    #Filer the data frame to include only accidents in CA
    ca_accidents = clean_df_two[clean_df_two['State'].isin(['CA'])]
    # Extract the year from 'Start_Time' dt object
    ca_accidents_fix = ca_accidents.copy()
    ca_accidents_fix['Year'] = ca_accidents_fix['Start_Time'].dt.year
    # Group by city and year, then count the number of accidents
    city_year_accidents = ca_accidents_fix.groupby(['City', 'Year']).size().reset_index(name = 'Accident Count')
    city_year_accidents_sorted = city_year_accidents.sort_values(by = ['Year', 'Accident Count'], ascending = [True, False])
    print("Top 5 cities with the most accidents in California per year:")
    print()

    # Display the top 5 cities with the most accidents for each year
    for year in city_year_accidents_sorted['Year'].unique():
        top_cities_year = city_year_accidents_sorted[city_year_accidents_sorted['Year'] == year].head(5)
        print(top_cities_year.to_string(index = False)) #remove index number from output
        print()

def question_7(clean_df):
    nyc_data = clean_df[clean_df['City'].isin(['New York'])]
    nyc_data_by_weather = nyc_data['Weather_Condition'].value_counts()
    nyc_data = nyc_data.sort_values(by='Start_Time')
    nyc_data['Month'] = nyc_data['Start_Time'].apply(lambda x: "%d" % (x.month)).astype(int)

    now = dtime.datetime.now()
    now = now.strftime("%I:%M:%S %p")
    # now = now.strftime("%H:%M:%S")

    print("")
    print(f"[{now}] 7. What are the 3 most common weather conditions (weather_conditions) when accidents occurred in New York city? Display the data per month.")
    print(f"[{now}] The 3 most common weather conditions when accidents occurred in New York city: ")
    print(f"[{now}]\n")
    print(nyc_data_by_weather.head(3))
    print("")
    print(f"[{now}] Here is each weather condition experienced in New York City per month:")
    print(f"[{now}]\n")
    print(nyc_data.groupby(['Month', 'Weather_Condition']).size())
    print("")

def question_8(clean_df):
    nh_data = clean_df[clean_df['State'].isin(['NH'])]
    nh_data_by_sev_two = nh_data.loc[nh_data['Severity'] == 2]
    nh_data_final = nh_data_by_sev_two['Visibility(mi)'].max()

    now = dtime.datetime.now()
    now = now.strftime("%I:%M:%S %p")

    print("")
    print(f"[{now}] 8. What was the maximum visibility of all accidents of severity 2 that occurred in the state of New Hampshire?")
    print(f"[{now}] The maximum visibility of all accidents of severity 2 that occurred in the state of New Hampshire: {nh_data_final} miles")
    print("")

def question_9(clean_df):
    bak_data = clean_df[clean_df['City'].isin(['Bakersfield'])]
    # bak_data_by_severity = bak_data['Severity'].value_counts()[bak_data['Severity'].unique()]
    bak_data_by_severity = bak_data['Severity'].value_counts().sort_index()
    # bak_data_by_severity = bak_data.groupby('Severity')['Severity'].value_counts().sort_values(ascending=False)
    bak_data = bak_data.sort_values(by='Start_Time')
    bak_data['Year'] = bak_data['Start_Time'].apply(lambda x: "%d" % (x.year))

    now = dtime.datetime.now()
    now = now.strftime("%I:%M:%S %p")

    print("")
    print(f"[{now}] 9. How many accidents of each severity were recorded in Bakersfield? Display the data per year.")
    print(f"[{now}] Accidents based on what severity was recorded in Bakersfield:")
    print(f"[{now}]")
    print("")
    print(bak_data_by_severity)
    print("")
    print(f"[{now}] Here is the number of accidents per severity level recorded in Bakersfield per year:")
    print(f"[{now}]\n")
    print(bak_data.groupby(['Year', 'Severity']).size())
    print("")

def main():
    complete_df = cleanDataFrame()
    
    # Print cleaned data frame
    print(complete_df)
    print()
    
    # Print most common severity of 3 states
    commonSeverity()
    
    # Print cities with most accidents in CA
    californiaCityAccidents()

    # print(complete_df)
    question_7(complete_df)
    question_8(complete_df)
    question_9(complete_df)

main()
