import pandas as pd
import numpy as np
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

    # Create a copy of cleaned_thrice dataframe to resolve a runtime error
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
