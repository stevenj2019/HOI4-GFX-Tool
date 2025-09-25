import json
import os 
from GFXObjects import FocusIconsMainFile, GenericGFXMainFile

class SaveSettings():
    def __init__(self, save_int:int):
        self.save_nothing = True if save_int == 0 else False
        self.save_mod = True if save_int == 1 else False
        self.save_all = True if save_int == 2 else False

    def GetSaveInt(self):
        if self.save_nothing:
            return 0
        elif self.save_mod:
            return 1
        elif self.save_all:
            return 2
        else:
            return -1
        
class AppData():
    def __init__(self, config_file:str):
        self.config_file   = config_file #filepath/file string
        self.config_json   = None        #config dict
        self.interface_dir = None        #filepath string
        self.gfx_dir = None              #filepath string 
        self.mod_directory = None        #filepath string 
        self.save_settings = None        #SaveSettings()
        self.focus_file = None           #FocusIconsMainFile()
        self.idea_file = None            #GenericGFXMainFile()
        self.cutscene_file = None        #

    def SetSaveState(self, save_int:int):
        self.save_settings = SaveSettings(save_int)
        if save_int != -1:
            self.config_json["SAVE_STATE"] = save_int

    def SetGoalsGFX(self, goal_file:str, save_override:bool=False):
        self.focus_file = FocusIconsMainFile()
        self.focus_file.LoadFromInput(goal_file)
        if self.save_settings.save_all and not save_override:
            if not goal_file == self.focus_file.goal_file:
                self.config_json["FOCUSICONS"] = {
                    'GOAL_FILE': self.focus_file.goal_file,
                    'SHINE_FILE': self.focus_file.shine_file
                }
        
    def SetIdeasGFX(self, idea_file:str, save_override:bool=False):
        self.idea_file = GenericGFXMainFile()
        self.idea_file.LoadFromInput(idea_file)

        if self.save_settings.save_all and not save_override:
            if not idea_file == self.idea_file.gfx_file:
                self.config_json["IDEAICONS"] = { 'IDEA_FILE': self.idea_file.gfx_file }

    def LoadFromConfig(self):
        if os.path.exists(self.config_file):
            self.config_json = json.load(open(self.config_file, "r")) 
            KEYS = self.config_json.keys()

            self.SetSaveState(self.config_json['SAVE_STATE'])
            self.mod_directory = self.config_json['MANAGING'] if 'MANAGING' in KEYS else None
            
            # self.SetSaveState(self.config_json['save_state'] if 'save_state' in KEYS else 0) this should ALWAYS BE SAVED
            # self.interface_dir = self.config_json['INTERFACE_DIR'] if 'INTERFACE_DIR' in KEYS else None
            # self.gfx_dir = self.config_json['GFX_DIR'] if 'GFX_DIR' in KEYS else None

            if "FOCUSICONS" in KEYS:
                self.focus_file = FocusIconsMainFile()
                self.focus_file.LoadFromConfig()
            if "IDEAICONS" in KEYS:
                self.idea_file = GenericGFXMainFile()
                self.idea_file.LoadFromConfig()
            #add other config loads here
        else:
            self.config_json = dict()
            
    def LoadFromInput(self, base_dir:str):
        if os.path.exists(os.path.join(base_dir, "interface\\")) and os.path.exists(os.path.join(base_dir, "gfx\\")):
            self.mod_directory = base_dir

            if self.save_settings.save_all or self.save_settings.save_mod:
                self.config_json['MANAGING'] = self.mod_directory

            return True
        else:
            return False
        
    def SaveToConfig(self):
        if self.config_json.keys():
            json.dump(self.config_json, open(self.config_file, "w"), sort_keys=True, indent=4)