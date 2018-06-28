import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
CITIES = ['chicago', 'new york city', 'washington']
CITIES_STR = ', '.join(CITIES)

WAYS_FOR_FILTER = ['month', 'day', 'all']
WAYS_STR = ', '.join(WAYS_FOR_FILTER)

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June']
MONTHS_STR = ', '.join(MONTHS)

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
DAYS_STR = ', '.join(DAYS)

MONTH_TO_NUMBER = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6}
NUMBER_TO_MONTH = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    invalid_msg = 'Invalid Input. Only "{}" accepted, please try again'

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Would you like to see data for "{}"? --- Please input : \n'.format(CITIES_STR))
            if city not in CITIES:
                print(invalid_msg.format(CITIES_STR))
                continue
            break
        except ValueError:
            print(invalid_msg.format(CITIES_STR))

    # get user input for month (all, january, february, ... , june)

    month, day = ('all', 'all')
    while True:
        try:
            way_of_filter = input('Would you like to filter the data by "{}"? --- Please input : \n'.format(WAYS_STR))
            if way_of_filter not in WAYS_FOR_FILTER:
                print(invalid_msg.format(WAYS_STR))
                continue
            break
        except ValueError:
            print(invalid_msg.format(WAYS_STR))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if way_of_filter == 'month':

        while True:
            try:
                month = input('Which month - "{}"? --- Please input : \n'.format(MONTHS_STR))
                if month not in MONTHS:
                    print(invalid_msg.format(MONTHS_STR))
                    continue
                break
            except ValueError:
                print(invalid_msg.format(MONTHS_STR))

    elif way_of_filter == 'day':

        while True:
            try:
                day = input('Which day - "{}" --- Please input : \n'.format(DAYS_STR))
                if day not in DAYS:
                    print(invalid_msg.format(DAYS_STR))
                    continue
                break
            except ValueError:
                print(invalid_msg.format(DAYS_STR))

    print('-' * 40)
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == MONTH_TO_NUMBER[month]]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_often_month = df['month'].mode()[0]
    print('the most common month is : {}'.format(NUMBER_TO_MONTH[most_often_month].title()))

    # Display the most common day of week
    most_often_dayofweek = df['day_of_week'].mode()[0]
    print('the most common day of week is : {}'.format(most_often_dayofweek))

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_often_hour = df['hour'].mode()[0]
    print('the most common start hour is : {}'.format(most_often_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('the most commonly used start station is : {}'.format(most_common_start_station))
    # print(df['Start Station'].value_counts())

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('the most commonly used end station is : {}'.format(most_common_end_station))

    # TODO: display most frequent combination of start station and end station trip
    most_frequent_combin_station = df.groupby(['Start Station', 'End Station'], sort=False).size().idxmax()
    print('the most frequent combination of start station and end station trip is fron "{0}" to "{1}"'.format(
        *most_frequent_combin_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('total travel time is : {} seconds'.format(df['Trip Duration'].sum()))

    # Display mean travel time
    print('total travel time is : {} seconds'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('counts of user type is : \n{}\n'.format(df['User Type'].value_counts()))

    # Display counts of gender
    print('counts of gender is : \n{}\n'.format(df['Gender'].value_counts()))

    # Display earliest, most recent, and most common year of birth
    print('earliest year of birth is : {}'.format(int(df['Birth Year'].min())))
    print('most recent year of birth is : {}'.format(int(df['Birth Year'].max())))
    print('most common year of birth is : {}'.format(int(df['Birth Year'].value_counts().idxmax())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        try:
            city, month, day = get_filters()
        except KeyboardInterrupt:
            break
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if not city == 'washington':
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
