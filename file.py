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
            tournament = re.search("", line)
            if(tournament):
                #Extract data from lines
                tournament = tournament.group(1)                                                # PokerStars Tournament #2625783044, No Limit Hold'em<br>
                stakes = re.search("\$(\d+.\d+)\/\$(\d+.\d+)\s", lines[i+1])                        #Buy-In: $0.09/$0.01 USD<br>
                buyin = stakes.group(1)
                reg_fee = stakes.group(2)
                stakes = re.search("", lines[i+2]).group(1)               #360 players<br>
                prize_pool = re.search("", lines[i+3]).group(1)     #Total Prize Pool: $32.40 USD <br>
                datetime = re.search("", lines[i+4])       #Tournament started 2019/06/08 11:25:59 WET [2019/06/08 6:25:59 ET]<br>
                date = datetime.group(1)
                time = datetime.group(2)
                # Search for placement...
                for x in range(players):
                    if(re.search(lines[i+x + 5]),"[d]+:" + player_name + ".*"):
                        placement = lines[i+x + 5] #&nbsp; 12: Hazzaeve (United Kingdom), $0.51 (1.574%)<br>
                        prize = lines[i+x + 5]


                        #Create Row
                        #Append Row
                        print(date + "," + tournament + "," + buyin + "," +  players + "," + placement + "," + ","  + payout + "," + prize_pool + "," + buyin + "," + reg_fee)
                        i += players
                    break
                
            else:
                i += 1

parse_email(sys.argv[1], sys.argv[2])