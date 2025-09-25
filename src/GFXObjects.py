import os
import json
import re
# from script import ReadGFXFile, SerializeGFXFile, BackupGFXFile, GenerateGFXFile, GenerateGFXShineFile, CollectNewSprites
# import shelve
# from app_storage import app_storage.app_data
import app_storage
from GFXTools import GFXTools 
from jinja2 import Environment, FileSystemLoader

class AppExit(Exception):
    "App Exit (normal)"
    pass

class MenuError(Exception):
    "Menus Brokened"
    pass

class GenericGFXMainFile():
    def __init__(self, type:str):
        self.config_key = type
        self.gfx_file = None
        self.json = None

    def LoadFromConfig(self):
        try:
            self.gfx_file = app_storage.app_data.config_json[self.config_key]['FILE']
        except KeyError:
            self.gfx_file = None

    def LoadFromInput(self, file:str):
        self.gfx_file = file.split("\\")[-1]

    def SerializeFile(self):
        self.json, duplicate_arr = GFXTools.SerializeGFXFile(GFXTools.ReadGFXFile(os.path.join(app_storage.app_data.mod_directory, "interface\\", self.gfx_file)))
        return duplicate_arr
        
    def GenerateGFXFiles(self):
        gfx_file_path = os.path.join(app_storage.app_data.mod_directory, "interface\\", self.gfx_file)
        GFXTools.BackupGFXFile(gfx_file_path)
        template_env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
        sprite_data = sorted(self.json, key=lambda x: x['name'])
        GFXTools.GenerateGFXFile(gfx_file_path, sprite_data, template_env)

class FocusIconsMainFile():
    def __init__(self):
        self.config_key = "FOCUSICONS"
        self.goal_file = None
        self.shine_file = None
        self.json = None

    def LoadFromConfig(self):
        try:
            self.goal_file = app_storage.app_data.config_json[self.config_key]["GOAL_FILE"]
            self.shine_file = app_storage.app_data.config_json[self.config_key]["SHINE_FILE"]
        except KeyError:
            self.goal_file, self.shine_file = None, None

    def LoadFromInput(self, goal_file:str):
        filename = goal_file.split("\\")[-1]
        self.goal_file = filename
        self.shine_file = self.goal_file.replace("goals", "goals_shine")

    def SerializeFile(self):
        self.json, duplicate_arr = GFXTools.SerializeGFXFile(GFXTools.ReadGFXFile(os.path.join(app_storage.app_data.mod_directory, "interface\\", self.goal_file)))
        return duplicate_arr
    
    # def RemoveDuplicates(self):
    #     dupes = 0
    #     seen_gfx = set()
    #     clean_json = list()
    #     for _dict in self.json:
    #         if _dict['name'] not in seen_gfx:
    #             seen_gfx.add(_dict['name'])
    #             clean_json.append(_dict)
    #         else:
    #             dupes += 1
    #     self.json = clean_json
    #     return dupes

    def GenerateGFXFiles(self):
        goal_file_path = os.path.join(app_storage.app_data.mod_directory, "interface\\", self.goal_file)
        shine_file_path = os.path.join(app_storage.app_data.mod_directory, "interface\\", self.shine_file)
        GFXTools.BackupGFXFile(goal_file_path)
        GFXTools.BackupGFXFile(shine_file_path)
        template_env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
        sprite_data = sorted(self.json, key=lambda x: x['name'])
        GFXTools.GenerateGFXFile(goal_file_path, sprite_data, template_env)
        GFXTools.GenerateGFXShineFile(shine_file_path, sprite_data, template_env)
        
    def RegisterNewIcons(self, to:str, new_sprites:dict):
        template_base_path = to.split("gfx\\")[1]
        template_base_path = f"gfx\\{template_base_path}"
        duplicate_arr = list[str]()
        load_sprite_array = list[dict[str, str]]()
        current_icons = set([n['name'] for n in self.json])
        for sprite in new_sprites:
            sprite_file = sprite.split("\\")[-1]
            sprite_name, file_extension = sprite_file.split(".")
            if not sprite_name.startswith("GFX_"):
                sprite_name = f"GFX_{sprite_name}"
            if sprite_name in current_icons:
                duplicate_arr.append(sprite_name)
            else:
                tmpdir = template_base_path.replace("\\", "/")
                load_sprite_array.append({'name':sprite_name, 'src':sprite, 'texturefile':f"{tmpdir}/{sprite_name}.{file_extension}"})
                current_icons.add(sprite_name)
        
        GFXTools.CopyAllAssetsToDirectory(load_sprite_array, to)
        self.json = [*self.json, *load_sprite_array]
        return len(load_sprite_array), len(duplicate_arr)

    def RegisterConsolidatedIcons(self, new_sprites:list[dict]):
        sprite_names = [s['name'] for s in self.json]
        duplicate = 0
        loaded = 0
        for sprite in new_sprites:
            if sprite['name'] not in sprite_names:
                loaded += 1
                self.json.append(sprite)
                sprite_names.append(sprite['name'])
            else:
                duplicate += 1
        return loaded, duplicate

class CutsceneIconsFile():
    def __init__(self):
        self.config_key = "CUTSCENES"
        self.gfx_file = None
        self.json = None

    def LoadFromConfig(self):
        try:
            self.gfx_file = app_storage.app_data.config_json[self.config_key]['FILE']
        except KeyError:
            self.gfx_file = None

    def LoadFromInput(self, file:str):
        self.gfx_file = file.split("\\")[-1]

    def SerializeFile(self):
        self.json, duplicate_arr = GFXTools.SerializeGFXFile(GFXTools.ReadGFXFile(os.path.join(app_storage.app_data.mod_directory, "interface\\", self.gfx_file)))
        return duplicate_arr
        
    def GenerateGFXFiles(self):
        gfx_file_path = os.path.join(app_storage.app_data.mod_directory, "interface\\", self.gfx_file)
        GFXTools.BackupGFXFile(gfx_file_path)
        template_env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
        sprite_data = sorted(self.json, key=lambda x: x['name'])
        GFXTools.GenerateGFXFile(gfx_file_path, sprite_data, template_env)
