from functions import input_number_of_weeks
from functions import input_teams
from functions import generate_weeks
from functions import generate_matchups
from functions import generate_schedule
from functions import print_schedule
from functions import shuffle_so_no_repeats

import time
import random


# 4 weeks 4 teams makes it so that some teams never get to play each other sometimes. Big issue!!! (i may not be able to do a home and away. would have to be swapped later somehow)
has_weeknum = False
has_teamlist = False

while not has_weeknum:
    try:
        weeknum = input_number_of_weeks()
        has_weeknum = True
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        time.sleep(1.5)

while not has_teamlist:
    try:
        teamlist = input_teams()
        #has_teamlist = True
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        time.sleep(1.5)

    has_duplicates = len(teamlist) != len(set(teamlist)) # Check for duplicates in the team list
    if has_duplicates:
        print("Duplicate team names found. Please enter unique team names.")
        time.sleep(1.5)
    else:
        has_teamlist = True



time_limit = 20
weeks = generate_weeks(weeknum)
matchups = generate_matchups(teamlist, weeknum)

schedule = generate_schedule(weeks, matchups, teamlist, time_limit, weeknum)

print_schedule(schedule)

finished = False
while not finished:
    selection = input("\nType \"g\" to generate a completely new schedule, \"s\" to only shuffle the weeks, or \"q\" to quit: ").lower()

    if selection == "g":
        matchups = generate_matchups(teamlist, weeknum)
        schedule = generate_schedule(weeks, matchups, teamlist, time_limit, weeknum)
        print_schedule(schedule)

    elif selection == "s":
        random.shuffle(schedule) # Seems redundant but necessary to get out of a perfect schedule that wouldn't need to be shuffled.
        shuffle_so_no_repeats(schedule, weeknum)
        print_schedule(schedule)

    elif selection == "q":
        finished = True

    else:
        print("Invalid input. Please enter \"g\", \"s\", or \"q\".")
        time.sleep(1.5)

print("Goodbye!")
time.sleep(1.5)
