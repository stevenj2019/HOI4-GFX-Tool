import os 
import shutil
import re
from jinja2 import Environment, FileSystemLoader
class GFXTools:
    @staticmethod
    def ReadGFXFile(filepath:str):
        with open(filepath, "r") as file:
            FILEDATA = file.readlines() 
            return "".join(FILEDATA)
        
    @staticmethod
    def CollectNewSprites(import_directories:list[str]):
        new_sprites = list[str]()
        report = dict[str, int]()
        for dir in import_directories:
            report[dir] = 0
            for file in os.listdir(dir):
                if file.endswith("dds") or file.endswith("png") or file.endswith("tga"):
                    new_sprites.append(os.path.join(dir, file))
                    report[dir]+=1
        return new_sprites, report
    
    @staticmethod
    def BackupGFXFile(file):
        if os.path.exists(file):
            file_bak = file.replace(".gfx", ".bak")
            if os.path.exists(file_bak):
                os.remove(file_bak)
            shutil.copyfile(file, file_bak)
    
    @staticmethod
    def GenerateGFXFile(file:str, sprite_data:list[dict], env:Environment):
        template = env.get_template('template.gfx.jinja')
        file_data = template.render(sprite_array=sprite_data)
        with open(file, "w") as FILE:
            FILE.write(file_data)

    @staticmethod
    def GenerateGFXShineFile(shine_file:str, sprite_data:list[dict], env:Environment):
        template = env.get_template('template_shine.gfx.jinja')
        file_data = template.render(sprite_array=sprite_data)
        with open(shine_file, "w") as FILE:
            FILE.write(file_data)
    
    @staticmethod
    def SerializeGFXFile(file_data:str):
        pattern = r'name\s*=\s*"([^"]+)"\s*texturefile\s*=\s*"([^"]+)"'

        seen_names = set[str]()
        duplicates = list[str]()
        sprite_list = list[dict]()
        for name, texture in re.findall(pattern, file_data):
            if name in seen_names:
                duplicates.append(name)
            else:
                seen_names.add(name)
                sprite_list.append({'name': name, 'texturefile': texture})
        return sprite_list, duplicates
    
    @staticmethod
    def CopyAllAssetsToDirectory(file_source:list[dict[str, str]], base_path:str):
        for file in file_source:
            filename_with_extension = file['src'].split("\\")[-1]
            if not filename_with_extension.startswith("GFX_"):
                filename_with_extension = f"GFX_{filename_with_extension}"
            shutil.copyfile(file['src'], f"{base_path}\\{filename_with_extension}")

    @staticmethod
    def GetAllGoalFilesFromDir(goal_file:str, dir:str):
        files = set(os.listdir(dir))
        goal_files = list[str]()
        goal_shine_files = list[str]()
        for f in files:
            if not f == goal_file:
                if f.lower().endswith("_goals.gfx"):
                    goal_files.append(os.path.join(dir, f))
                    goal_shine_files.append(f"{f[:-10]}_goals_shine.gfx")
                    # file_prex = f[:-10]
                    # if f"{file_prex}_goals_shine.gfx" in files:
                        # goal_files.append(os.path.join(dir, f))
                        # goal_shine_files.append(f"{file_prex}_goals_shine.gfx")
        return goal_files, goal_shine_files
    
    # def GenerateGFXFiles(self, goal_file:str, shine_file:str):
    #     GFXTools.BackupGFXFile(goal_file)
    #     GFXTools.BackupGFXFile(shine_file)
        # template_env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
        # sprite_data = sorted(self.goals_json, key=lambda x: x['name'])
        # GFXTools.GenerateGFXFile(self.goal_file, sprite_data, template_env)
        # GFXTools.GenerateGFXShineFile(self.shine_file, sprite_data, template_env)