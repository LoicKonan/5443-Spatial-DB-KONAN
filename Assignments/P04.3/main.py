import json
from commsCode.options import *

from simple_term_menu import TerminalMenu


CHOICE = []
CHOICE.append("Create Game")
CHOICE.append("Current Game")

with open("menu.json", "r") as f:
    data = json.loads(f.read())

    for options in data:
        CHOICE.append(options["item"])
        
    
    



def main():
    while(True):
        terminal_menu = TerminalMenu(CHOICE)
        menu_entry_index = terminal_menu.show()
        value = "Success "
        if CHOICE[menu_entry_index] == "Start":
            start_game()
        if CHOICE[menu_entry_index] == "Generate Fleet":
            generate_fleet()
        
        if CHOICE[menu_entry_index] == "Current Game":
            current_game()
        
        if CHOICE[menu_entry_index] == "Create Game":
            create_game()
               
        if CHOICE[menu_entry_index] == "Get Battle Location":
            get_a_location()
            
        if CHOICE[menu_entry_index] == "Position Fleet":
            pass
            
        if CHOICE[menu_entry_index] == "Ships Speed":
            pass
            
        if CHOICE[menu_entry_index] == "Move Ships":
            pass
        if CHOICE[menu_entry_index] =="Turn Ships":
            turn_ship()
        
        if CHOICE[menu_entry_index] =="Move Guns":
            pass
        
        if CHOICE[menu_entry_index] =="Fire Guns":
            pass
            
        
        
        



if __name__ == "__main__":
    main()