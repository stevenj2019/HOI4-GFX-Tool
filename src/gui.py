from easygui import buttonbox
from GFXObjects import MenuError, AppExit
from constants import scripted_dialogue
EOO_options = ("Exit App", "Exit to Main Menu")
def EndOfOperationMenu(previous_page:str):
    options=list(EOO_options)
    #match case that swaps the button text
    match previous_page:
        case "Goals GFX":
            options.append("Exit to Focus Menu")
        case "Idea GFX":
            options.append("Exit to Ideas Menu")
        case _:
            options.append("dev is a moron, tell him you saw this")

    exit_menu = str(buttonbox(  title="Operation Completed.",
                                choices=tuple(options),
                                default_choice=previous_page))
    
    #this match case needs options for the defaults
    match exit_menu:
        case "Exit to Main Menu":
            return True
        case "Exit App":
            raise AppExit
        #default covers previous page statements
        case _:
            pass
            
def UseDefaultFileMenu():
    return

def ScriptedWindows(storage_key:str, message_append:str=""):
    return str( buttonbox(title=scripted_dialogue['title'][storage_key],
                         msg=str(scripted_dialogue['messages'][storage_key] + message_append),
                         choices=scripted_dialogue['options'][storage_key]))