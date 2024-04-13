import pandas as pd
import numpy as np
import time


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

# Load data function 
def load_data():

    file = input("Enter the name of your file (with extension): ")
    print("Loading input data set:")
    print("***********************")
    start_time = time.time()
    current_time = time.strftime("%H:%M:%S")
    print(f"[{(current_time)}] Starting Script")
    
    try: 
        dframe = pd.read_csv(file)
        print(f"[{current_time}] Loading {file}")
        print(f"[{current_time}] Total Columns Read: {len(dframe.columns)}")
        print(f"[{current_time}] Total Rows Read: {len(dframe)}")
        end_time = time.time()
        total_time = end_time - start_time
        print(f"\nTime to load is: {total_time: .2f} seconds")
        return dframe
    except FileNotFoundError:
        print(f"Error: File '{file}' not found.")
        return None

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
            load_data()
        elif choice == '2':
            pass
        elif choice == '3':
            pass
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
