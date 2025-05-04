from functions import input_number_of_weeks
from functions import input_teams
from functions import generate_weeks
from functions import generate_matchups_v2
from functions import generate_unshuffled_schedule
from functions import print_schedule
from functions import shuffle_so_no_repeats

import time
import random
import msvcrt
import os

time_limit = 10 # used individually for generate and shuffle (up to {time_limit} seconds each)

# 6 weeks 6 teams makes it so that some teams never get to play each other sometimes. Big issue!!! (i may not be able to do a home and away. would have to be swapped later somehow)
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


weeks = generate_weeks(weeknum)
matchups = generate_matchups_v2(teamlist, weeknum)
unshuffled_schedule = generate_unshuffled_schedule(weeks, matchups, teamlist, time_limit)
schedule = shuffle_so_no_repeats(unshuffled_schedule, weeknum, time_limit)

print_schedule(schedule)

while True:
    print("\nHit \"g\" to generate a completely new schedule.\nHit \"s\" to only shuffle the weeks." \
    "\nHit \"c\" to create a copy of the schedule onto a text file on your desktop.\nHit \"q\" to quit.")
    key = msvcrt.getch()

    if key in {b"\x00", b"\xe0"}: # Handle special keys (like arrow keys)
        special = msvcrt.getch() # assigns second code to this variable and never uses it.
        print("\nInvalid input.")
        time.sleep(1.5)
        continue
    
    try:
        key_string = key.decode("utf-8").lower()
    except UnicodeDecodeError:
        print("\nInvalid input.")
        time.sleep(1.5)
        
    if key_string == "g":
        matchups = generate_matchups_v2(teamlist, weeknum)
        unshuffled_schedule = generate_unshuffled_schedule(weeks, matchups, teamlist, time_limit)
        schedule = shuffle_so_no_repeats(unshuffled_schedule, weeknum, time_limit)
        print_schedule(schedule)

    elif key_string == "s":
        random.shuffle(schedule) # Seems redundant but necessary to get out of a perfect schedule that wouldn't need to be shuffled.
        shuffle_so_no_repeats(schedule, weeknum, time_limit)
        print_schedule(schedule)

    elif key_string == "c":

        possible_paths = [
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop"),
        ]

        for path in possible_paths:
            if os.path.exists(path):
                desktop_path = path
                break
        else:
            print("Desktop path not found. Could not create schedule file.")
            time.sleep(1.5)
            continue

        file_path = os.path.join(desktop_path, "schedule.txt")
        
        with open(file_path, "w") as file:
            for week in schedule:
                file.write(f"{week.name}:\n")
                for matchup in week.matchups:
                    file.write(f"{matchup.team1} vs {matchup.team2}\n")
                file.write("\n")
        print(f"\nSchedule copied to {file_path}")

    elif key_string == "q":
        break

    else:
        print("\nInvalid input.")
        time.sleep(1.5)

print("\nGoodbye!")
time.sleep(1.5)
