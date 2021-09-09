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

    print("Hello! Let\'s explore some US bikeshare data!")
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    """
    String Formatting Woes
        Already used .format where it's possible. More information on refactoring (beside 2 links) would be great.
        No idea how I can improve the code.
    """

    cities = ["chicago", "new york city", "washington"]
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city not in cities:
            print("There is no data for '{}'. Please try again.\n".format(city))
            continue
        else:
            print("...Filtering data for '{}'. If this is not true, restart the program now.\n".format(city))
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ["january", "february", "march", "april", "may", "june", "all"]
    while True:
        month = input("Please select a month: January, February, March, April, May, June, or 'all'\n").lower()
        if month not in months:
            print("There is no data for '{}'. Please try again.\n".format(month))
            continue
        else:
            print("...Filtering data for '{}'. If this is not true, restart the program now.\n".format(month))
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]
    while True:
        day = input("Please select a day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or 'all'\n").lower()
        if day not in days:
            print("There is no data for '{}'. Please try again.\n".format(day))
            continue
        else:
            print("...Filtering data for '{}'. If this is not true, restart the program now.\n".format(day))
            break

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':

        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # TO DO: display the most common month
    print("Most common month (1: Jan, 2: Feb, 3: Mar, etc.):\n", df['month'].value_counts()[0:1])

    # TO DO: display the most common day of week
    print("\nMost common day of week:\n", df['day_of_week'].value_counts()[0:1])

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nMost common start hour:\n", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # TO DO: display most commonly used start station
    mcuss = df['Start Station'].value_counts().idxmax() #mcuss = most commonly used start station
    print("Most commonly used start station:\n ", mcuss)

    # TO DO: display most commonly used end station
    mcues = df['End Station'].value_counts().idxmax() #mcues = most commonly used end station
    print("\nMost commonly used end station:\n ", mcues)

    # TO DO: display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)[0:1]
    print("\nMost frequent combination:\n", combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time (in hours):\n", df['Trip Duration'].sum()/360)

    # TO DO: display mean travel time
    print("\nMean travel time (in minutes):\n", df['Trip Duration'].mean()/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # TO DO: Display counts of user types
    print("User types:\n", df['User Type'].value_counts())

    # TO DO: Display counts of gender
    print("\nCounts of gender:")
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())
    else:
        print("No data given")

    # TO DO: Display earliest, most recent, and most common year of birth
    print("\nDate of Birth:")

    if 'Birth Year' in df.columns:
        mean_dob = df['Birth Year'].mean() #create mean for "Birth Year column in case of NaN"
        df['Birth Year'].fillna(value=mean_dob, inplace=True) #replace NaN with mean-value
        print("Earliest:\n", int(df['Birth Year'].min()))
        print("Most recent:\n", int(df['Birth Year'].iloc[-1]))
        print("Most common:\n", int(df['Birth Year'].mode()[0]))
    else:
            print("No data given")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)

def display_data(df):
    """Displays 5 lines of row data if the user wants to see"""
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no.\n')
    start_loc = 0
    end_loc = 5
    while view_data == "yes":
        print(df.iloc[start_loc:end_loc])
        start_loc += 5
        end_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        view_data = view_display

    """If I would know how to improve the code, I would have done it already"""
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
