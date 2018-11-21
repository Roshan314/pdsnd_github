import time
import pandas as pd
import numpy as np
import calendar as cal

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city=input("Would you like to see data for Chicago, New York, or Washington?:  ")
        city=city.lower()
        if city not in ("chicago","new york","washington"):
            print("Not a valid choice (ex. Chicago, New York, Washington)")
        else:
            break

    while True:
        choice_in=input("\nWhat type of filter would you like to apply?  Month, day, both, or none:  ")
        choice_in = choice_in.lower() 
        if choice_in not in ("month","day","both","none"):
            print ("Not a valid choice (ex. month, day, both, not at all)")
        else:
            break


    # get user input for month (all, january, february, ... , june)
    if choice_in in ("month","both"):
        while True:
            month=input("\nWhich month? January, February, March, April, May, or June:  ")
            month=month.lower()
            if month not in ("january","february","march","april","may","june"):
                print ("Not a valid choice (ex. January-June)")
            else:
                break
    else:
        month="all"

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if choice_in in ("day","both"):
        while True:
            day=input("\nWhat day? Please type a day Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday:  ")
            day=day.title()
            if day not in ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"):
                print ("Not a valid choice (ex. Monday-Sunday)")
            else:
                break
    else:
        day="all"

    print('-'*40)

    return city, month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

 
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most Popular Travel Month: ', df['month'].mode()[0])


    # display the most common day of week
    print('Most Popular Travel Day of the week:', df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most Popular Start Hour:', df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most popular start station: ", df['Start Station'].mode()[0])
    print()

    # display most commonly used end station
    print("Most popular end station: ", df['End Station'].mode()[0])
    print()

    # display most frequent combination of start station and end station trip
    combo=df.groupby(['Start Station','End Station'])['Trip Duration'].size().idxmax()
    print("\nThe most frequent combination goes from {} station to {} station".format(*combo))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    # display total travel time
    print("Total travel time: ", df['Trip Duration'].sum())
    print()

    # display mean travel time
    print("Mean travel time: ", df['Trip Duration'].mean())
    print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    print(df['User Type'].value_counts())
    print()

    # Display counts of gender
    try:
        print(df['Gender'].value_counts())
    except:
        pass    
    print()
  

    # Display earliest, most recent, and most common year of birth

    try:
        print("Earliest Birth Year: ",int(df['Birth Year'].min()))
        print("\nRecent Birth Year: ",int(df['Birth Year'].max()))
        print("\nCommon Birth Year: ",int(df['Birth Year'].mode()[0]))
    except:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:


        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


#    while True:
#        city=input("Would you like to see data for Chicago, New York, or Washington?:  ")
#        city=city.lower()
#        if city not in ("chicago","new york","washington"):
#            print("Not a valid choice (ex. Chicago, New York, Washington)")
#        else:
#            break

        see_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
        if see_data.lower() == "yes":
            print(df.iloc[0:5])
            i=0
            see_more='yes'
            while see_more=='yes':
                see_more=input('\nWould you like to see more? Enter yes or no.\n')
                if see_more.lower()  != 'yes':
                    break
                else:
                    i+=5
                    print(df.iloc[i:(i+5)])
                    if (i+5)>=df.last_valid_index():
                        print("\nYou have reached end of index")
                        see_more='no'
                        break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in ("yes", "y"):
            break

        print()


if __name__ == "__main__":
	main()
