import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    """get user input for city (chicago, new york city, washington)"""
    city = ""
    time_filter = ""
    month = ""
    day = ""
    city = str(input("Please type the name of the city you'd like to analyse from the list:\n New York City\n Chicago\n Washington\n")).lower()
    while city not in ['new york city','chicago','washington']:
        city = str(input("Please type the name of the city you'd like to analyse from the list:\n New York City\n Chicago\n Washington\n")).lower()
    month = str(input("Type in the month you'd like to filter on, \nData for analysis is available for January, February, March, April, May and June\n Or type 'all' for no filter on month: \n")).lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june','all']:
        month = str(input("Which month? Data for analysis is available for January, February, March, April, May and June\n")).lower()
    day = str(input("Which day do you want to filter on? E.g., Sunday, Monday, ..., Saturday)\n Or type 'all' for no filter on day: \n")).title()
    while day not in ['Sunday','Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','All']:
        day = str(input("Which day do you want to filter on? E.g., Sunday, Monday, ..., Saturday)\n Or type 'all' for no filter on day: \n")).title()
    return city, month, day
print('-'*40)
    

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    """extract month and day of week from Start Time to create new columns"""
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    """filter by month if applicable"""
    if month != 'all':
        """use the index of the months list to get the corresponding int"""
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        """filter by month to create the new dataframe"""
        df = df[df['month'] == month]

    """filter by day of week if applicable"""
    if day != 'All':
        """filter by day of week to create the new dataframe"""
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.weekday_name
    """ Display the most common month"""
    popular_month = df['month'].mode()[0]
    print ('The most common month is: ', popular_month)
    """display the most common day of week"""
    popular_day = df['day_of_week'].mode()[0]
    print ('The most common day of week is: ', popular_day)
    """display the most common start hour"""
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """ Display most commonly used start station"""
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station)
    """ Display most commonly used end station"""
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station)
    """ Display most frequent combination of start station and end station trip"""
    df['Popular Stations'] = '\nStart Station: '+df['Start Station'] +' | End Station: '+df['End Station']
    popular_stations = df['Popular Stations'].mode()[0]
    print('Most Popular Station Combination:', popular_stations) 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """ Display total travel time"""
    total_travel_time = df['Trip Duration'].sum()
    print ("Total Travel Time: ", total_travel_time)
    """ Display mean travel time"""
    mean_travel_time = df['Trip Duration'].mean()
    print ("Mean Travel Time: ", mean_travel_time)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """ Display counts of user types"""
    count_users = df['User Type'].value_counts()
    print ('Count Number of each user type: \n', count_users)

    try:
        count_gender = df['Gender'].value_counts()
        print('Count Number of each Gender: \n', count_gender)
    except KeyError: 
        print('There is no Gender column for washington dataset')
    """ Display counts of gender"""
    try:
        most_recent_birthyear = int(df['Birth Year'].max())
        print('Most recent year of birth: ', most_recent_birthyear)
        earliest_birthyear = int(df['Birth Year'].min())
        print('Earliest year of birth: ', earliest_birthyear)
        most_common_birthyear = int(df['Birth Year'].mode())
        print('Most common year of birth: ', most_common_birthyear)
        
    except KeyError: 
        print('There is no birthyear column for Washington dataset')

    """Display earliest, most recent, and most common year of birth"""

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data (df):
    view_raw = input('\nWould you like to view individual trip data? Enter yes or no.\n')
    while True:
        if view_raw.lower() not in ['yes','no']:
             view_raw = input('\nWould you like to view individual trip data? Enter yes or no.\n')
        elif view_raw.lower() == 'no':
            break
        else:
            i = 0
            while i < len(df):
                i += 5
                if i >= len(df):
                    print('No more data to display.\n')
                else: 
                    print(df.iloc[i-5 : i])
                    
                    view_raw = input('\n Type Yes to view 5 more rows, No to end this view.\n')
                    if view_raw.lower() != 'yes':
                                     break

                    
                    
     
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
 
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main()