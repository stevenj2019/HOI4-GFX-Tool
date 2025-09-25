scripted_dialogue = {
    'title': {
        "Main": "Select Icon Type",
        "GoalsMain": "FOCUS:Select Operation",
        "First_Run": "Notice",
        "Duplicate_OnFileLoad": "WARNING: Duplicates Found",
        "RefreshFilesReport": "File Refresh Report",
        "InputFilesDirLoop": "Add Icon Stores",
        "IconPreLoadReport": "Icon Detection Report",
        "IconLoadReport": "Icon Load Report",
        "Consolidate_AutoConfirm": "Auto-Detect Files?",
        "ConsolidateFileLoop": "Select goals.gfx Files to Consolidate",
        "ConsolidateReport": "Icon Definition Consolidation Report",
        "InvalidModDir": "Invalid Mod Folder Selected"
    },
    'messages': {
        "Main": "Request to Dau if you want a new one (be prepared for minor pushback)",
        "GoalsMain": "File Refresh      - Reads the Selected goals.gfx file, and re-generates a new\n                    goals.gfx and goals_shine.gfx, resulting in a clean version\n                    of what you already have\nImport New Icons  - Allows you to select one or many folders to import them into\n                    your mod files and re-generates goals.gfx and\n                    goals_shine.gfx\nConsolidate       - allows you to select (optionally search for) gfx files,\n                    loading them, merging them, and re-generates goals.gfx and \n                    goals_shine.gfx",
        "First_Run": "Thank you for using this tool \nthis is the first run prompt, it will not re appear unless you save nothing at all\n                    The Programme only accessed folders/files you specifically select, and any files modifies will create a .bak file, NOTE: you should not solely rely on this method as they will be overwritten should the file be modified again, \nthe following options are available:\n -save all                     - We will Save mod folders (mod/gfx or\n                                 mod/interface), default files (*.gfx) \n -save only mod folders        - self expalanatory, only saves directories where\n                                 you select your mod is \n -save preference not to share - the only thing i save to config, is a 0 to stop\n                                 this message reappearing. \n -save nothing                 - doesnt even create the file, this will keep\n                                 popping up \n -i want to leave              - programme immediatly terminates",
        "Duplicate_OnFileLoad": "The Following Icons have Duplicates, Run File Refresh to Fix This",
        "RefreshFilesReport": "",
        "InputFilesDirLoop": "This is a loop, click continue when you wish to exit.",
        "IconPreLoadReport": "NOTE: This has not yet been merged with mod files. any data is between the input folders and their icons name's",
        "IconLoadReport": "Final Post-Merge Report",
        "Consolidate_AutoConfirm": "The Programme will search for files based on *_goals.gfx and *_goals_shine.gfx, and will be consolidated into your default(or selected) *_goals.gfx and _goals_shine.gfx files respectively\n You will still be able to add _goals.gfx files",
        "ConsolidateFileLoop": "Files Currently Being Consolidated:",
        "ConsolidateReport": "",
        "InvalidModDir": "you need to select the folder which contains gfx/ interface/ common/ etc."
    },
    'options': {
        "Main": ("Focus GFX", "Idea GFX","Exit"),
        "GoalsMain": ("File Refresh", "Import New Icons", "Consolidate Other Files", "Back to Main Menu"),
        "First_Run": ("Noted, and yes save all", "Noted, only save mod folders.", "Save my preference not to share", 
                      "Noted, and save nothing", "I want to Leave."),
        "Duplicate_OnFileLoad": ("OK", " OK"),
        "RefreshFilesReport": ("OK", " OK"),
        "InputFilesDirLoop": ("Add another Input Folder", "Next:Select Save Location"),
        "IconPreLoadReport": ("Continue", "Go Back To Menu"),
        "IconLoadReport": ("OK", " OK"),
        "Consolidate_AutoConfirm": ("Auto-Detect", "Auto-Detect (safe)", "No Thanks"),
        "ConsolidateFileLoop": ("add goals file", "Next: Begin Merging"),
        "ConsolidateReport": ("OK", " OK"),
        "InvalidModDir": ("OK", "Quit")
    }
}