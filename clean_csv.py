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
import time

# set full dataframe for display
'''
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
'''

# Read and assign csv data into 'raw_data' variable
#raw_data = pd.read_csv('US_Accidents_data.csv')

# Create a data frame from our csv dataraw_data
#data_frame = pd.DataFrame(raw_data, columns = ['ID', 'Severity', 'Start_Time', 'End_Time', 'Distance(mi)', 
                                               #'Description', 'City', 'County', 'State', 'Zipcode', 'Country', 
                                               #'Timezone', 'Weather_Timestamp', 'Temperature(F)', 'Humidity(%)', 
                                               #'Pressure(in)', 'Visibility(mi)', 'Precipitation(in)', 'Weather_Condition'])

def cleanDataFrame(data_frame):
    print("Processing Input Data Set:")
    print("***********************")
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")
    print(f"[{(current_time)}] Starting Script")
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
    cleaned_four['Start_Time'] = pd.to_datetime(cleaned_four['Start_Time'], format = 'mixed') # Note: added format = 'mixed'
    cleaned_four['End_Time'] = pd.to_datetime(cleaned_four['End_Time'], format = 'mixed')
    fully_cleaned_df = cleaned_four[(cleaned_four['End_Time'] - cleaned_four['Start_Time']).dt.total_seconds() / 60 > 0]

    print(f"[{current_time}] Performing Data Clean Up")
    print(f"[{current_time}] Total Rows Read After Cleaning Is: {len(fully_cleaned_df)}")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nTime to clean is: {total_time: .2f} seconds")

    return fully_cleaned_df

# Load data function 
def load_data():

    # Ask user for file
    raw_data = input("Enter the name of your raw_data (with extension): ")
    print("Loading input data set:")
    print("***********************")

    # Set variables to track total time
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")
    print(f"[{(current_time)}] Starting Script")
    
    try: 
        data_frame = pd.read_csv(raw_data)
        print(f"[{current_time}] Loading {raw_data}")
        print(f"[{current_time}] Total Columns Read: {len(data_frame.columns)}")
        print(f"[{current_time}] Total Rows Read: {len(data_frame)}")
        end_time = time.time()
        total_time = end_time - start_time
        print(f"\nTime to load is: {total_time: .2f} seconds")
        return data_frame
    except FileNotFoundError:
        print(f"Error: raw_data '{raw_data}' not found.")
        return None

# The first four Output question
def output1(data_frame):
    
    print("Answering Questions:")
    print("***********************")

    # Begining of Question 1
    # Set variables to track time
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")

    # Get the Year and Month from Start_Time column
    data_frame['Year'] = data_frame['Start_Time'].dt.year
    data_frame['Month'] = data_frame['Start_Time'].dt.month

    # Group by Year & Month, count total accidents
    monthly_data = data_frame.groupby(['Year', 'Month']).size().reset_index(name = 'Total_Accidents')

    # Sort accidents by descedning order to leave highest accidents on top rows
    sorted_monthly = monthly_data.sort_values(by = 'Total_Accidents', ascending = False)

    # Months with most accidents are now in the top 3 rows
    highest_accidents = sorted_monthly.head(3)

    end_time = time.time()
    total_time = end_time - start_time

    print("The top 3 months with the most accidents are:")
    for index, row in highest_accidents.iterrows():
        print(f"[{current_time}] Month: {row['Month']}, Total Accidents: {row['Total_Accidents']}")

    #### End of Question 1 ####
        
    # Beginning of Question 2 
        
    # Group by year, count total accidents
def output2(data_frame):
    
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")

    yearly_data =  data_frame.groupby('Year').size().reset_index(name ='Total_Yearly_Accidents')

    top_year = yearly_data.loc[yearly_data['Total_Yearly_Accidents'].idxmax()]

    end_time = time.time()
    total_time = end_time - start_time

    print("The year with the highest amount of accidents reported is: ")
    print(f"[{current_time}] Year: {top_year['Year']}, Total Accidents: {top_year['Total_Yearly_Accidents']}")
    
    ### End of Question 2 ###

def output3(data_frame):

    # Filter to only include severity 2 
    severity_2 = data_frame[data_frame['Severity'] == 2]

    # Group by year and state, count accidents
    yearly_state_accidents = severity_2.groupby(['Year', 'State']).size().reset_index(name='Total_Accidents')

    # Find the state with the most accidents for each year
    state_severity = yearly_state_accidents.loc[yearly_state_accidents.groupby('Year')['Total_Accidents'].idxmax()]

    #Sort by descending order
    sorted_state_severity = state_severity.sort_values( by = 'Total_Accidents' , ascending = False)

    #Get state with highest accidents
    top_state_severity = sorted_state_severity.head(1)

    print("The the state that had the most accidents of severity 2 is: ")
    print(top_state_severity)
        

    
# Checks for similiar severity in 3 States
def commonSeverity(data_frame):
    # Store the data frame into a variable
    #clean_df_one = cleanDataFrame()
    # Filter the data frame to include only accidents from VA, CA, and FL
    check_states = data_frame[data_frame['State'].isin(['VA', 'CA', 'FL'])]        #Switched from clean_df_one
    # Group the filtered data frame by severity and count the occurrences of each severity level
    severity_level = check_states['Severity'].value_counts()
    # Find the severity level with the highest count
    most_common_severity = severity_level.idxmax()

    print("The most common severity in VA, CA, and FL is: ", most_common_severity)
    print()

# Check for the top 5 cities with the most accidents in CA    
def californiaCityAccidents(data_frame):
    # Store the data frame into a variable
    #clean_df_two = cleanDataFrame()
    #Filer the data frame to include only accidents in CA
    ca_accidents = data_frame[data_frame['State'].isin(['CA'])]     # Switched from clean_df_two
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
    while True:
        print("\nMenu:")
        print("(1) Load Data")
        print("(2) Process Data")
        print("(3) Print Answers")
        print("(4) Search Accidents (City, State, and Zip Code)")
        print("(5) Search Accidents (Year, Month, and Day)")
        print("(6) Search Accidents (Temperatute Range and Visibility Range)")
        print("(7) Quit")

        choice = input("Please enter your choice: ")

        if choice == '1':
            data_frame = load_data()
        elif choice == '2':
            fully_cleaned_df = cleanDataFrame(data_frame)
        elif choice == '3':
            output1(fully_cleaned_df)
            output2(fully_cleaned_df)
            output3(fully_cleaned_df)
            commonSeverity(fully_cleaned_df)
            californiaCityAccidents(fully_cleaned_df)
            question_7(fully_cleaned_df)
            question_8(fully_cleaned_df)
            question_9(fully_cleaned_df)

        elif choice == '4':
            pass
        elif choice == '5':
            pass
        elif choice == '6':
            pass
        elif choice == '7':
            print("Goodbye")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
            #Implement feauture to print Total Runnign Time
            # "Total Running Time (In Minutes): <Answer>"

main()
