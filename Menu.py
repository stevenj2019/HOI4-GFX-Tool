import os 
from pathlib import Path
# import easygui as gui
from easygui import diropenbox, fileopenbox
import gui
from GFXObjects import MenuError, AppExit
from GFXTools import GFXTools
import app_storage

def MainMenu():
    op = gui.ScriptedWindows("Main")
    match op:
        case "Focus GFX":
            GoalsMainMenu()
        case "Idea GFX":
            IdeasMainMenu()
        case "Exit":
            raise AppExit
        case _:
            raise MenuError(f"Option {op} is not valid") 
        

def before_goals_menu():
    goals_file = str(fileopenbox(title="Select goals.gfx File" if not app_storage.app_data.save_settings.save_all else "Select Default goals.gfx File",
                                 filetypes=["*.gfx"],
                                 default=os.path.join(app_storage.app_data.mod_directory, "interface\\")))
    if os.path.exists(goals_file) and os.path.isfile(goals_file):
        app_storage.app_data.SetGoalsGFX(goals_file)
    else:
        raise MenuError
    
def GoalsMainMenu():
    exit = False
    skip = False
    while not exit:
        if app_storage.app_data:
            #gui asking if you want to use default/ default answer being yes   
            pass     
            if not app_storage.app_data.focus_file:
                before_goals_menu()
        else:
            before_goals_menu()
        if not app_storage.app_data.focus_file.json:
            duplicates = app_storage.app_data.focus_file.SerializeFile()
            if duplicates:
                gui.ScriptedWindows("Duplicate_OnFileLoad", '\n'+"\n -".join(duplicates))
        
        op = gui.ScriptedWindows("GoalsMain", '\n\n\n\n\t\t'+f"FILE SELECTED: {app_storage.app_data.focus_file.goal_file}")
        match op:
            case 'Back to Main Menu':
                exit = True
                skip = True
                break
            
            case "File Refresh": 
                app_storage.app_data.focus_file.GenerateGFXFiles()
                gui.ScriptedWindows("RefreshFilesReport", f"{len(app_storage.app_data.focus_file.json)} Sprites saved to {app_storage.app_data.focus_file.goal_file} and {app_storage.app_data.focus_file.shine_file}")
            
            case "Import New Icons": 
                popup = False
                inner_op = None
                import_directories = set()
                while not inner_op == "Next:Select Save Location":
                    dir = diropenbox(title="Add Directory to Import", default=Path.home()) 
                    if os.path.exists(dir):
                        import_directories.add(dir)
                    inner_op = gui.ScriptedWindows("InputFilesDirLoop", '\n'+"\n".join(map(str, import_directories)))
                    # inner_op = str(gui.buttonbox(title="Add Icon Stores", msg=f"This is a loop, click continue when you wish to exit.\n{message}", choices=("Add another Input Folder", "Next:Select Save Location"))) 
                new_sprite_arr, new_image_report = GFXTools.CollectNewSprites(import_directories)
                for key in new_image_report.keys():
                    if new_image_report[key] != 0:
                        popup = True 
                if popup:
                    selected = gui.ScriptedWindows("IconPreLoadReport", '\n'+"\n".join([f"{k} - {v} Icons" for k, v in new_image_report.items()]))
                    if selected == "Go Back To Menu":
                        break 
                destination_dir = str(diropenbox(title="Set GFX Save location", default=os.path.join(app_storage.app_data.mod_directory, "gfx\\")))
                loaded, duplicates = app_storage.app_data.focus_file.RegisterNewIcons(destination_dir, new_sprite_arr)
                app_storage.app_data.focus_file.GenerateGFXFiles()
                msg = str()
                msg += f" {loaded} Sprites Saved" if loaded != 0 else ""
                msg += f" {duplicates} Duplicates Detected" if duplicates != 0 else ""
                gui.ScriptedWindows("IconLoadReport", msg)
            
            case "Consolidate Other Files":
                    goal_file_array, goal_shine_file_array = GFXTools.GetAllGoalFilesFromDir(app_storage.app_data.focus_file.goal_file, os.path.join(app_storage.app_data.mod_directory, "interface\\"))
                    inner_op = None
                    while not inner_op or inner_op == "add goals file":
                        inner_op = gui.ScriptedWindows("ConsolidateFileLoop", "\n".join(goal_file_array))
                        if "Next" in inner_op:
                            break
                        else:
                            new_file = str(fileopenbox("select other goals.GFX Files to consolidate", filetypes=["*.gfx"], default=os.path.join(app_storage.app_data.mod_directory, "interface\\"), multiple=True)) #type: ignore
                            goal_file_array = [*goal_file_array, *new_file]
                            goal_shine_file_array = [*goal_shine_file_array, *[f.replace("goals.gfx", "goals_shine.gfx") for f in new_file]]

                    loaded_dict = {}
                    for x, file in enumerate(goal_file_array):
                        file_path = os.path.join(os.path.join(app_storage.app_data.mod_directory, "interface\\"), file)
                        shine_file_path = os.path.join(os.path.join(app_storage.app_data.mod_directory, "interface\\"), goal_shine_file_array[x])
                        tmp_data, _ = GFXTools.SerializeGFXFile(GFXTools.ReadGFXFile(file_path))
                        loaded, duplicate = app_storage.app_data.focus_file.RegisterConsolidatedIcons(tmp_data)
                        loaded_dict[file] = {'loaded':loaded, 'duplicate':duplicate}
                        # BackupGFXFiles(file_path, shine_file_path) replace with object version
                        GFXTools.BackupGFXFile(file_path)
                        GFXTools.BackupGFXFile(shine_file_path)
                        os.remove(file_path)
                        if os.path.exists(shine_file_path):
                            os.remove(shine_file_path) 
                    app_storage.app_data.focus_file.GenerateGFXFiles()
                    for key, dict in loaded_dict.items():
                        dict["short_name"] = str(key.split("\\")[-1])
                    msg = "\n".join([f"{v['short_name']}:{v['loaded']} Loaded {v['duplicate']} Duplicates Ignored" for v in loaded_dict.values()])
                    gui.ScriptedWindows("ConsolidateReport", msg)
            case _:
                raise AppExit
        if not skip:
            exit = gui.EndOfOperationMenu("Goals GFX")

#
## IDEAS
# TODO do we centralise this?
# TODO just need to implement the relevant actions, the dats is in place, and the class has been written.

def before_ideas_menu():
    goals_file = str(fileopenbox(title="Select ideas.gfx File" if not app_storage.app_data.save_settings.save_all else "Select Default ideas.gfx File",
                                 filetypes=["*.gfx"],
                                 default=os.path.join(app_storage.app_data.mod_directory, "interface\\")))
    if os.path.exists(goals_file) and os.path.isfile(goals_file):
        app_storage.app_data.SetGoalsGFX(goals_file)
    else:
        raise MenuError
    
def IdeasMainMenu():
    exit = False
    skip = False
    while not exit:
        if app_storage.app_data:
            #gui asking if you want to use default/ default answer being yes   
            pass     
            if not app_storage.app_data.focus_file:
                before_ideas_menu()
        else:
            before_ideas_menu()
        if not app_storage.app_data.focus_file.json:
            duplicates = app_storage.app_data.focus_file.SerializeFile()
            if duplicates:
                gui.ScriptedWindows("Duplicate_OnFileLoad", '\n'+"\n -".join(duplicates))
        
        # op = gui.ScriptedWindows("GoalsMain", '\n\n\n\n\t\t'+f"FILE SELECTED: {app_storage.app_data.focus_file.goal_file}")
        # match op:

        if not skip:
            exit = gui.EndOfOperationMenu("Idea GFX") 

def before_cutscene_menu():
    cutscene_file = str(fileopenbox(title="Select cutscene.gfx File" if not app_storage.app_data.save_settings.save_all else "Select Default cutscene.gfx File",
                                 filetypes=["*.gfx"],
                                 default=os.path.join(app_storage.app_data.mod_directory, "interface\\")))
    if os.path.exists(cutscene_file) and os.path.isfile(cutscene_file):
        app_storage.app_data.SetGoalsGFX(cutscene_file)
    else:
        raise MenuError
