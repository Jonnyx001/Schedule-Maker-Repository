import random
import time
from classes import Matchup
from classes import Week
from operator import attrgetter


def input_number_of_weeks():
    return int(input("How many weeks are in your regular season?: "))


# Allows user to build a list of team names. Strings.
def input_teams():
    try:
        teamnum = int(input("How many teams are in your league?: "))
    except ValueError:
        print("Invalid input. Please enter a whole number.")
        time.sleep(1.5)
        return input_teams()
    
    teamlist = []
    for i in range(teamnum):
        team = input(f"Enter team {i + 1}: ")
        teamlist.append(team)

    if len(teamlist) % 2 != 0:
        teamlist.append("BYE")

    max_length = max(len(team) for team in teamlist)
    padded_teamlist = [team.ljust(max_length) for team in teamlist]

    print("Registration complete.")
    return padded_teamlist


# User inputs number of weeks. This outputs a list of week objects with a name like "Week 1" ready to have matchups appended to it as nested objects.
def generate_weeks(weeknum):
    weeks = []
    for i in range(weeknum):
        newweek = Week(f"Week {i + 1}") # Name will be changed later after schedule is shuffled to avoid back to back games with same opp.
        weeks.append(newweek)
    return weeks


# Takes a list of team names and generates a list of every possible matchup, home and away. Also assigns it a "uses left" value.
def generate_matchups(teamlist, weeknum):
    matchups = []
    games_in_week = len(teamlist) / 2
    games_in_season = games_in_week * weeknum
    for team1 in teamlist:
        for team2 in teamlist:
            if team1 != team2:
                newmatchup = Matchup(team1, team2, None) # to be used with "home" and "away" team class.
                matchups.append(newmatchup)
    for matchup in matchups:
        matchup.usesleft = (games_in_season / len(matchups))
    return matchups

# Attempting to fix above issue. This helps but not completely. Needs to prioritize pulling from higher usesleft matchups first. (done in generate schedule)
def generate_matchups_v2(teamlist, weeknum): # fix name if going to use this
    matchups = []
    games_in_week = len(teamlist) / 2
    games_in_season = games_in_week * weeknum

    for i in range(len(teamlist) - 1): # 0 to 6 (8 team league)
        for j in range(i + 1, len(teamlist)): # 1 to 7 (8 team league)
            team1 = teamlist[i]
            team2 = teamlist[j]
            newmatchup = Matchup(team1, team2, None)
            matchups.append(newmatchup)
    for matchup in matchups:
        matchup.usesleft = (games_in_season / len(matchups))
    return matchups


# Generates the full schedule by assigning matchups to each week
def generate_unshuffled_schedule(weeks, matchups, teamlist, time_limit):
    games_in_week = len(teamlist) / 2
    matchup_uses_left_resetter = matchups[0].usesleft
    gen_finished = False
    attempt_count = 0
    start_time = time.time()
    #time.sleep(0.05)
    #print(f"Each week will have {games_in_week} games.")  # For debugging
    print("\nGenerating schedule...")

    while not gen_finished:
        if time.time() - start_time > time_limit:
            print(f"\nTime limit exceeded ({time_limit} seconds). Schedule generation failed.")
            time.sleep(4)
            print("Closing the program...")
            time.sleep(2)
            exit(1)
            
        attempt_count += 1
        schedule = []
        for matchup in matchups:
            matchup.usesleft = matchup_uses_left_resetter  # Reset uses left for each matchup
        #time.sleep(1)
        #print("Generating schedule...")
        for week in weeks:
            #time.sleep(0.05)
            #print(f"\nGenerating {week.name}")
            week.matchups = []  # Reset matchups for the week
            matchupscopy = matchups.copy()
            random.shuffle(matchupscopy)  # Shuffle the matchups to randomize the order
            prioritized_matchups = sorted(matchupscopy, key=attrgetter("usesleft"), reverse=True)  # Sort by uses left
            usedteams = []
            matchups_this_week = []

            while len(matchups_this_week) < games_in_week:
                added = False
                for matchup in prioritized_matchups:
                    if matchup.usesleft <= 0:
                        continue
                    if matchup.team1 in usedteams or matchup.team2 in usedteams:
                        continue
                    matchups_this_week.append(matchup)
                    usedteams.extend([matchup.team1, matchup.team2])
                    matchup.usesleft -= 1
                    added = True
                    #time.sleep(0.05)
                    #print(f"Added: {matchup.team1} vs {matchup.team2} | Uses left: {matchup.usesleft}")
                    break
                if not added:
                    #time.sleep(0.05)
                    #print("No valid matchups left to assign this week.")
                    break
            
            week.matchups = matchups_this_week
            schedule.append(week)

        for week in schedule:
            if len(week.matchups) != games_in_week:
                # Start over if any week has fewer matchups than expected
                break
        
        # Checking if some teams played each other much more than they played another team instead of being balanced.
        prioritized_matchups = sorted(matchups, key=attrgetter("usesleft"))
        if abs(prioritized_matchups[0].usesleft - prioritized_matchups[-1].usesleft) > 1:
            continue
        else:
            gen_finished = True
            #time.sleep(0.2)
            #print(f"{week.name} was added to schedule with {len(week.matchups)} matchups: {[f'{m.team1} vs {m.team2}' for m in week.matchups]}")
            print(f"\nSchedule generated on attempt {attempt_count} after {time.time() - start_time:.3f} seconds.")

    return schedule


def print_schedule(schedule):
    for week in schedule:
        week.name = f"Week {schedule.index(week) + 1}"
        print(f"\n{week.name}")
        for value in week.matchups:
            print(f"{value.team1}  vs  {value.team2}")


def swap_2_item_list(list):
    swapped_list = [list[1], list[0]]
    return swapped_list


def shuffle_so_no_repeats(schedule, weeknum, time_limit):
    last_week = 0
    current_week = 1
    shuffle_count = 0
    start_time = time.time()
    print("\nShuffling schedule...")
    
    while current_week < weeknum:

        if time.time() - start_time > time_limit:
            print(f"\nTime limit exceeded ({time_limit} seconds). Shuffling failed.")
            time.sleep(2)
            print("Closing the program...")
            time.sleep(1.5)
            exit(1)
                
        last_week_matchups = []
        current_week_matchups = []

        for week in schedule[last_week].matchups:
            last_week_matchups.append([{week.team1}, {week.team2}])

        for week in schedule[current_week].matchups:
            current_week_matchups.append([{week.team1}, {week.team2}])

        for matchup in current_week_matchups:
            if matchup in last_week_matchups or swap_2_item_list(matchup) in last_week_matchups: # swapped function useless with no home/away teams.
                random.shuffle(schedule)
                last_week = 0
                current_week = 1
                shuffle_count += 1
                break
        else:
            current_week += 1
            last_week += 1
    
    print(f"\nShuffling complete after {shuffle_count} shuffles and {time.time() - start_time:.3f} seconds.")
    return schedule
