# Module imports
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# My imports
import logger
import get_prop

CHART_FILE = get_prop.get_prop("CHART_FILE", "s")
THRESHOLD = 0.5

# create_chart(levels: number[], datetimes: datetime[]): String
def create_chart(levels, datetimes):
    fig, ax = plt.subplots(1, 1) # Start creating a chart with axes    
    myFmt = mdates.DateFormatter('%I %p') # Create a formatting function for x axis datetimes    
    ax.xaxis.set_major_formatter(myFmt) # Format the datetimes on the x axis    
    ax.set_ylim(bottom = 0, top = 100) # Set the limits of the y axis    
    ax.grid(axis = 'y') # Add horizontal grid lines
    ax.set_xlabel("Time") # Add x axis label
    ax.set_ylabel("Percent Full") # Add y axis label
    ax.set_title("Percent vs time") # Add chart title
    ax.plot(datetimes, levels) # Plot the data    
    fig.savefig(CHART_FILE)    


# get_smooth_levels(levels: number[]): number[]
def get_smooth_levels(levels):
    smooth_arr = []

    i = 0
    while(i < len(levels)):
        right_index = __get_range(i, levels)    # get the right edge of the line run
        local_total = 0  # Total up all points in the line run to calc an average

        j = i
        while(j <= right_index): # Loop through points in the line run an total up
            local_total += levels[j]
            j += 1

        local_total /= (right_index - i + 1)

        j = i
        while(j <= right_index):    # Add the new flat value for each entry in the line run
            smooth_arr.append(local_total)
            j += 1

        i = right_index + 1

    return smooth_arr

# __get_range(index: int, arr: number[]): int
def __get_range(index, arr):
    """
    returns:
        the index of the last value that doesn't violate the threshold
    """

    i = index
    while(i < len(arr)):
        if(abs(arr[i] - arr[index]) > THRESHOLD):
            return i - 1    # This index breaks rule so return the previous one
                            # This will never force for i = index because the diff will always be zero
                            # so a previous index can't be returned
        i += 1

    return len(arr) - 1

# get_inc_dec(levels: number[]): (number, number)
def get_inc_dec(levels):
    inc = 0
    dec = 0

    i = 0
    while(i < len(levels) - 1): #don't want to reach index of last element
        diff = levels[i + 1] - levels[i]
        if(diff < 0):
            dec -= diff
        elif(diff > 0):
            inc += diff
        i += 1

    return (inc, dec)

# percent_to_gallon(percent: number): number
def percent_to_gallon(percent):
    CUBIC_FT_TO_GALLON = 7.481
    WELLMAN_FULL_HEIGHT = 59 / 12
    WELLMAN_LENGTH = 36 / 12
    WELLMAN_WIDTH = 23 / 12
    WELLMAN_USABLE_HEIGHT = 52.25 / 12

    return (WELLMAN_USABLE_HEIGHT * (percent / 100)) * WELLMAN_LENGTH * WELLMAN_WIDTH * CUBIC_FT_TO_GALLON
