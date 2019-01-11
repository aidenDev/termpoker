import csv

COLUMN_TITLE_ROW = ["datetime", "name", "buyin", "players", "position", "payout"]
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