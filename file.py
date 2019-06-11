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
    with open(file, 'r') as email_file:

        print("Date, Tournament, Buy-In, Num Players, Position Placed, Notes, Payout, Prize-pool, Buyin, Reg-Fee")

        lines = email_file.readlines()
        i=0
        while i < len(lines):
            line = lines[i]
            tournament = re.search("PokerStars Tournament #(\d+),", line)
            if(tournament):
                #Extract data from lines
                tournament = tournament.group(1)                                                # PokerStars Tournament #2625783044, No Limit Hold'em<br>
                stakes_match = re.search("\$(\d+.\d+)\/\$(\d+.\d+)\s", lines[i+1])                        #Buy-In: $0.09/$0.01 USD<br>
                players_match = re.search("(\d+) players", lines[i+2])               #360 players<br>
                prize_pool_match = re.search("Total Prize Pool: \$(\d+\.\d+)", lines[i+3])     #Total Prize Pool: $32.40 USD <br>
                datetime_match = re.search("Tournament \w+ (\d+/\d+/\d+ \d+:\d+:\d+ \w+) \[(\d+/\d+/\d+ \d+:\d+:\d+ \w+)\]", lines[i+4])       #Tournament started 2019/06/08 11:25:59 WET [2019/06/08 6:25:59 ET]<br>
                if(stakes_match and players_match and prize_pool_match and datetime_match):
                    buyin = stakes_match.group(1)

                    reg_fee = stakes_match.group(2)
                    
                    players = players_match.group(1)
                    prize_pool = prize_pool_match.group(1)

                    date = datetime_match.group(1)
                    time = datetime_match.group(2)
                    # Search for placement...
                    #print(i)
                    for x in range(int(players) + 10):
                        #print(lines[i+x + 5])
                        placement_search = re.search("(\d+): " + player_name + " \(.+\), ?\$?(\d+\.\d+)?\s", lines[i+x])
                        if(placement_search):
                            placement = placement_search.group(1) #&nbsp; 12: Hazzaeve (United Kingdom), $0.51 (1.574%)<br>
                            if(placement_search.group(2)):
                                payout = placement_search.group(2)
                            else:
                                payout = "0.00"


                            #Create Row
                            #Append Row
                            print(date + "," + tournament + "," + buyin + "," +  players + "," + placement + "," + ","  + payout + "," + prize_pool + "," + buyin + "," + reg_fee)
                            i += int(players) - 1
                            break
                i += 1
                
            else:
                i += 1

parse_email(sys.argv[1], sys.argv[2])