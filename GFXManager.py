import os
import sys
from easygui import diropenbox, exceptionbox
from pathlib import Path
from GFXObjects import AppExit, MenuError
from APPObjects import AppData
from Menu import MainMenu
import gui

config_file = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "userconfig.json")
app_active = True

if __name__ == '__main__':
    import app_storage
    while app_active:
        try:
            app_storage.app_data = AppData(config_file)
            app_storage.app_data.LoadFromConfig()
            while app_active:
                if not app_storage.app_data.save_settings:
                    menu = gui.ScriptedWindows("First_Run")
                    match menu:
                        case "Noted, and yes save all":
                            save_int = 2
                        case "Noted, only save mod folders.":
                            save_int = 1
                        case "Save my preference not to share":
                            save_int = 0
                        case "Noted, and save nothing":
                            save_int = -1
                        case "I want to Leave.":
                            raise AppExit
                        case _:
                            raise MenuError(f"Option {menu} is not valid") 
                    app_storage.app_data.SetSaveState(save_int) 
                elif not app_storage.app_data.mod_directory:
                    mod_folder = str(diropenbox(title="Please Select your mods base file", 
                                                msg="This is where gfx/ and interface/ folders are located",
                                                default=Path.home()))
                    if os.path.exists(mod_folder):
                        success = app_storage.app_data.LoadFromInput(mod_folder)
                        if not success:
                            cont = gui.ScriptedWindows("InvalidModDir")
                            if not cont:
                                raise AppExit
                    else:
                        raise MenuError("diropenbox failed")
                else:
                    MainMenu()

        except AppExit:
            if app_storage.app_data.save_settings:
                app_storage.app_data.SaveToConfig()
            app_active = False
        except Exception as e:
            if app_storage.app_data.save_settings:
                app_storage.app_data.SaveToConfig()
            exceptionbox(title="ERROR", msg=e)
            app_active = False
    
