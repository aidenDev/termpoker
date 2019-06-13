import csv
import re
import sys

COLUMN_TITLE_ROW = ["Date",  "Tournament ID", "Total Buyin",  "Number of Players",
                    "Placement", "Notes",  "Payout",  "Prize Pool",  "Buyin",  "Registration Fee"]
DIR_NAME = "termpoker_game_log.csv"

player_history = {}

# determine if a termpoker CSV file already exists


def csv_file_exists():
    try:
        return open(DIR_NAME, 'r')
    except FileNotFoundError:
        return False

# save the given game array as a row in the termpoker CSV file


def save_game(game):
    row = [game["Date"],
           game["Tournament ID"],
           game["Total Buyin"],
           game["Number of Players"],
           game["Placement"],
           game["Notes"],
           game["Payout"],
           game["Prize Pool"],
           game["Registration Fee"]]

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


def tournament_added(id):
    with open(DIR_NAME, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if(row[1] == id):
                return True
    return False


# parse PokerStars tournament request email
def parse_email(file, player_name):
    arr = []
    with open(file, 'r') as email_file:

        print("Date, Tournament, Buy-In, Num Players, Position Placed, Notes, Payout, Prize-pool, Buyin, Reg-Fee")
        lines = email_file.readlines()
        i = 0
        g = 0
        sum_payouts = 0.00
        sum_buyins = 0.00
        while i < len(lines):
            tournament = None
            line = lines[i]
            try:
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
                        if(stakes_match.group(4)):
                            buyin = "0.00"
                            reg_fee = "0.00"
                        else:
                            buyin = stakes_match.group(2)
                            reg_fee = stakes_match.group(3)
                            # For tournaments with no registration fee such as the $0.02 sit & go
                            if(not reg_fee):
                                reg_fee = "0.00"

                        players = players_match.group(1)
                        prize_pool = prize_pool_match.group(1)

                        date = datetime_match.group(1)
                        time = datetime_match.group(2)

                        # Search for placement
                        for x in range(int(players) + 10):
                            placement_search = re.search(
                                "(\d+): " + player_name + " \(.+\), ?\$?(\d+\.\d+)?\s", lines[i+x])

                            if(placement_search):
                                placement = placement_search.group(1)
                                # Payout will be in group 2, if there is a payout
                                if(placement_search.group(2)):
                                    payout = placement_search.group(2)
                                else:
                                    payout = "0.00"
                                g += 1


                                total_buyin = round(float(buyin) + float(reg_fee),2)
                                sum_buyins += total_buyin
                                sum_payouts += float(payout)
                                arr.append([date,  tournament,  total_buyin,  players,
                                            placement, "",  payout,  prize_pool,  buyin,  reg_fee])
                                #print(date + "," + tournament + "," + buyin + "," +  players + "," + placement + "," + ","  + payout + "," + prize_pool + "," + buyin + "," + reg_fee)
                                i += int(players) - 1
                            player_search = re.search(
                                "(\d+): (.*) \(.+\), ?\$?(\d+\.\d+)?\s", lines[i+x])
                            if(player_search):
                                player = player_search.group(2)
                                if player in player_history:
                                    player_history[player]+= 1
                                else:
                                    player_history[player] = 1

                        
                    else:
                        # For debugging
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
            except:
                if(tournament):
                    print("The email may be malformed in some way for tournament {}, it has been skipped".format(tournament))
                i += 1
    for l in reversed(arr):
        
        if not tournament_added(l[1]):
            append_row(l)
            print("Added row", l, "to the database")
        else:
            print("Did not add row", l, "to the database as it is a duplicate")
    print("Num tournaments: {}, Total Buyins:${}, Total Payouts:${}, Profit/loss:${}".format(g,round(sum_buyins,2),round(sum_payouts,2),round(sum_payouts-sum_buyins,2)))


if not csv_file_exists():
    create_csv()
parse_email(sys.argv[1], sys.argv[2])
with open("playerhistory.csv","w") as file:
    for i in sorted(player_history.items(), key = lambda kv:(kv[1], kv[0])):
        file.write(i[0] + "," + str(i[1]) +"\n")

