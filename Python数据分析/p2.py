import time
from datetime import datetime
from itertools import zip_longest

import dateparser
import matplotlib.dates as mdates
import pandas as pd
from matplotlib.pyplot import subplots, xlabel, tight_layout, style
from pylab import savefig

start = time.time()


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


style.use("ggplot")
data = pd.read_csv("euro.csv")
data["date"] = data.registered_db.apply(lambda x: dateparser.parse(x))

all_teams = data.groupby("team_name").decimal_odds.mean()
all_teams.sort_values(inplace=True)
all_teams = all_teams.keys().values

date_formatter = mdates.DateFormatter("%D")

# create 8 plots each one with 4 teams
for y, team_chunk in enumerate(grouper(all_teams, 4), 0):
    fig, ax = subplots(len(team_chunk), sharex=True)

    for i, team_name in enumerate(team_chunk, 0):
        team_data = data[data.team_name == team_name]
        ax[i].plot(team_data.date.astype(datetime), team_data.decimal_odds, "--", label=team_name)
        ax[i].set_title(team_name)
        ax[i].xaxis.set_major_formatter(date_formatter)
        # try to adjust y axis range so that all lines are clearly visible
        total_range = max(team_data.decimal_odds) - min(team_data.decimal_odds)
        total_range_to_adjust = total_range * 0.2
        ax[i].set_ylim([min(team_data.decimal_odds) - total_range_to_adjust,
                        max(team_data.decimal_odds) + total_range_to_adjust])

    fig.subplots_adjust(hspace=0)
    xlabel("Date")
    tight_layout()
    filename = "euro{}.png".format(y)
    savefig(filename)

print(time.time() - start)
