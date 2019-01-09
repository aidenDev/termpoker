import os

# display select interface to user and return the selected value
def get_selection(label, options):
    while True:
        os.system('clear')
        for i in range(len(options)):
            print("[" + str(i+1) + "] " + options[i])

        try:
            selection = int(input(label + ": "))
        except ValueError:
            continue
        
        index = selection-1
        if (index >= 0 and index < len(options)):
            return options[selection - 1]