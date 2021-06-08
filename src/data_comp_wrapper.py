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
    myFmt = mdates.DateFormatter('%I%p') # Create a formatting function for x axis datetimes    
    ax.xaxis.set_major_formatter(myFmt) # Format the datetimes on the x axis    
    ax.set_ylim(bottom = 0, top = 100) # Set the limits of the y axis    
    ax.plot(datetimes, levels) # Plot the data    
    fig.savefig("test-chart")    


# get_smooth_levels(levels: number[]): number[]
def get_smooth_levels(levels):
    smooth_arr = []

    i = 0
    while(i < len(levels)):
        right_index = __get_range(i, levels)    # get the right edge of the line run
        local_total = 0  # Total up all points in the line run to calc an average

        j = 0
        while(j <= right_index): # Loop through points in the line run an total up
            local_total += levels[j]
            j += 1

        local_total /= (right_index - i)

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
            break
        i += 1

    return i

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

    return (inc, dec)
