# date : 13th of july to 15th of july - 2020
# 1. Import necessary libraries 
# ................................................. #
import time
import pandas as pd
import numpy as np
import datetime


# 2. Define global variables 
# ................................................. #

# Dictionary that has the path to the file
CITY_DATA = { 'chicago': 'chicago.csv',
              'newyorkcity': 'new_york_city.csv',
              'washington': 'washington.csv' }


# 3. Define necessary functions 
# ................................................. #
    # 3.1 get user input 
    # .................................................................................. #
def get_filters():
    
    """
        Asks user to specify a city, month, and day to analyze.
        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    #print welcoming message
    print('―'*63)
    print('｜\t  Welcome to BikeShare statistics system \t  ｜')
    print('｜\tYou can filter data by city, month and day!\t  ｜')
    print('―'*63)
    
    #Get user input for city (chicago, new york city, washington)    
    # ................................................. #

    # List to be used later too verify user input 
    city_list=["chicago","newyorkcity","washington"]
    # while the user is inputting invalid input prints "invaild" and keeps going
    while True:
         city= input("｜Would you like chicago, new york city or washington?\n\n")
         # make the input lower and with no spaces to compare it to the city_list list
         city_filtered= city.lower().replace(" ","")
         if city_filtered in city_list:
            #break if the user input matches the any values in the list
            break
         #if there was no match try again message will show
         else: print("!!!! Invalid day, Try again") 
    
    
    # Get user input for month (all, january, february, ... , june)
    # ................................................. #
    month_list=["all","january","february","march","april","may","june"]
    while True:
         month= input("\n｜Which month All, January, February, March, April, May, June? \n\n")
         month_filtered= month.lower().replace(" ","")
         if month_filtered in month_list:
            break
         else: print("!!!! Invalid day, Try again") 

            
    # Get user input for day of week (all, monday, tuesday, ... sunday)
    # ................................................. #
    day_list=["all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    while True:
         day= input("\n｜Which day All, Monday, Tuesday, Wednesday, Thursday, Friday,\n｜Saturday, Sunday?\n\n")
         day_filtered = day.lower().replace(" ","") 
         if day_filtered in day_list:
             break
         else: print("!!!! Invalid day, Try again") 
            
    #Return valid user input
    return city_filtered, month_filtered, day_filtered


    # 3.2 Load data filtered by city, month, day
    # .................................................................................. #
def load_data(city, month, day):
    
    """
        Loads data for the specified city and filters by month and day if applicable.

        Args:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        Returns:
            df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # Load data file into a dataframe, using the dictionary CITY_DATA
    df=pd.read_csv(CITY_DATA[city])
    
    # Convert argument to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Separate the year month and day from start time 
    # and store them in separate column
    df['year'], df['month'],df['day'] = df['Start Time'].dt.year, df['Start Time'].dt.month,df['Start Time'].dt.day
    
    # Get the name of the month instead of number of month, capitalized 
    df['month_of_year']= df['Start Time'].dt.strftime('%B')
    
    # Get the day of the week
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # Get the hour from the time
    df['hour']=df['Start Time'].dt.hour
    
    # If the user choose a specific month filter the dataframe to that month only
    if month != 'all':
        df = df[df['month_of_year']==month.title()]
        
    # If the user choose a specific day filter the dataframe to that day only
    if day != 'all':
        df = df[df['day_of_week']==day.title()]
    
    # Return the dataframe
    return df


    # 3.3 Displays statistics on months, days and hours
    # .................................................................................. #
def time_stats(df):
    """
        Displays statistics on the most frequent times of travel.
    """
    print('―'*63)
    print('｜    The Most Frequent Times and Trip \t\t\t  ｜')
    print('―'*63)
    start_time = time.time()
    
    if('month_of_year' in df.columns):
        # Display the most common month using mode which gets the most frequent 
        common_month = df['month_of_year'].mode()[0]
        print("｜ \t Common Month: ", common_month, "\t\t\t  ｜")
        print('―'*63)
        
    if('day_of_week' in df.columns):
        # Display the most common day of week
        common_day_of_week= df['day_of_week'].mode()[0]
        print("｜ \t Common Day Of Week: ", common_day_of_week, "\t\t  ｜")
        print('―'*63)
        
    if('hour' in df.columns):
        # Display the most common start hour
        common_start_hour=df['hour'].mode()[0]
        print("｜ \t Common Starting Hour: ", common_start_hour, "\t\t\t  ｜")
        print('―'*63)
        
    print("｜   This took %s seconds to calculate \t  ｜" % (time.time() - start_time))
    print('―'*63,'\n\n')

    
    # 3.4 Displays statistics on stations and trip
    # .................................................................................. #
def station_stats(df):
    """
        Displays statistics on the most popular stations and trip.
    """
    
    print('―'*63)
    print('｜    The Most popular stations and trip \t\t  ｜')
    print('―'*63)
    start_time = time.time()
    
    if('Start Station' in df.columns):
        # Display most commonly used start station
        common_start_station = df['Start Station'].mode()[0]
        print("｜  Common Start Station: ", common_start_station, "\t  ｜")
        print('―'*63)
        
    if('End Station' in df.columns):
        # Display most commonly used end station
        common_end_station = df['End Station'].mode()[0]
        print("｜  Common End Station: ", common_end_station, "\t  ｜")
        print('―'*63)
        
    if('Start Station' and 'End Station' in df.columns):
        # Display most frequent combination of start station and end station trip
        df["start_end"]=  df['Start Station']+' => '+df['End Station']+'\t  ｜'
        common_start_end = df['start_end'].mode()[0]
        print("｜  Common start station and end station trip: \t\t  ｜\n｜ ",common_start_end)
        print('―'*63)
        
    print("｜   This took %s seconds to calculate \t  ｜" % (time.time() - start_time))
    print('―'*63,'\n\n')

    
    # 3.5 Displays statistics on the total and average trip duration
    # .................................................................................. #
def trip_duration_stats(df):
    """
        Displays statistics on the total and average trip duration.
    """

    print('―'*63)
    print('｜    statistics on the total and average trip duration \t  ｜')
    print('―'*63)
    start_time = time.time()

    if('Trip Duration' in df.columns):
        # Display total travel time
        total_travel_time = df['Trip Duration'].sum()
        print("｜\t  Total Travel Time: ",total_travel_time, "\t\t  ｜")
        print('―'*63)
        # Display mean travel time
        avg_travel_time = df['Trip Duration'].mean()
        print("｜\t  Average Travel Time: ",avg_travel_time, "\t\t  ｜")
        print('―'*63)
        
    print("｜   This took %s seconds to calculate \t  ｜" % (time.time() - start_time))
    print('―'*63,'\n\n')

    
    # 3.6 Displays statistics on users
    # .................................................................................. #
def user_stats(df):
    """
        Displays statistics on bikeshare users.
    """

    print('―'*63)
    print('｜    Statistics on bikeshare users \t\t\t  ｜')
    print('―'*63)
    start_time = time.time()

    if('User Type' in df.columns):
        # Display counts of user types
        count_user_types = df['User Type'].value_counts()
        print("｜    counts of user types \t\t\t\t  ｜\n\n",count_user_types)
        print('―'*63)
        
    if('Gender' in df.columns):
        # Display counts of gender
        count_gender = df['Gender'].value_counts()
        print("｜    counts of genders \t\t\t\t  ｜\n\n",count_gender)
        print('―'*63)
        
    if('Birth Year' in df.columns):
        # Display earliest, most recent, and most common year of birth 
        earliest_year = df['Birth Year'].min()
        print("｜    Earliest year of birth: ",int(earliest_year), "\t\t\t  ｜") 
        print('―'*63)
    
        recent_year = df['Birth Year'].max()
        print("｜    Most recent year of birth: ",int(recent_year), "\t\t\t  ｜") 
        print('―'*63)

        common_year = df['Birth Year'].mode()[0]
        print("｜    Common year of birth : ",int(common_year), "\t\t\t  ｜")
        print('―'*63)
        
    print("｜   This took %s seconds to calculate \t  ｜" % (time.time() - start_time))
    print('―'*63,'\n\n')

def show_raw_data(df):
    """
        Displays a slice of 5 rows from raw data upon user request.
    """
    num = 0
    #while true display message asking if user want to see raw data
    while True: 
        print('―'*63)
        raw = input('｜Would you like to see raw data about Bikeshare? Enter yes or no\n')
        print('―'*63)
        #if yes print 5 rows and incremeant number by 5 so next time it shows the next 5 rows
        if raw.lower() == 'yes':
            #to show all columns
            pd.set_option('display.max_columns', None)
            #make column width bigger to read all values
            pd.set_option('display.max_colwidth', 200)
            #slice only 5 rows and fill NaN values with 0
            print(df.iloc[num: num+5].fillna(0))
            num+=5
            
        #else stop and break out of the while loop
        else:
            break 
            
def main():
    while True:
        city, month, day = get_filters()
        # Ask user if they want to continue if yes it'll continure if no it will stop
#         stop = input('\n｜ Would you like to continue? Enter yes or no.\n')
#         if stop.lower() != 'yes':
#             break
        df = load_data(city, month, day)
        
        #get time stats
        time_stats(df)
        #get station stats
        station_stats(df)
        #get duration stats
        trip_duration_stats(df)
        #get user stats
        user_stats(df)
        #get raw data
        show_raw_data(df)
        
        # Ask user if they want to restart and test with different input, if yes it'll restart if no it'll stop
        restart = input('\n｜Would you like to restart? Enter yes or no \n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
