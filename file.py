import csv
import re
import sys

COLUMN_TITLE_ROW = ["datetime", "name",
                    "buyin", "players", "position", "payout"]
DIR_NAME = "termpoker_game_log.csv"

# determine if a termpoker CSV file already exists


def csv_file_exists():
    try:
        return open(DIR_NAME, 'r')
    except FileNotFoundError:
        return False

# save the given game array as a row in the termpoker CSV file


def save_game(game):
    row = [game["datetime"],
           game["name"],
           game["buyin"],
           game["players"],
           game["position"],
           game["payout"]]

    if (not csv_file_exists()):
        create_csv()

    append_row(row)

# create termpoker CSV file with column titles


def create_csv():
    with open(DIR_NAME, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(COLUMN_TITLE_ROW)
    csvFile.close()

# add given row to termpoker CSV file


def append_row(row):
    with open(DIR_NAME, 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

    csvFile.close()


# parse PokerStars tournament request email
def parse_email(file, player_name):

    arr = []
    with open(file, 'r') as email_file:

        print("Date, Tournament, Buy-In, Num Players, Position Placed, Notes, Payout, Prize-pool, Buyin, Reg-Fee")

        lines = email_file.readlines()
        i = 0
        a = 0
        g = 0
        while i < len(lines):
            line = lines[i]
            tournament = re.search("PokerStars Tournament #(\d+),", line)
            if(tournament):
                # Extract data from lines
                tournament = tournament.group(1)
                stakes_match = re.search(
                    "(Buy-In: \$(\d+.\d+)\/?\$?(\d+.\d+)?\s)|(Freeroll)", lines[i+1])

                players_match = re.search("(\d+) players", lines[i+2])

                prize_pool_match = re.search(
                    "Total Prize Pool: \$(\d+\.\d+)", lines[i+3])
                datetime_match = re.search(
                    "Tournament \w+ (\d+/\d+/\d+) (\d+:\d+:\d+ \w+) \[(\d+/\d+/\d+ \d+:\d+:\d+ \w+)\]", lines[i+4])

                i2 = 1
                while(not stakes_match and i2 < 6):
                    stakes_match = re.search(
                        "(Buy-In: \$(\d+.\d+)\/?\$?(\d+.\d+)?\s)|(Freeroll)", lines[i+1 + i2])
                    i2 += 1
                i2 = 1

                while(not players_match and i2 < 6):
                    players_match = re.search(
                        "(\d+) players", lines[i+2 + i2])
                    i2 += 1
                i2 = 1

                while(not prize_pool_match and i2 < 6):
                    prize_pool_match = re.search(
                        "Total Prize Pool: \$(\d+\.\d+)", lines[i+3 + i2])
                    i2 += 1
                i2 = 1

                while(not datetime_match and i2 < 6):
                    datetime_match = re.search(
                        "Tournament \w+ (\d+/\d+/\d+) (\d+:\d+:\d+ \w+) \[(\d+/\d+/\d+ \d+:\d+:\d+ \w+)\]", lines[i+4 + i2])
                    i2 += 1

                if(stakes_match and players_match and prize_pool_match and datetime_match):
                    # If tournament is a freeroll
                    # print(lines[i+1])
                    # print(stakes_match)
                    if(stakes_match.group(4)):
                        buyin = "0.00"
                        reg_fee = "0.00"
                    else:
                        buyin = stakes_match.group(2)
                        reg_fee = stakes_match.group(3)
                        if(not reg_fee):
                            reg_fee = "0.00"

                    players = players_match.group(1)
                    prize_pool = prize_pool_match.group(1)

                    date = datetime_match.group(1)
                    time = datetime_match.group(2)
                    # Search for placement...
                    # print(i)
                    for x in range(int(players) + 10):
                        #print(lines[i+x + 5])
                        placement_search = re.search(
                            "(\d+): " + player_name + " \(.+\), ?\$?(\d+\.\d+)?\s", lines[i+x])
                        if(placement_search):
                            # &nbsp; 12: Hazzaeve (United Kingdom), $0.51 (1.574%)<br>
                            placement = placement_search.group(1)
                            if(placement_search.group(2)):
                                payout = placement_search.group(2)
                            else:
                                payout = "0.00"
                            g += 1
                            # Create Row
                            # Append Row
                            arr.append(date + "," + tournament + "," + buyin + "," +  players + "," + placement + "," + ","  + payout + "," + prize_pool + "," + buyin + "," + reg_fee)
                            #print(date + "," + tournament + "," + buyin + "," +  players + "," + placement + "," + ","  + payout + "," + prize_pool + "," + buyin + "," + reg_fee)
                            i += int(players) - 1
                            break
                else:
                    #For debugging
                    if(False):
                        print()
                        print(tournament)
                        print(stakes_match)
                        print(players_match)
                        print(prize_pool_match)
                        print(datetime_match)
                    i += 1

            else:
                i += 1
    for l in reversed(arr):
        print(l)
    print(g)


parse_email(sys.argv[1], sys.argv[2])
