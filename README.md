# HOI4-Tools
Tools for bulk Updating HOI4 mod files/GFX

- other tools use dirty edits to notepad, this uses a combination of regex search(match) and then also jinja2 templates to regenerate it allowed us to sort the icons list before re-generating it (with the intent of keeping TAG_ icons seperate)
Notes: 
- Only the Focus tool currently works, didnt get to debugging the ideas yet (if stuck, use the focus one, and delete the generated _shine counterpart)
- any file you modify with this application will also generate a .bak file, this is a mostly redundant safeguard at this point. but its left in in case of unfound bugs and issues (feel welcome to report)
- the GUI is bad, im sorry, i just dont care, youre more than welcome to contribute to this github to create a less ugly one though (or fork and create a derivitive, as allowed by license, have at it)

